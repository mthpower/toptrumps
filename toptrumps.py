import json
import asyncio
import aiohttp

def url(id):
    return f'https://candidates.democracyclub.org.uk/api/v0.9/persons/{id}/'

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 2):
            tasks.append(get_candidate_json_by_id(session, i))

        return await asyncio.gather(*tasks)


async def get_candidate_json_by_id(session, id):
    async with session.get(url(id)) as response:
        return await response.json()


def extract_card(person):
    name = person['name']
    gender = person['gender']
    email = person['email']



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    fut = asyncio.ensure_future(main())
    loop.run_until_complete(fut)
