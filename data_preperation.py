import json
import bs4
import os
import numpy as np
import html

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.loads(file.read())
    else:
        print(f"File {filename} does not exist!")
        return None
    
def _filter_out_keys(dictionary, filter):
    keys = np.array(list(dictionary.keys()))
    filter = np.char.find(keys, filter) > -1
    return keys[filter]

def _filter_out_dict(dictionary, filters):
    keys = set(dictionary.keys())
    for f in filters:
        keys = keys - set(_filter_out_keys(dictionary,f))
    for k in keys:
        dictionary.pop(k)


def extract_articles(DATA):
    pass

def extract_text(HTML):
    pass

def _get_category(webpage):
    HTML = html.unescape(webpage["HTML"])
    webpage_parser = bs4.BeautifulSoup(HTML, "html.parser")
    return str(webpage_parser.h1)[4:-5]
    

def extract_categories(DATA):
    keys = _filter_keys(DATA, "category")
    categories = {}
    for k in keys[filter]:
        category = _get_category(DATA[k])
        categories[category] = DATA[k]["extracted_URLs"]
    print(categories)
    return categories

def add_categories(DATA):
    pass


def build_graph(DATA):
    pass


DATA = load_json("webdata.json")
extract_categories(DATA)