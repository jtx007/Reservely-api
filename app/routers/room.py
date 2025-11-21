from webbrowser import get
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.services import room_service
from app.schemas.room import RoomRead, RoomCreate, RoomUpdate
from backend.app.routers.user import MessageResponse

router = APIRouter(tags=["Room"])

@router.get("/rooms", response_model=list[RoomRead])
def list_rooms(db: Session = Depends(get_db)):
  return room_service.get_all_rooms(db)

@router.get("/rooms{room_id}", response_model=RoomRead)
def get_room_by_id(room_id: int, db: Session = Depends(get_db)):
  return room_service.get_room(room_id=room_id, db=db)

@router.post("/rooms", response_model=RoomRead)
def create_room(room_create: RoomCreate, db: Session = Depends(get_db)):
  return room_service.create_room(room_create, db)

@router.put("/rooms/{room_id}", response_model=RoomRead)
def update_room_by_id(room_id: int, room_update: RoomUpdate, db: Session = Depends(get_db)):
  return room_service.update_room(room_id, room_update, db)

@router.delete("/rooms/{room_id}", response_model=MessageResponse)
def destroy_room_by_id(room_id: int, db: Session = Depends(get_db)):
  return room_service.destroy_room(room_id, db)