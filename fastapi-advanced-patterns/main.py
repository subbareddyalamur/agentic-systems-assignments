from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import time
from datetime import datetime

app = FastAPI(title="FastAPI Advanced Patterns")

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = None

class User(BaseModel):
    id: int
    username: str
    email: str

async def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    return authorization.replace("Bearer ", "")

async def get_current_user(token: str = Depends(verify_token)) -> User:
    if token == "invalid":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return User(id=1, username="testuser", email="test@example.com")

@app.middleware("http")
async def add_process_time_header(request, call_next):
    print(f"[MIDDLEWARE] Incoming request: {request.method} {request.url.path}")
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"[MIDDLEWARE] Request processed. Time: {process_time:.4f}s")
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Timestamp"] = datetime.now().isoformat()
    return response

@app.get("/hello")
async def hello():
    return {"message": "Hello, Welcome to FastAPI!"}

@app.get("/items/", response_model=List[Item])
async def list_items(skip: int = 0, limit: int = 10):
    items = [
        Item(name="Item 1", price=9.99, tax=0.99),
        Item(name="Item 2", price=19.99, tax=1.99),
        Item(name="Item 3", price=29.99, tax=2.99),
    ]
    return items[skip:skip + limit]

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item, current_user: User = Depends(get_current_user)):
    if item.tax is None:
        item.tax = item.price * 0.1
    return item

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int, current_user: User = Depends(get_current_user)):
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item ID must be positive"
        )
    return Item(name=f"Item {item_id}", price=float(item_id * 10), tax=float(item_id))

@app.put("/items/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item: Item,
    current_user: User = Depends(get_current_user)
):
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item ID must be positive"
        )
    item.name = f"{item.name} (Updated)"
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, current_user: User = Depends(get_current_user)):
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item ID must be positive"
        )
    return None

@app.get("/user/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "The requested resource was not found"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
