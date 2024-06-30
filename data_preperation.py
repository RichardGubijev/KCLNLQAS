import json
import bs4
import os
import numpy as np
import html
from web_scraper import save_as_json
import re

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

def _strip_whitespace(TEXT):
    return re.sub(r"\s+", " ", TEXT)

def extract_text(WEBPAGE):
    soup = bs4.BeautifulSoup(WEBPAGE["HTML"], "html.parser")
    return _strip_whitespace(soup.get_text())

def _get_category(webpage):
    HTML = html.unescape(webpage["HTML"])
    webpage_parser = bs4.BeautifulSoup(HTML, "html.parser")
    return str(webpage_parser.h1)[4:-5].replace("&amp", "&")
    
def extract_categories(DATA):
    keys = _filter_out_keys(DATA, "category")
    categories = {}
    for k in keys:
        category = _get_category(DATA[k])
        categories[category] = DATA[k]["extracted_URLs"]
    return categories

def add_categories(CATEGORIES, DATA):
    for k in CATEGORIES.keys():
        for a in CATEGORIES[k]:
            if a in DATA:
                if "category" not in DATA[a]:
                    DATA[a]["category"] = [k]
                else:
                    DATA[a]["category"].append(k)
                DATA[a]["category_num"] = len(DATA[a]["category"])
                    

def build_graph(DATA):
    pass


DATA = load_json("webdata.json")
print(extract_text(DATA["https://self-service.kcl.ac.uk/article/KA-01971/en-us"]))
# categories = extract_categories(DATA)
# add_categories(categories, DATA)
# save_as_json(DATA, "webdata2.json")