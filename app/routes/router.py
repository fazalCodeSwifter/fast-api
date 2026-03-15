from fastapi import APIRouter, Depends
from app.models.abstraction import Item, ItemCreate
from app.services.item_service import item_service, ItemService

router = APIRouter()

# Dependency provider function
def get_item_service():
    return item_service

@router.post("/items/", response_model=Item)
async def create_item(
    item: ItemCreate, 
    service: ItemService = Depends(get_item_service)
):
    
    return service.create_item(item)

@router.get("/items/", response_model=list[Item])
async def read_items(service: ItemService = Depends(get_item_service)):
    return service.get_all_items()