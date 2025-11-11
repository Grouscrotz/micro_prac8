import aio_pika
from uuid import UUID
from .settings import settings
from .schemas import DBEvent
from .database import SessionLocal

async def consume(msg: aio_pika.IncomingMessage):
    async with msg.process():
        payload = msg.body.decode()
        print(f"[USERS] Получено: {payload}")
        db = SessionLocal()
        event = DBEvent(event_type="medicine_added", payload=payload)
        db.add(event)
        db.commit()
        db.close()

async def start_consumer(loop):
    conn = await aio_pika.connect_robust(settings.amqp_url, loop=loop)
    ch = await conn.channel()
    q = await ch.declare_queue("medicine_added", durable=True)
    await q.consume(consume)
    return conn