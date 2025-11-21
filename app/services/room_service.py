from sqlalchemy.orm import Session
from app.schemas.room import RoomCreate, RoomUpdate
from app.models.room import Room

def get_all_rooms(db: Session):
  return db.query(Room).all()

def get_room(room_id: int, db: Session):
  return db.get(Room, room_id)

def update_room(room_id: int, room_update: RoomUpdate, db: Session):
  room = db.get(Room, room_id)
  update_room = room_update.model_dump(exclude_unset=True)
  
  for field, value in update_room.items():
    setattr(room, field, value)
  
  db.add(room)
  db.commit()
  db.refresh(room)
  return room

def destroy_room(room_id: int, db: Session):
  room = db.get(Room, room_id)
  db.delete(room)
  db.commit()
  return {"message": "room destroyed"}

def create_room(room_create: RoomCreate, db: Session):
  room = Room(
    name=room_create.name,
    description=room_create.description,
    restaurant_id=room_create.restaurant_id
  )
  
  db.add(room)
  db.commit()
  db.refresh(room)
  return room


  