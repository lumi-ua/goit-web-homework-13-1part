from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from fastapi_limiter.depends import RateLimiter

from src.database.db import get_db
from src.database.models import User
from src.schemas import ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service


router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get("/", response_model=List[ContactResponse], description="Requests are limited", 
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), 
                        current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, description="Requests are limited", 
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), 
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, description="Requests are limited", dependencies=[Depends(RateLimiter(times=5, seconds=60))], 
             status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):    
    contact = await repository_contacts.create_contact(body, current_user, db)
    return contact
    


@router.put("/{contact_id}", response_model=ContactResponse, description="Requests are limited", 
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(body, contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", description="Requests are limited", dependencies=[Depends(RateLimiter(times=10, seconds=60))], 
               status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db), 
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.get("/search/", response_model=List[ContactResponse], description="Requests are limited", 
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts(query: str, db: Session = Depends(get_db), 
                          current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.search_contacts(query, current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts


@router.get("/birthdays/", response_model=List[ContactResponse], description="Requests are limited", 
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts_with_upcoming_birthdays(db: Session = Depends(get_db), 
                                               current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_with_upcoming_birthdays(current_user, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts

