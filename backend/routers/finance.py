from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from core.database import get_db
from models.finance import Budget, BudgetAllocation, FundRelease, Expenditure, FinancialYear
from typing import List, Dict, Any, Optional
import uuid

router = APIRouter(prefix="/api/v1/finance", tags=["Finance"])

@router.get("/budgets")
def list_budgets(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    budgets = db.query(Budget).offset(offset).limit(limit).all()
    return [
        {
            "id": str(b.id),
            "amount": float(b.amount),
            "currency": b.currency,
            "original_source_value": b.original_source_value
        }
        for b in budgets
    ]

@router.get("/allocations")
def list_allocations(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    allocations = db.query(BudgetAllocation).offset(offset).limit(limit).all()
    return [
        {
            "id": str(a.id),
            "project_id": str(a.project_id),
            "budget_id": str(a.budget_id),
            "amount": float(a.amount),
            "currency": a.currency
        }
        for a in allocations
    ]

@router.get("/releases")
def list_releases(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    releases = db.query(FundRelease).offset(offset).limit(limit).all()
    return [
        {
            "id": str(r.id),
            "allocation_id": str(r.allocation_id),
            "amount": float(r.amount),
            "date": r.date
        }
        for r in releases
    ]

@router.get("/expenditures")
def list_expenditures(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    expenditures = db.query(Expenditure).offset(offset).limit(limit).all()
    return [
        {
            "id": str(e.id),
            "work_id": str(e.work_id),
            "amount": float(e.amount),
            "date": e.date
        }
        for e in expenditures
    ]
