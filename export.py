import graphql_api
import html2text
from openpyxl import Workbook

def check_chip(chip):
    return ', '.join(chip) if chip else None

def check_description(description):
    return html2text.html2text(description).strip() if description else None

def get_rows(site):
    return [
        {
            'page_id': page['id'],
            'page_name': page['name'],
            'carousel_id': playlist['id'],
            'chip': check_chip([chip['name'] for chip in playlist['chip']]),
            'carousel_title': playlist['title'],
            'carousel_description': check_description(playlist['description'])
        }
        for page in graphql_api.get_response(site)
        for row in page['grid']['rows']
        for placement in row['placements']
        for playlist in placement['items']
        if 'id' in playlist
    ]

def save_to_excel(rows, filename):
    wb = Workbook()
    ws = wb.active

    if not rows:
        print("No data to save.")
        return

    headers = list(rows[0].keys())
    ws.append(headers)
    
    for row in rows:
        ws.append([row[h] for h in headers])

    wb.save(filename)
    print(f"Saved {len(rows)} rows to {filename}")

if __name__ == '__main__':
    rows = get_rows('leonardo-en')
    save_to_excel(rows, 'leonardo_output.xlsx')