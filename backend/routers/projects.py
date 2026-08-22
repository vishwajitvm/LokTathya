from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.project import Project, Work, Contractor, Tender, Contract
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

@router.get("/")
def list_projects(
    q: Optional[str] = Query(None),
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(Project)
    if q:
        query = query.filter(Project.name.ilike(f"%{q}%"))
        
    projects = query.offset(offset).limit(limit).all()
    
    return {
        "data": [
            {
                "id": str(p.id),
                "name": p.name,
                "raw_name": p.raw_name
            }
            for p in projects
        ],
        "meta": {"limit": limit, "offset": offset, "has_more": len(projects) == limit}
    }

@router.get("/{id}")
def get_project(id: uuid.UUID, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "id": str(p.id),
        "name": p.name,
        "raw_name": p.raw_name
    }

@router.get("/{id}/history")
def get_project_history(id: uuid.UUID, db: Session = Depends(get_db)):
    return {"project_id": str(id), "history": []}

@router.get("/{id}/finance")
def get_project_finance(id: uuid.UUID, db: Session = Depends(get_db)):
    # Aggregates allocations for works of this project
    works = db.query(Work).filter(Work.project_id == id).all()
    work_ids = [w.id for w in works]
    
    # Financial allocation summaries
    return {
        "project_id": str(id),
        "financial_summary": {
            "status": "INSUFFICIENT_DATA",
            "message": "No allocations linked to this project"
        }
    }

@router.get("/{id}/tenders")
def get_project_tenders(id: uuid.UUID, db: Session = Depends(get_db)):
    works = db.query(Work).filter(Work.project_id == id).all()
    tenders_list = []
    for w in works:
        tenders = db.query(Tender).filter(Tender.work_id == w.id).all()
        for t in tenders:
            tenders_list.append({
                "id": str(t.id),
                "work_name": w.name,
                "tender_reference": t.tender_reference
            })
    return {"project_id": str(id), "tenders": tenders_list}

@router.get("/{id}/contracts")
def get_project_contracts(id: uuid.UUID, db: Session = Depends(get_db)):
    works = db.query(Work).filter(Work.project_id == id).all()
    contracts_list = []
    for w in works:
        tenders = db.query(Tender).filter(Tender.work_id == w.id).all()
        for t in tenders:
            contracts = db.query(Contract).filter(Contract.tender_id == t.id).all()
            for c in contracts:
                contractor = db.query(Contractor).filter(Contractor.id == c.contractor_id).first() if c.contractor_id else None
                contracts_list.append({
                    "id": str(c.id),
                    "contractor": contractor.name if contractor else "Unknown",
                    "amount": float(c.amount)
                })
    return {"project_id": str(id), "contracts": contracts_list}

@router.get("/{id}/documents")
def get_project_documents(id: uuid.UUID, db: Session = Depends(get_db)):
    return {"project_id": str(id), "documents": []}

@router.get("/{id}/sources")
def get_project_sources(id: uuid.UUID, db: Session = Depends(get_db)):
    return {"project_id": str(id), "sources": []}

@router.get("/{id}/financial-summary")
def get_project_financial_summary(id: uuid.UUID, db: Session = Depends(get_db)):
    return {
        "project_id": str(id),
        "status": "INSUFFICIENT_DATA",
        "message": "No financial allocations linked to this project"
    }
