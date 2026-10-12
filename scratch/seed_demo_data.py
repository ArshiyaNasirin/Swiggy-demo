"""
Food Order API - Database Seed Script
=====================================
Utility script to populate the database with realistic sample restaurants, menu items, and a demo user.
"""

import os
import sys
from typing import Any, Dict, List, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.base import Base
from app.database.connection import SessionLocal, engine
from app.models.food_item import FoodItem
from app.models.restaurant import Restaurant
from app.models.user import User

DEMO_USER_DATA: Dict[str, str] = {
    "name": "Alex Morgan",
    "email": "alex.morgan@tastingroom.io",
    "phone": "+1 (555) 382-9011",
    "address": "742 Evergreen Terrace, Apt 4B, Downtown, 5th Ave",
}

RESTAURANTS_SEED_DATA: List[Dict[str, Any]] = [
    {
        "name": "Trattoria Bella Roma",
        "address": "124 Bella St, Downtown, 5th Ave",
        "phone": "+1-555-0101",
        "foods": [
            ("Bruschetta al Pomodoro", "Grilled artisanal sourdough topped with vine-ripened San Marzano tomatoes, fresh garlic, basil, and olive oil.", 12.50),
            ("Arancini Siciliani", "Crispy golden saffron risotto balls stuffed with rich ragù, melted mozzarella, and green peas.", 14.00),
            ("Handmade Tagliatelle Bolognese", "Slow-cooked traditional beef and pork ragù simmered for six hours, tossed with fresh egg tagliatelle.", 22.00),
            ("Truffle Gnocchi al Forno", "Potato gnocchi baked in a velvety black truffle cream sauce with wild mushrooms and fontina cheese.", 24.50),
            ("Margherita DOP Pizza", "San Marzano tomatoes, fresh buffalo mozzarella, fragrant basil leaves, and extra virgin olive oil.", 18.00),
            ("Classic Tiramisu", "Espresso-soaked savoiardi ladyfingers layered with whipped mascarpone cream and dusted with cocoa.", 9.50),
        ],
    },
    {
        "name": "Artisan Smash Burger Co.",
        "address": "45 Oak Ave, Downtown",
        "phone": "+1-555-0102",
        "foods": [
            ("Double Truffle Smash Burger", "Two crispy smashed Angus patties, black truffle aioli, Swiss cheese, and caramelized onions on brioche.", 15.50),
            ("Classic Bacon Cheddar Smash", "Double beef patty, thick cut smoked bacon, Wisconsin sharp cheddar, house burger sauce.", 14.00),
            ("Garlic Parmesan Truffle Fries", "Crispy shoestring fries tossed in garlic oil, freshly grated parmesan, and chives.", 6.50),
            ("Vanilla Bean Craft Milkshake", "Hand-spun rich Madagascar vanilla custard milkshake topped with whipped cream.", 6.00),
        ],
    },
    {
        "name": "Sakura Omakase & Sushi",
        "address": "88 Tokyo Way, Downtown",
        "phone": "+1-555-0103",
        "foods": [
            ("Salmon Nigiri Tasting (6 pcs)", "Premium Scottish salmon torched lightly with sweet nikiri soy and yuzu zest.", 22.00),
            ("Spicy Bluefin Tuna Crunch Roll", "Fresh chopped bluefin tuna, cucumber, sriracha mayo, topped with crispy tempura flakes.", 16.50),
            ("Tonkotsu Chashu Ramen", "Rich 16-hour pork bone broth, springy ramen noodles, tender pork belly chashu, and ajitsuke egg.", 17.50),
        ],
    },
    {
        "name": "El Toro Taqueria",
        "address": "12 Mission Blvd, Downtown",
        "phone": "+1-555-0104",
        "foods": [
            ("Carne Asada Tacos (3 pcs)", "Grilled citrus-marinated skirt steak on warm pressed corn tortillas with onion and cilantro.", 13.50),
            ("Birria Quesatacos with Consome", "Slow-braised beef brisket stuffed with melted Oaxaca cheese, served with rich dipping consome.", 15.00),
            ("Guacamole & Hand-Pressed Chips", "Fresh Hass avocado mashed with lime, jalapeño, and pico de gallo, served with warm tortilla chips.", 8.50),
        ],
    },
    {
        "name": "Le Petit Paris Bakery",
        "address": "5 Rue Gourmet, Downtown",
        "phone": "+1-555-0105",
        "foods": [
            ("Butter Croissant Trio", "Three freshly baked golden Parisian croissants with 84% cultured French butter.", 9.50),
            ("Pain au Chocolat", "Flaky layered pastry dough filled with rich Valrhona dark chocolate batons.", 4.75),
            ("Artisanal French Sourdough Loaf", "Naturally fermented 36-hour sourdough loaf with a blistered crunchy crust.", 7.50),
        ],
    },
    {
        "name": "Aloha Poke & Greens",
        "address": "22 Palm Lane, Downtown",
        "phone": "+1-555-0106",
        "foods": [
            ("Classic Ahi Tuna Poke Bowl", "Sashimi-grade yellowfin tuna, sweet onion, sea asparagus, sesame seeds, avocado, and jasmine rice.", 16.50),
            ("Salmon Avocado Super Bowl", "Marinated Atlantic salmon, edamame, cucumber ribbons, pickled ginger, and spicy ponzu.", 17.00),
            ("Ceremonial Matcha Green Tea Smoothie", "Japanese Uji matcha blended with organic almond milk, banana, and chia seeds.", 7.50),
        ],
    },
]


def seed() -> None:
    """
    Ensure tables exist and seed initial demo data for Users, Restaurants, and Foods.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == DEMO_USER_DATA["email"]).first()
        if not user:
            user = db.query(User).first()
            if user:
                user.name = DEMO_USER_DATA["name"]
                user.email = DEMO_USER_DATA["email"]
                user.phone = DEMO_USER_DATA["phone"]
                user.address = DEMO_USER_DATA["address"]
            else:
                user = User(
                    name=DEMO_USER_DATA["name"],
                    email=DEMO_USER_DATA["email"],
                    phone=DEMO_USER_DATA["phone"],
                    address=DEMO_USER_DATA["address"],
                )
                db.add(user)
            db.commit()
            db.refresh(user)

        for r_data in RESTAURANTS_SEED_DATA:
            existing_r = db.query(Restaurant).filter(Restaurant.name == r_data["name"]).first()
            if not existing_r:
                existing_r = Restaurant(
                    name=r_data["name"],
                    address=r_data["address"],
                    phone=r_data["phone"],
                    is_active=True,
                )
                db.add(existing_r)
                db.commit()
                db.refresh(existing_r)

            for food_name, desc, price in r_data["foods"]:
                existing_food = db.query(FoodItem).filter(
                    FoodItem.restaurant_id == existing_r.id,
                    FoodItem.name == food_name,
                ).first()
                if not existing_food:
                    f = FoodItem(
                        restaurant_id=existing_r.id,
                        name=food_name,
                        description=desc,
                        price=price,
                        is_available=True,
                    )
                    db.add(f)
            db.commit()

        print("Seeding complete! Successfully seeded restaurants and foods.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
