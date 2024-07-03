import json
import bs4
import os
import numpy as np
import html
from web_scraper import save_as_json
import re

# // TEMP // 
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

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

# def _filter_new_dict(dictionary, filter):
#     keys = np.array(list(dictionary.keys()))
#     filter = np.char.find(keys, filter) >= 0
#     new_dict = dictionary.copy()
#     for k in keys[filter]:
#         new_dict.pop(k)
#     return new_dict

def _filter_new_dict(dictionary, filter):
    keys = np.array(list(dictionary.keys()))
    filter = np.char.find(keys, filter) >= 0
    new_dict = {k: dictionary[k] for k in keys[filter]}
    return new_dict

# Cite: https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
def _strip_whitespace(TEXT):
    lines = (line.strip() for line in TEXT.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    TEXT = '\n'.join(chunk for chunk in chunks if chunk)
    return TEXT

# Cite: https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
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
                    
def add_text(DATA):
    for k in DATA.keys():
        DATA[k]["text"] = _strip_whitespace(extract_text(DATA[k]))

def add_title(DATA):
    for k in DATA.keys():
        soup = bs4.BeautifulSoup(DATA[k]["HTML"], "html.parser")
        title = soup.title.string.replace("\r", "").replace("\n","").replace("\t","").replace("\xa0","")
        title = str(title[:title.find("·")])
        DATA[k]["title"] = title
        print(f"{title}\n")

if __name__ == "__main__":
    key = "https://self-service.kcl.ac.uk/article/KA-01971/en-us"
    DATA = load_json("webdata.json")
    DATA = _filter_new_dict(DATA, "article")  
    add_title(DATA)

    # print(DATA[key]["HTML"])
    # categories = extract_categories(DATA)
    # add_categories(categories, DATA)
    # add_text(DATA)
    # save_as_json(DATA, "webdata2.json")