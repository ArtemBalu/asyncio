import asyncio
import aiohttp
import json

from more_itertools import chunked
from models import init_base, People, engine, Session

MAX_CHUNK = 10

async def get_person(client, person_id):
    result = await client.get(f'https://swapi.dev/api/people/{person_id}/')
    return await result.json()


async def insert_to_db(list_of_jsons):
    models = []
    for people in list_of_jsons:
        model = People(
                    birth_year = people.get('birth_year'),
                    eye_color = people.get('eye_color'),
                    films = people.get('films'),
                    gender = people.get('gender'),
                    hair_color = people.get('hair_color'),
                    height = people.get('height'),
                    homeworld = people.get('homeworld'),
                    mass = people.get('mass'),
                    name = people.get('name'),
                    skin_color = people.get('skin_color'),
                    species = people.get('species'),
                    starships = people.get('starships'),
                    vehicles = people.get('vehicles')
                )
        models.append(model)
    async with Session() as session:
        session.add_all(models)
        await session.commit()

async def main():
    await init_base()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, 84), MAX_CHUNK):
        coro_persons = [get_person(client, person_id) for person_id in chunk]
        result = await asyncio.gather(*coro_persons)
        asyncio.create_task(insert_to_db(result))
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)
    await client.close()
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())