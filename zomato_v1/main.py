from fastapi import FastAPI, HTTPException, Depends
from database import get_db, engine
from sqlalchemy.orm import Session
import models as models
import schemas as schemas
import uvicorn
from typing import List, Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Zomato_API",
    description="A simple API to manage restaurant data",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the Zomato API!"}

@app.get("/restaurants/", response_model=List[schemas.Restaurant])
def get_restaurants(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Retrieve a list of restaurants. Optionally filter by name.
    """
    if name:
        restaurants = db.query(models.RestroBase).filter(models.RestroBase.name.ilike(f"%{name}%")).all()
    else:
        restaurants = db.query(models.RestroBase).all()
    
    return restaurants

@app.post("/restaurants/", response_model=schemas.Restaurant)
def create_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    """
    Create a new restaurant.
    """
    db_restaurant = models.RestroBase(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    
    return db_restaurant

@app.put("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    """
    Update an existing restaurant by ID.
    
    """
    db_restaurant = db.query(models.RestroBase).filter(models.RestroBase.id == restaurant_id).first()
    
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    for key, value in restaurant.dict().items():
        setattr(db_restaurant, key, value)
    
    db.commit()
    db.refresh(db_restaurant)
    
    return db_restaurant

@app.delete("/restaurants/{restaurant_id}", response_model=schemas.Restaurant)
def delete_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    """
    Delete a restaurant by ID.
    """
    db_restaurant = db.query(models.RestroBase).filter(models.RestroBase.id == restaurant_id).first()
    
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db.delete(db_restaurant)
    db.commit()
    
    return db_restaurant

@app.get("/restaurants/search", response_model=List[schemas.Restaurant])
def search_restaurants_by_cuisine(cuisine: schemas.CuisineType, db: Session = Depends(get_db)):
    """
    Search restaurants by cuisine type.
    """
    restaurants = db.query(models.RestroBase).filter(models.RestroBase.cuisine_type == cuisine.value).all()
    
    if not restaurants:
        raise HTTPException(status_code=404, detail=f"No restaurants found for cuisine type: {cuisine.value}")
    
    return restaurants


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 



