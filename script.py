import asyncio
import aiohttp
import json

from more_itertools import chunked
from models import init_base, People, engine, Session

MAX_CHUNK = 10

async def get_person(client,person_id):
    result = await client.get(f'https://swapi.dev/api/people/{person_id}/')
    return await result.json()


async def get_object_name(client, object_type, url_list):
    name_list = []
    if url_list:
        for url in url_list:
            response = await client.get(url)
            result = await response.json()
            if object_type == 'film':
                name = result.get('title')
            else:
                name = result.get('name')
            name_list.append(name)
    return name_list


async def insert_to_db(client, list_of_jsons):
    models = []
    for people in list_of_jsons:
        if people.get('name'):
            model = People(
                        birth_year = people.get('birth_year'),
                        eye_color = people.get('eye_color'),
                        films = await get_object_name(client, object_type='film', url_list=people.get('films')),
                        gender = people.get('gender'),
                        hair_color = people.get('hair_color'),
                        height = people.get('height'),
                        homeworld = await get_object_name(client, object_type='planet', url_list=[people.get('homeworld')]),
                        mass = people.get('mass'),
                        name = people.get('name'),
                        skin_color = people.get('skin_color'),
                        species = await get_object_name(client, object_type='species', url_list=people.get('species')),
                        starships = await get_object_name(client, object_type='starship', url_list=people.get('starships')),
                        vehicles = await get_object_name(client, object_type='vehicle', url_list=people.get('vehicles'))
                    )
            models.append(model)
    async with Session() as session:
        session.add_all(models)
        await session.commit()

async def main():
    await init_base()
    client = aiohttp.ClientSession()
    for chunk in chunked(range(1, 200), MAX_CHUNK):
        coro_persons = [get_person(client, person_id) for person_id in chunk]
        result = await asyncio.gather(*coro_persons)
        asyncio.create_task(insert_to_db(client, result))
    tasks = asyncio.all_tasks() - {asyncio.current_task()}
    await asyncio.gather(*tasks)
    await client.close()
    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(main())