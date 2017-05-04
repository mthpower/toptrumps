import json
import asyncio
import aiohttp
import operator
from collections import Counter
from terminaltables import AsciiTable

def url(id):
    return f'https://candidates.democracyclub.org.uk/api/v0.9/persons/{id}/'

async def main():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 34000):
            tasks.append(get_candidate_json_by_id(session, i))

        return await asyncio.gather(*tasks)


async def get_candidate_json_by_id(session, id):
    async with session.get(url(id)) as response:
        person = await response.json()
        card = extract_card(person)
        table = create_table(card)
        print(table.table)


def extract_card(person):
    name = person.get('name')
    gender = person.get('gender')
    email = person.get('email')
    birth_date = person.get('birth_date')
    death_date = person.get('death_date')
    try:
        party_memberships = person['versions'][0]['data']['party_memberships'].values()
        parties = Counter(m['name'] for m in party_memberships)
        party = sorted(parties.items(), key=operator.itemgetter(1))[0][0]
    except KeyError:
        party = None

    try:
        standing_in = person['versions'][0]['data']['standing_in'].values()
        times_elected = sum(m.get('elected', False) for m in standing_in)
    except (KeyError, AttributeError):
        times_elected = None

    if email:
        score = score_email_address(email)
    else:
        score = None

    return {
        'name': name,
        'gender': gender,
        'email': email,
        'party': party,
        'score': score,
        'birth_date': birth_date,
        'death_date': death_date,
        'times_elected': times_elected,
    }

def create_table(card):
    return AsciiTable([list(x) for x in card.items()])


def score_email_address(email_address):
    email_providers_to_scores = {
        'aol.com': 1,
        'yahoo.com': 10,
        'hotmail.com': 100,
        'gmail.com': 1000,
    }

    _, email_provider = email_address.split('@')
    return email_providers_to_scores.get(email_provider, 10000)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    fut = asyncio.ensure_future(main())
    loop.run_until_complete(fut)
