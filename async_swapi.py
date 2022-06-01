import asyncio
import time
from more_itertools import chunked


URL = 'https://swapi.dev/api/people/'

async def get_more_info(url, session):  
    async with session.get(url) as response:
        a = await response.json()
        return a['title'] if a.get('title') else a['name']

async def get_info(urls, session):
    tasks = [asyncio.create_task(get_more_info(url, session)) for url in urls]
    for task in tasks:
        task_result = await task
        yield task_result

async def get_person(person_id, session):
    async with session.get(f'{URL}{person_id}') as response:
        data = await response.json()
        if data.get('name'):
            data['homeworld'] = ', '.join([i async for i in get_info([data['homeworld']], session)])
            data['films'] = ', '.join([i async for i in get_info(data['films'], session)])
            data['species'] = ', '.join([i async for i in get_info(data['species'], session)])
            data['vehicles'] = ', '.join([i async for i in get_info(data['vehicles'], session)])
            data['starships'] = ', '.join([i async for i in get_info(data['starships'], session)])
            del data['created']
            del data['edited']    
            del data['url'] 
            return data


async def get_people(all_ids, partition, session):
    for chunk_ids in chunked(all_ids, partition):
        tasks = [asyncio.create_task(get_person(person_id, session)) for person_id in chunk_ids]
        for task in tasks:          
            task_result = await task
            if task_result:
                yield task_result


start = time.time()
print(time.time() - start)