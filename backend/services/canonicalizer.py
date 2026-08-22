import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from models.observation import Observation
from models.provenance import CanonicalFact, Claim, Evidence
from services.normalization import NormalizationService
from entity_resolution.engine import EntityResolutionEngine
from data_quality.reconciliation import ReconciliationEngine

class CanonicalizationFactory:
    """
    Step 14, 15, 16: Canonicalization & Provenance Pipeline.
    Resolves, normalises, reconciles, and links observations to canonical facts.
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.resolver = EntityResolutionEngine(db_session)

    def process_observation(self, obs_id: uuid.UUID) -> Optional[uuid.UUID]:
        """
        Executes full canonicalization pipeline for a single observation.
        """
        obs = self.db.query(Observation).filter(Observation.id == obs_id).first()
        if not obs:
            return None

        # 1. Normalization
        norm_val = obs.normalized_value
        if not norm_val and obs.raw_value:
            # Attempt to normalize numeric/dates
            parsed_num = NormalizationService.normalize_numeric(obs.raw_value)
            if parsed_num is not None:
                norm_val = {"value": parsed_num, "type": "numeric"}
                obs.normalized_value = norm_val
                self.db.flush()

        # 2. Entity Resolution
        # Resolve target reference entity if name
        resolved_id = None
        if obs.entity_type in ["representative", "ministry", "party", "geography"]:
            res = self.resolver.resolve_entity(obs.raw_value, obs.entity_type, obs.source_id)
            resolved_id = res.get("matched_entity_id")

        if not resolved_id:
            resolved_id = uuid.uuid4() # Fallback abstract identifier if not matchable

        # 3. Reconciliation
        # Find if a canonical fact already exists for this entity and attribute
        existing_fact = self.db.query(CanonicalFact).filter(
            CanonicalFact.entity_id == str(resolved_id),
            CanonicalFact.attribute_name == obs.field_name
        ).first()

        conflict_status = "CONSISTENT"
        canonical_val = norm_val or {"value": obs.raw_value, "type": "string"}

        if existing_fact:
            # Evaluate using reconciliation logic
            rec = ReconciliationEngine.evaluate_observations(
                {"normalized_value": existing_fact.value, "published_at": None},
                {"normalized_value": canonical_val, "published_at": None}
            )
            
            conflict_status = rec["status"]
            if rec["status"] == "SUPERSEDED":
                existing_fact.value = canonical_val
                existing_fact.status = "SUPERSEDED"
            elif rec["status"] == "CONFLICTING":
                existing_fact.conflict_status = "CONFLICTING"
                
            fact_id = existing_fact.id
        else:
            # Create new canonical fact
            new_fact = CanonicalFact(
                entity_id=str(resolved_id),
                attribute_name=obs.field_name,
                value=canonical_val,
                status="CURRENT",
                conflict_status=conflict_status
            )
            self.db.add(new_fact)
            self.db.flush()
            fact_id = new_fact.id

        # 4. Provenance Graph creation (Claim & Evidence)
        claim = Claim(
            claim_level="RECORD",
            description=f"Extracted fact for {obs.field_name} from raw source value '{obs.raw_value}'",
            status="CURRENT",
            canonical_fact_id=fact_id
        )
        self.db.add(claim)
        self.db.flush()

        evidence = Evidence(
            claim_id=claim.id,
            source_id=obs.source_id,
            document_id=obs.document_id,
            content_version_id=obs.content_version_id
        )
        self.db.add(evidence)
        self.db.commit()

        return fact_id
