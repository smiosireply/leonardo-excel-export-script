import requests

# this returns 403 unauthorized
# GRAPHQL_URL = 'https://one-essilorluxottica-cms.luxgroup.net/graphql'

# to work around this we can port forward the headless server service
GRAPHQL_URL = 'http://localhost:41180/graphql'

with open('query.graphql', 'r') as query_file:
    QUERY = query_file.read()

def get_response(site: str, doctype: str):
    session = requests.session()
    page = 0
    num_found = 0
    result = []

    while page == 0 or len(result) < num_found:
        params = {
            'page': page
        }

        json = {
            'query': QUERY,
            'variables': {
                'site': site,
                'docTypes': doctype
            }
        }

        response = session.post(GRAPHQL_URL, params=params, json=json)
        if not response.ok:
            raise Exception(f'Could not call /graphql (response={response.status_code} - {response.text})')
        
        page_result = response.json()['data']['content']['contents']
        
        num_found = page_result['numFound']
        if num_found == 0: break
        result += page_result['result']
        page += 1
    return result