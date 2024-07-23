from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def scrape_tower_data(tower_name):
    url = f'https://towerheroes.fandom.com/wiki/{tower_name}'
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    def clean_text(text):
        # Remove emojis and extra whitespace
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\u2600-\u26FF\u2700-\u27BF]+", 
            flags=re.UNICODE)
        return emoji_pattern.sub(r'', text).strip()

    def get_text_from_div(soup, data_source):
        element = soup.find('div', class_='pi-item pi-data pi-item-spacing pi-border-color', attrs={'data-source': data_source})
        if element:
            return clean_text(element.find('div', class_='pi-data-value pi-font').text)
        return None

    def get_table_data(soup):
        table = soup.find('table', {'class': 'wikitable', 'data-index-number': '1'})
        if not table:
            return None

        headers = [clean_text(header.text) for header in table.find_all('th')]
        logging.debug(f"Headers found: {headers}")
        rows = table.find_all('tr')[1:]  # Skip header row
        
        level_data = []
        for row in rows:
            cells = row.find_all('td')
            level_info = {}
            for index, header in enumerate(headers):
                value = clean_text(cells[index].text)
                logging.debug(f"Processing header: {header}, value: {value}")
                if header == 'Detection':
                    level_info['detection'] = value == '✔️'
                elif header == 'Level':
                    level_info['level'] = value
                else:
                    # Normalize header to match the expected output keys
                    key_map = {
                        'Mana Cost': 'mana_cost',
                        'Damage': 'damage',
                        'Range': 'range',
                        'Rate': 'rate',
                        'DPS': 'dps'
                    }
                    if header in key_map:
                        level_info[key_map[header]] = value
            logging.debug(f"Level info: {level_info}")
            level_data.append(level_info)
        
        return level_data

    data = {}
    data['gender'] = get_text_from_div(soup, 'gender')

    price = get_text_from_div(soup, 'price')
    if price and re.search(r'\d', price):
        data['price'] = price
    else:
        data['price'] = '0'

    data['limit'] = get_text_from_div(soup, 'limit')

    level_data = get_table_data(soup)
    if level_data:
        for level_info in level_data:
            if 'level' in level_info:
                level = level_info.pop('level')
                data[f'level {level}'] = level_info
            else:
                logging.error("Level key not found in level_info")
    
    return data

@app.route('/get_tower_info', methods=['GET'])
def get_tower_info():
    tower_type = request.args.get('tower_type')
    if not tower_type:
        return jsonify({'error': 'Tower type is required'}), 400

    data = scrape_tower_data(tower_type)
    if not data:
        return jsonify({'error': 'Tower not found'}), 404

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
