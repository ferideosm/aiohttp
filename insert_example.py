import asyncio
from async_swapi import get_people
import asyncpg
import aiohttp
import config


MAX = 1000
PARTITION = 10


async def insert_users(pool: asyncpg.Pool, user_list):
    query = 'INSERT INTO users (name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, films, species, vehicles, starships)\
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)'
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.executemany(query, user_list)


async def main():
    pool = await asyncpg.create_pool(config.PG_DSN, min_size=20, max_size=20)
    tasks = []
    async with aiohttp.ClientSession() as session:
        async for person in get_people(range(1, MAX +1), PARTITION, session):
            person = [tuple(x for x in person.values())]
            tasks.append(asyncio.create_task(insert_users(pool, person)))
    await asyncio.gather(*tasks)
    await pool.close()

if __name__ == '__main__':
    asyncio.run(main())
