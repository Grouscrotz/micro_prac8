import asyncio
from fastapi import FastAPI
from .routers import router
from .database import Base, engine
from .rabbitmq import start_consumer

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    asyncio.create_task(start_consumer(loop))