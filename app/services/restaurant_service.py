from sqlalchemy.orm import Session
from app.schemas.restaurant import RestaurantCreate, RestaurantUpdate
from app.models.restaurant import Restaurant

def get_all_restaurants(db: Session):
  return db.query(Restaurant).all()

def get_restaurant(restaurant_id: int, db: Session):
  return db.get(Restaurant, restaurant_id)

def update_restaurant(restaurant_id: int, restaurant_update: RestaurantUpdate, db: Session):
    restaurant = db.get(Restaurant, restaurant_id)
    if not restaurant:
        return None
    
    # Update only provided fields
    update_data = restaurant_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(restaurant, field, value)
    
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return restaurant

def destroy_restaurant(restaurant_id: int, db: Session):
  restaurant = db.get(Restaurant, restaurant_id)
  db.delete(restaurant)
  db.commit()
  return {"message": "restaurant destroyed"} 
  

def create_restaurant(restaurant_create: RestaurantCreate, db: Session):
  restaurant = Restaurant(
    name=restaurant_create.name,
    open=restaurant_create.open,
    close=restaurant_create.close,
    description=restaurant_create.description
  )
  db.add(restaurant)
  db.commit()
  db.refresh(restaurant)
  return restaurant