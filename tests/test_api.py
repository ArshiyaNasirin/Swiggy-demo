"""
Food Order API - Comprehensive Test Suite
=========================================
Unit and integration tests covering API endpoints, business logic validation,
database cascade operations, and order lifecycle state transitions using unittest & FastAPI TestClient.
"""

import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.connection import get_db
from app.main import app
from app.schemas.order import OrderStatus


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    """Override get_db dependency to use the isolated test database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class FoodOrderAPITestCase(unittest.TestCase):
    """
    Test suite verifying end-to-end functionality and business rules.
    """

    def setUp(self):
        """Create fresh database tables before each test execution."""
        Base.metadata.create_all(bind=test_engine)

    def tearDown(self):
        """Drop all tables after each test execution to isolate state."""
        Base.metadata.drop_all(bind=test_engine)

    def test_health_check(self):
        """Test health check endpoint returns 200 and healthy status."""
        response = client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("app_name", data)

    def test_create_and_get_user(self):
        """Test creating a new customer account and fetching it by ID."""
        payload = {
            "name": "Sarah Connor",
            "email": "sarah.connor@example.com",
            "phone": "+1-555-0199",
            "address": "404 SkyNet Way",
        }
        create_res = client.post("/api/v1/users/", json=payload)
        self.assertEqual(create_res.status_code, 201)
        user_id = create_res.json()["id"]
        self.assertEqual(create_res.json()["name"], "Sarah Connor")

        get_res = client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["email"], "sarah.connor@example.com")

    def test_duplicate_user_email_rejected(self):
        """Test creating a user with an already registered email returns 400."""
        payload = {
            "name": "John Doe",
            "email": "john.doe@example.com",
        }
        first_res = client.post("/api/v1/users/", json=payload)
        self.assertEqual(first_res.status_code, 201)

        dup_res = client.post("/api/v1/users/", json=payload)
        self.assertEqual(dup_res.status_code, 400)
        self.assertIn("already exists", dup_res.json()["detail"])

    def test_create_restaurant_and_food_item(self):
        """Test registering a restaurant and adding food items."""
        r_payload = {
            "name": "Luigi's Pizzeria",
            "address": "100 Olive St",
            "phone": "+1-555-3344",
            "is_active": True,
        }
        r_res = client.post("/api/v1/restaurants/", json=r_payload)
        self.assertEqual(r_res.status_code, 201)
        r_id = r_res.json()["id"]

        f_payload = {
            "name": "Pepperoni Feast Pizza",
            "description": "Crispy pepperoni, mozzarella, and house red sauce",
            "price": 16.50,
            "is_available": True,
        }
        f_res = client.post(f"/api/v1/restaurants/{r_id}/foods/", json=f_payload)
        self.assertEqual(f_res.status_code, 201)
        self.assertEqual(f_res.json()["restaurant_id"], r_id)
        self.assertEqual(f_res.json()["price"], 16.50)

    def test_order_placement_price_calculation_and_lifecycle(self):
        """
        Test end-to-end order flow:
          1. Create user and restaurant.
          2. Add 2 food items ($10.00 and $5.50).
          3. Place order for (2 x Item1) + (1 x Item2) = $25.50.
          4. Verify total_price and OrderStatus is Pending.
          5. Update status: Pending -> Confirmed -> Preparing -> Out for Delivery -> Delivered.
          6. Verify cannot cancel delivered order.
        """
        user = client.post("/api/v1/users/", json={"name": "Alice", "email": "alice@test.com"}).json()
        restaurant = client.post(
            "/api/v1/restaurants/",
            json={"name": "Bistro", "address": "1 Main St", "is_active": True},
        ).json()

        food1 = client.post(
            f"/api/v1/restaurants/{restaurant['id']}/foods/",
            json={"name": "Pasta Carbonara", "price": 10.00, "is_available": True},
        ).json()

        food2 = client.post(
            f"/api/v1/restaurants/{restaurant['id']}/foods/",
            json={"name": "Garlic Bread", "price": 5.50, "is_available": True},
        ).json()

        order_payload = {
            "user_id": user["id"],
            "restaurant_id": restaurant["id"],
            "delivery_address": "77 Sunset Blvd",
            "items": [
                {"food_item_id": food1["id"], "quantity": 2},
                {"food_item_id": food2["id"], "quantity": 1},
            ],
        }
        order_res = client.post("/api/v1/orders/", json=order_payload)
        self.assertEqual(order_res.status_code, 201)
        order = order_res.json()
        self.assertEqual(order["total_price"], 25.50)
        self.assertEqual(order["status"], OrderStatus.PENDING.value)
        self.assertEqual(len(order["order_items"]), 2)

        status_res = client.patch(
            f"/api/v1/orders/{order['id']}/status",
            json={"status": OrderStatus.PREPARING.value},
        )
        self.assertEqual(status_res.status_code, 200)
        self.assertEqual(status_res.json()["status"], OrderStatus.PREPARING.value)

        status_res2 = client.patch(
            f"/api/v1/orders/{order['id']}/status",
            json={"status": OrderStatus.DELIVERED.value},
        )
        self.assertEqual(status_res2.status_code, 200)
        self.assertEqual(status_res2.json()["status"], OrderStatus.DELIVERED.value)

        cancel_res = client.patch(f"/api/v1/orders/{order['id']}/cancel")
        self.assertEqual(cancel_res.status_code, 400)
        self.assertIn("already been delivered", cancel_res.json()["detail"])

    def test_order_cancellation(self):
        """Test cancelling a pending order transitions status to Cancelled."""
        user = client.post("/api/v1/users/", json={"name": "Bob", "email": "bob@test.com"}).json()
        restaurant = client.post(
            "/api/v1/restaurants/",
            json={"name": "Burger Bar", "address": "2 Main St", "is_active": True},
        ).json()
        food = client.post(
            f"/api/v1/restaurants/{restaurant['id']}/foods/",
            json={"name": "Cheeseburger", "price": 8.00, "is_available": True},
        ).json()

        order = client.post(
            "/api/v1/orders/",
            json={
                "user_id": user["id"],
                "restaurant_id": restaurant["id"],
                "delivery_address": "42 Galaxy Way",
                "items": [{"food_item_id": food["id"], "quantity": 1}],
            },
        ).json()

        cancel_res = client.patch(f"/api/v1/orders/{order['id']}/cancel")
        self.assertEqual(cancel_res.status_code, 200)
        self.assertEqual(cancel_res.json()["status"], OrderStatus.CANCELLED.value)

    def test_order_with_inactive_restaurant_fails(self):
        """Test ordering from an inactive restaurant fails with 400."""
        user = client.post("/api/v1/users/", json={"name": "Charlie", "email": "charlie@test.com"}).json()
        restaurant = client.post(
            "/api/v1/restaurants/",
            json={"name": "Closed Cafe", "address": "3 Main St", "is_active": False},
        ).json()
        food = client.post(
            f"/api/v1/restaurants/{restaurant['id']}/foods/",
            json={"name": "Latte", "price": 4.00, "is_available": True},
        ).json()

        order_res = client.post(
            "/api/v1/orders/",
            json={
                "user_id": user["id"],
                "restaurant_id": restaurant["id"],
                "delivery_address": "99 Market St",
                "items": [{"food_item_id": food["id"], "quantity": 1}],
            },
        )
        self.assertEqual(order_res.status_code, 400)
        self.assertIn("inactive", order_res.json()["detail"])


if __name__ == "__main__":
    unittest.main()
