import graphql_api

def get_rows(site):
    return [
        {
            'page_id': page['id'],
            'page_name': page['name'],
            'carousel_id': playlist['id'],
            'chip': [chip['name'] for chip in playlist['chip']],
            'carousel_title': playlist['title'],
            'carousel_description': playlist['description']
        }
        for page in graphql_api.get_response(site)
        for row in page['grid']['rows']
        for placement in row['placements']
        for playlist in placement['items']
        if 'id' in playlist
    ]

if __name__ == '__main__':
    print(get_rows('leonardo-en'))