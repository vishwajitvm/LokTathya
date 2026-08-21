# SCHEMA COMPLETENESS REVIEW

## 1. Missing Entities Found & Added
- **Geography**: Added geo_entity (polymorphic table supporting Country, State, UT, District, Subdistrict, Block, Village, GramPanchayat, Municipality, MunicipalCorporation, Ward, Constituencies) and geo_relationship for complex historic/overlapping links.
- **Entity Resolution**: Added sys_entity_resolution for auditable tracking of raw -> canonical mappings.
- **Sources**: Added src_endpoint, src_ingestion_run, and src_fetch_event (decoupled from src_content_version).
- **Representatives**: Explicitly isolated ep_position.
- **Elections**: Explicitly added lec_event and lec_candidate.
- **Projects**: Added proj_work, proj_tender, proj_contract, proj_contractor.
- **Finance**: Added explicit separation for in_budget, in_allocation, in_release, and in_expenditure. 

## 2. Entities Intentionally Combined
- **Geography Hierarchy**: Merged strict tables (e.g. geo_district, geo_state) into a unified geo_entity mapped by a dynamic geo_relationship table. This prevents hardcoding a rigid parent-child tree that doesn't fit India's complex overlapping administrative and electoral boundaries.

## 3. Entities Intentionally Deferred
- **Prediction Results**: lec_prediction tables remain deferred from this core schema setup to maintain a strict wall between authoritative fact data and AI-derived forecasts. They will reside in a separate logical module.

## 4. Relationship Changes
- Converted geographic links to a many-to-many temporal relationship graph (geo_relationship).
- Decoupled src_content_version from src_fetch_event (many fetches -> one content version if hash unchanged).

## 5. Temporal Changes
- Applied alid_from and alid_until exclusively to real-world changing boundaries (geo_relationship, geo_entity) and active periods (ep_term). Observation times (etrieved_at, etch_time) use system-time timestamps.

## 6. Provenance Changes
- Supported claim_level on prov_claim to allow Dataset, Document, Record, and Claim granularities. Primitive rows like in_budget retain original_source_value for direct low-overhead provenance.

## 7. Embedding Changes
- Removed the hardcoded 1536 dimension constraint on i_embedding.vector. Used Vector() to allow dynamic dimensions dictated by the i_embedding_model row. 

## 8. Geography Changes
- Added a geom_simplified column alongside geom authoritative canonical geometry to explicitly support map rendering without destroying raw precision.

## 9. Migration Impact
- The updated schema relies on polymorphic tables and generic relationship mapping for geography, which increases query complexity (requiring recursive CTEs for hierarchical walks) but significantly improves long-term flexibility.

## 10. Final Recommended Table/Domain List
- **sys**: sys_entity_resolution
- **geo**: geo_entity, geo_relationship
- **src**: src_source, src_endpoint, src_dataset, src_ingestion_run, src_fetch_event, src_document, src_content_version
- **prov**: prov_claim, prov_evidence
- **rep**: ep_person, ep_party, ep_position, ep_term
- **elec**: lec_election, lec_event, lec_candidate, lec_result
- **proj**: proj_project, proj_work, proj_tender, proj_contract, proj_contractor
- **fin**: in_year, in_budget, in_allocation, in_release, in_expenditure
- **ai**: i_embedding_model, i_chunk, i_embedding

**TOTAL TABLES: 33**
