from sqlmodel import Session, select
from app.database import engine
from app.models.restaurant import Restaurant

def seed_restaurants():
    restaurants_data = [
        {"name": "Pasta Palace", "open": 10, "close": 22, "description": "Homemade pasta, fresh sauces, and Italian wines."},
        {"name": "Sushi Station", "open": 11, "close": 23, "description": "Fresh sushi, sashimi, and Japanese comfort food."},
        {"name": "Taco Town", "open": 9, "close": 21, "description": "Street-style tacos, burritos, and margaritas."},
        {"name": "Burger Barn", "open": 8, "close": 20, "description": "Smash burgers, fries, and craft milkshakes."},
    ]

    with Session(engine) as session:
        for data in restaurants_data:
            existing = session.exec(select(Restaurant).where(Restaurant.name == data["name"])).first()
            if existing:
                existing.open = data["open"]
                existing.close = data["close"]
                existing.description = data["description"]
            else:
                session.add(Restaurant(**data))
        session.commit()
        print("🌱 Restaurant data seeded successfully.")
