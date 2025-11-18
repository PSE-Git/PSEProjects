"""
BOQ Items API routes - Add, Edit, Delete operations for PseApBoqItems
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import io

from ...db.database import get_db
from ...core import models, schemas

router = APIRouter(prefix="/api/boq-items", tags=["BOQ Items"])


@router.post("/", response_model=schemas.BoqItemResponse, status_code=status.HTTP_201_CREATED)
def create_boq_item(
    item: schemas.BoqItemCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new BOQ (Bill of Quantities) item.
    
    - **company_id**: Company ID (optional)
    - **project_type**: Type of project (e.g., "Residential", "Commercial")
    - **title**: Item title/name
    - **description**: Detailed description of the item
    - **unit**: Unit of measurement (e.g., "sqft", "piece", "running meter")
    - **basic_rate**: Basic rate per unit
    - **premium_rate**: Premium rate per unit
    """
    db_item = models.PseApBoqItems(
        company_id=item.company_id,
        project_type=item.project_type,
        title=item.title,
        description=item.description,
        unit=item.unit,
        basic_rate=item.basic_rate,
        premium_rate=item.premium_rate
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.get("/", response_model=List[schemas.BoqItemResponse])
def get_boq_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    company_id: Optional[int] = None,
    project_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all BOQ items with optional filtering.
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    - **company_id**: Filter by company ID
    - **project_type**: Filter by project type
    """
    query = db.query(models.PseApBoqItems)
    
    if company_id:
        query = query.filter(models.PseApBoqItems.company_id == company_id)
    
    if project_type:
        query = query.filter(models.PseApBoqItems.project_type == project_type)
    
    items = query.offset(skip).limit(limit).all()
    return items


@router.get("/project-types/{company_id}", response_model=List[str])
def get_project_types_by_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    """
    Get distinct project types for a specific company.
    
    - **company_id**: Company ID to filter project types
    
    Returns a list of unique project types available for the company.
    """
    # Query to get distinct project types
    project_types = db.query(models.PseApBoqItems.project_type)\
        .filter(models.PseApBoqItems.company_id == company_id)\
        .filter(models.PseApBoqItems.project_type.isnot(None))\
        .distinct()\
        .all()
    
    # Extract the project type values from tuples
    result = [pt[0] for pt in project_types if pt[0]]
    
    return result


@router.get("/{sno}", response_model=schemas.BoqItemResponse)
def get_boq_item(
    sno: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific BOQ item by SNo (Serial Number).
    """
    item = db.query(models.PseApBoqItems).filter(models.PseApBoqItems.sno == sno).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BOQ item with SNo {sno} not found"
        )
    
    return item


@router.put("/{sno}", response_model=schemas.BoqItemResponse)
def update_boq_item(
    sno: int,
    item_update: schemas.BoqItemUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a BOQ item.
    
    Only provided fields will be updated. Fields set to None will be ignored.
    """
    db_item = db.query(models.PseApBoqItems).filter(models.PseApBoqItems.sno == sno).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BOQ item with SNo {sno} not found"
        )
    
    # Update only provided fields
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    
    return db_item


@router.delete("/{sno}", status_code=status.HTTP_200_OK)
def delete_boq_item(
    sno: int,
    db: Session = Depends(get_db)
):
    """
    Delete a BOQ item by SNo.
    """
    db_item = db.query(models.PseApBoqItems).filter(models.PseApBoqItems.sno == sno).first()
    
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"BOQ item with SNo {sno} not found"
        )
    
    db.delete(db_item)
    db.commit()
    
    return {
        "success": True,
        "message": f"BOQ item with SNo {sno} deleted successfully"
    }


@router.get("/search/", response_model=List[schemas.BoqItemResponse])
def search_boq_items(
    query: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Search BOQ items by title or description.
    """
    search_pattern = f"%{query}%"
    
    items = db.query(models.PseApBoqItems).filter(
        (models.PseApBoqItems.title.like(search_pattern)) |
        (models.PseApBoqItems.description.like(search_pattern))
    ).all()
    
    return items


@router.post("/import-excel/preview")
async def preview_excel_import(
    file: UploadFile = File(...),
    company_id: Optional[int] = Query(None)
):
    """
    Preview Excel file content before importing.
    Only reads rows where Description AND (BasicRate OR PremiumRate) have values.
    
    Expected Excel columns:
    - ProjectType
    - Title
    - Description (required)
    - Unit
    - BasicRate (at least one of BasicRate or PremiumRate required)
    - PremiumRate (at least one of BasicRate or PremiumRate required)
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an Excel file (.xlsx or .xls)"
        )
    
    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Expected columns mapping
        column_mapping = {
            'ProjectType': 'project_type',
            'Title': 'title',
            'Description': 'description',
            'Unit': 'unit',
            'BasicRate': 'basic_rate',
            'PremiumRate': 'premium_rate'
        }
        
        # Check if required columns exist
        missing_columns = [col for col in column_mapping.keys() if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Filter rows: Description must have value AND (BasicRate OR PremiumRate must have value)
        df = df[
            df['Description'].notna() & 
            (df['BasicRate'].notna() | df['PremiumRate'].notna())
        ]
        
        # Replace NaN with None for optional fields
        df = df.where(pd.notna(df), None)
        
        # Prepare preview data
        preview_items = []
        for _, row in df.iterrows():
            item = {
                'company_id': company_id,
                'project_type': row.get('ProjectType'),
                'title': row.get('Title'),
                'description': row.get('Description'),
                'unit': row.get('Unit'),
                'basic_rate': float(row['BasicRate']) if pd.notna(row.get('BasicRate')) else None,
                'premium_rate': float(row['PremiumRate']) if pd.notna(row.get('PremiumRate')) else None
            }
            preview_items.append(item)
        
        return {
            "success": True,
            "total_rows": len(preview_items),
            "message": f"Found {len(preview_items)} valid rows to import",
            "items": preview_items
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing Excel file: {str(e)}"
        )


@router.post("/import-excel/save")
async def save_excel_import(
    file: UploadFile = File(...),
    company_id: int = Query(..., description="Company ID for the BOQ items"),
    db: Session = Depends(get_db)
):
    """
    Import and save BOQ items from Excel file to database.
    Only imports rows where Description AND (BasicRate OR PremiumRate) have values.
    """
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an Excel file (.xlsx or .xls)"
        )
    
    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Expected columns
        required_columns = ['ProjectType', 'Title', 'Description', 'Unit', 'BasicRate', 'PremiumRate']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Filter valid rows
        df = df[
            df['Description'].notna() & 
            (df['BasicRate'].notna() | df['PremiumRate'].notna())
        ]
        
        # Replace NaN with None
        df = df.where(pd.notna(df), None)
        
        # Save items to database
        saved_items = []
        for _, row in df.iterrows():
            db_item = models.PseApBoqItems(
                company_id=company_id,
                project_type=row.get('ProjectType'),
                title=row.get('Title'),
                description=row.get('Description'),
                unit=row.get('Unit'),
                basic_rate=float(row['BasicRate']) if pd.notna(row.get('BasicRate')) else None,
                premium_rate=float(row['PremiumRate']) if pd.notna(row.get('PremiumRate')) else None
            )
            db.add(db_item)
            saved_items.append(db_item)
        
        db.commit()
        
        # Refresh all items to get their IDs
        for item in saved_items:
            db.refresh(item)
        
        return {
            "success": True,
            "message": f"Successfully imported {len(saved_items)} BOQ items",
            "total_imported": len(saved_items),
            "items": [
                {
                    "sno": item.sno,
                    "company_id": item.company_id,
                    "project_type": item.project_type,
                    "title": item.title,
                    "description": item.description,
                    "unit": item.unit,
                    "basic_rate": item.basic_rate,
                    "premium_rate": item.premium_rate
                }
                for item in saved_items
            ]
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing Excel file: {str(e)}"
        )

