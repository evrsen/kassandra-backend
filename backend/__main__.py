from fastapi import FastAPI
import aio_pika
import asyncpg
import asyncio

from backend import pg_user, pg_db, pg_pass

async def main():
    async with asyncpg.create_pool(
        user=pg_user,
        password=pg_pass,
        database=pg_db,
        host="localhost"
    ) as apg_pool, aio_pika.connect_robust(
        "amqp://guest:guest@localhost/",
    ) as rmq_conn:
        async def consume_messages(message):
            async with message.process():
                data = message.body.decode()
                async with apg_pool.acquire() as conn:
                    await conn.execute(
                        "INSERT INTO messages (message) VALUES ($1)",
                        data
                    )
        
        channel = await rmq_conn.cannel()
        queue = await channel.declare_queue("messages")
        await queue.consume(consume_messages)

asyncio.run(main())