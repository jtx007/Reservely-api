from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.services import restaurant_service
from app.schemas.restaurant import RestaurantRead, RestaurantCreate, RestaurantUpdate

router = APIRouter(tags=["Restaurant"])

@router.get("/restaurants", response_model=list[RestaurantRead])
def list_restaurants(db: Session = Depends(get_db)): 
    return restaurant_service.get_all_restaurants(db)


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def get_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_service.get_restaurant(restaurant_id=restaurant_id, db=db)


@router.put("/restaurants/{restaurant_id}", response_model=RestaurantRead)
def update_restaurant_by_id(restaurant_id: int, restaurant_update: RestaurantUpdate, db: Session = Depends(get_db)):
    return restaurant_service.update_restaurant(restaurant_id=restaurant_id, restaurant_update=restaurant_update, db=db)
class MessageResponse(BaseModel):
    message: str
@router.delete("/restaurants/{restaurant_id}", response_model=MessageResponse)
def delete_restaurant_by_id(restaurant_id: int, db: Session = Depends(get_db)):
    return restaurant_service.destroy_restaurant(restaurant_id=restaurant_id, db=db)



@router.post("/restaurants", response_model=RestaurantRead)
def create_restaurant(restaurant_create: RestaurantCreate, db: Session = Depends(get_db)):
    return restaurant_service.create_restaurant(restaurant_create, db)

