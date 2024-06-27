import json
import bs4
import os

def load_json(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read()
    else:
        print(f"File {filename} does not exist!")
        return None

def extract_articles(DATA):
    pass

def extract_text(HTML):
    pass

def add_categories(DATA):
    pass

def build_graph(DATA):
    pass


DATA = load_json("webdata.json")