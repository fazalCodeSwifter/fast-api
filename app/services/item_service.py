from app.models.abstraction import Item, ItemCreate

class ItemService:
    def __init__(self):
        # Farz karein ye hamara temporary database hai
        self.db = []

    def create_item(self, item_data: ItemCreate) -> Item:
        # Business Logic: ID generate karna aur save karna
        new_id = len(self.db) + 1
        new_item = Item(id=new_id, **item_data.model_dump())
        self.db.append(new_item)
        return new_item

    def get_all_items(self) -> list[Item]:
        return self.db

# Service ka aik instance banayein (Singleton pattern ki tarah)
item_service = ItemService()