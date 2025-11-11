import aio_pika
from uuid import UUID
from .settings import settings

async def publish(medicine_id: UUID):
    conn = await aio_pika.connect_robust(settings.amqp_url)
    ch = await conn.channel()
    await ch.default_exchange.publish(
        aio_pika.Message(body=f"Medicine added: {medicine_id}".encode()),
        routing_key="medicine_added"
    )
    await conn.close()