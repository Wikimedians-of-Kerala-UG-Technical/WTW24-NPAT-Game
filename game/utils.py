# game/utils.py
import requests

def make_query(name, template, entity):
    """
    Helper function to make a SPARQL query to Wikidata.
    """
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = template.format(name=name)
    response = requests.get(url, params={'query': query, 'format': 'json'})

    # Ensure the response is valid
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', {}).get('bindings', [])
        if results:
            return {
                'link': results[0]['item']['value'],
                'correct': True,
                'name': name,
                'entity': entity
            }
    return {'correct': False, 'name': name, 'entity': entity}


def check_name(name):
    """
    Check if a name exists as a person entity in Wikidata.
    """
    template = """SELECT ?item
    WHERE
    {{
      ?item wdt:P31 wd:Q5 .  # Q5 indicates human
      ?item rdfs:label "{name}"@en .
    }}
    """
    return make_query(name, template, "name")


def check_place(name):
    """
    Check if a place exists as a city or location in Wikidata.
    """
    template = """SELECT ?item
    WHERE
    {{
      ?item wdt:P31/wdt:P279* wd:Q515 .  # Q515 indicates city
      ?item rdfs:label "{name}"@en .
    }}
    """
    return make_query(name, template, "place")


def check_animal(name):
    """
    Check if an animal exists in Wikidata.
    """
    template = """SELECT ?item
    WHERE
    {{
      ?item wdt:P31 wd:Q16521 .  # Q16521 indicates animal
      ?item rdfs:label "{name}"@en .
    }}
    """
    return make_query(name, template, "animal")


def check_movie(name):
    """
    Check if a movie exists in Wikidata.
    """
    template = """SELECT ?item
    WHERE
    {{
      ?item wdt:P31 wd:Q11424 .  # Q11424 indicates film
      ?item rdfs:label "{name}"@en .
    }}
    """
    return make_query(name, template, "movie")


def get_examples(letter, entity):
    """
    Get examples of names, places, animals, or movies starting with a specific letter.
    """
    entity_mapping = {
        "name": "wd:Q5",        # Human
        "place": "wd:Q515",     # City
        "animal": "wd:Q16521",  # Animal
        "movie": "wd:Q11424"    # Film
    }

    if entity not in entity_mapping:
        return None

    template = """SELECT ?item ?itemLabel
    WHERE
    {{
      ?item wdt:P31 {entity} .
      ?item rdfs:label ?itemLabel .
      FILTER(LANG(?itemLabel) = "en") .
      FILTER(STRSTARTS(LCASE(?itemLabel), "{letter}"))
    }}
    LIMIT 5
    """
    url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
    query = template.format(letter=letter.lower(), entity=entity_mapping[entity])
    response = requests.get(url, params={'query': query, 'format': 'json'})

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', {}).get('bindings', [])
        return {"examples": results, "entity": entity}
    return None
