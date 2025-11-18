from typing import List, Optional
from sqlalchemy.orm import Session
from ..core import models, schemas

class ClientRepository:
    @staticmethod
    def create(db: Session, client: schemas.ClientCreate) -> models.Client:
        db_client = models.Client(**client.model_dump())
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        return db_client

    @staticmethod
    def update(db: Session, client_id: int, client: schemas.ClientUpdate) -> Optional[models.Client]:
        db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
        if db_client:
            for key, value in client.model_dump().items():
                setattr(db_client, key, value)
            db.commit()
            db.refresh(db_client)
        return db_client

    @staticmethod
    def delete(db: Session, client_id: int) -> bool:
        db_client = db.query(models.Client).filter(models.Client.id == client_id).first()
        if db_client:
            db.delete(db_client)
            db.commit()
            return True
        return False

    @staticmethod
    def get(db: Session, client_id: int) -> Optional[models.Client]:
        return db.query(models.Client).filter(models.Client.id == client_id).first()

class ProposalRepository:
    @staticmethod
    def create(db: Session, proposal: schemas.ProposalCreate) -> models.Proposal:
        # Create proposal
        proposal_data = proposal.model_dump(exclude={'proposal_items'})
        db_proposal = models.Proposal(**proposal_data)
        db.add(db_proposal)
        db.flush()  # Get proposal ID without committing

        # Create proposal items
        for item in proposal.proposal_items:
            item_data = item.model_dump()
            item_data['total'] = item.quantity * item.unit_price
            db_item = models.ProposalItem(**item_data, proposal_id=db_proposal.id)
            db.add(db_item)

        db.commit()
        db.refresh(db_proposal)
        return db_proposal

    @staticmethod
    def update(db: Session, proposal_id: int, proposal: schemas.ProposalUpdate) -> Optional[models.Proposal]:
        db_proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
        if not db_proposal:
            return None

        # Update proposal fields
        update_data = proposal.model_dump(exclude={'proposal_items'})
        for key, value in update_data.items():
            setattr(db_proposal, key, value)

        # Update proposal items if provided
        if proposal.proposal_items:
            # Delete existing items
            db.query(models.ProposalItem).filter(models.ProposalItem.proposal_id == proposal_id).delete()

            # Create new items
            for item in proposal.proposal_items:
                item_data = item.model_dump()
                item_data['total'] = item.quantity * item.unit_price
                db_item = models.ProposalItem(**item_data, proposal_id=proposal_id)
                db.add(db_item)

        db.commit()
        db.refresh(db_proposal)
        return db_proposal

    @staticmethod
    def delete(db: Session, proposal_id: int) -> bool:
        db_proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
        if db_proposal:
            db.delete(db_proposal)
            db.commit()
            return True
        return False

    @staticmethod
    def get(db: Session, proposal_id: int) -> Optional[models.Proposal]:
        return (
            db.query(models.Proposal)
            .filter(models.Proposal.id == proposal_id)
            .first()
        )

    @staticmethod
    def update_pdf_url(db: Session, proposal_id: int, pdf_url: str) -> Optional[models.Proposal]:
        db_proposal = db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()
        if db_proposal:
            db_proposal.pdf_url = pdf_url
            db.commit()
            db.refresh(db_proposal)
        return db_proposal