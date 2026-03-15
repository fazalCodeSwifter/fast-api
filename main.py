from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.config.prisma import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    print('Database Connected')

    yield
    
    await db.disconnect()
    print('Database Disconnected')

app = FastAPI(title='Advanced FastAPI MVC' ,lifespan=lifespan)
app.include_router(router.router, prefix="/v1", tags=["Items"])
@app.get("/")
def root():
    return {"message": "SOLID MVC Pattern is active!"}