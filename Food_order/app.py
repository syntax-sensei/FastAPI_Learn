from fastapi import FastAPI
from enum import Enum

from pydantic import BaseModel, Field, model_validator

app = FastAPI()

menu_db = [
{
    "id": 1,
    "name": "Margherita Pizza",
    "description": "Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
    "category": "main_course",
    "price": 15.99,
    "preparation_time": 20,
    "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
    "calories": 650,
    "is_vegetarian": True,
    "is_spicy": False,
    "is_available": True
},

{
    "id": 2,
    "name": "Caesar Salad",
    "description": "Fresh romaine lettuce with Caesar dressing, croutons, and parmesan cheese",
    "category": "salad",
    "price": 10.99,
    "preparation_time": 15,
    "ingredients": ["romaine lettuce", "Caesar dressing", "croutons", "parmesan cheese"],
    "calories": 350,
    "is_vegetarian": True,
    "is_spicy": False,
    "is_available": True
}
]

class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"

class FoodItemCreate(BaseModel):
    name: str = Field(..., max_length=100, pattern="^[a-zA-Z\s]+$")
    description: str = Field(..., min_length=10, max_length=500)
    price: float = Field(..., gt=10.0, le=100.0)
    category: FoodCategory
    is_available: bool
    preparation_time: int
    ingredients: list[str]
    calories: int
    is_vegetarian: bool
    is_spicy: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_vegetarian_calories(self):
        """Ensure vegetarian items have calories < 800"""
        if self.is_vegetarian and self.calories >= 800:
            raise ValueError('Vegetarian items must have calories less than 800')
        return self

    @model_validator(mode='after')
    def validate_beverage_preparation_time(self):
        """Ensure beverages have preparation time ≤ 10 minutes"""
        if self.category == FoodCategory.BEVERAGE and self.preparation_time > 10:
            raise ValueError('Beverages must have preparation time of 10 minutes or less')
        return self
    
    @model_validator(mode='after')
    def dessert_not_spicy(self):
        """Ensure desserts and beverages are not spicy"""
        if (self.category == FoodCategory.DESSERT or self.category == FoodCategory.BEVERAGE) and self.is_spicy:
            raise ValueError('Desserts and beverages cannot be spicy')
        return self

class FoodItem(FoodItemCreate):
    id: int
    
def generate_id():
    if menu_db:
        return max(item["id"] for item in menu_db) + 1
    return 1

@app.post("/menu/")
def create_food_item(food_item: FoodItemCreate):
    # Generate new ID
    new_id = generate_id()
    
    # Create the full food item with ID
    food_item_dict = food_item.dict()
    food_item_dict["id"] = new_id
    
    # Add to menu_db
    menu_db.append(food_item_dict)
    
    # Return the complete item
    return {"message": "Food item created successfully", "item": food_item_dict}

@app.put("/menu/{id}")
def update_food_item(id: int, food_item: FoodItemCreate):
    updated_data = food_item.dict()

    for item in menu_db:
        if item["id"] == id:
            item.update(updated_data)
            return {"message": "Food item updated successfully", "item": item}

    return {"error": "Food item not found"}


@app.delete("/menu/{id}")
def delete_food_item(id: int):
    for i, item in enumerate(menu_db):
        if item["id"] == id:
            del menu_db[i]
            return {"message": "Food item deleted successfully"}
    return {"error": "Food item not found"}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Food Order API!"}

@app.get("/health")
def health_check():
    return {"status": "Healthy", "menu_items_count": len(menu_db)}

@app.get("/menu")
def get_menu():
    return {"menu": menu_db}

@app.get("/menu/{id}")
def get_menu_item_by_id(id: int):
    for item in menu_db:
        if item["id"] == id:
            return {"item": item}
    return {"error": "Menu item not found"}





