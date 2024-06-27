import requests
import numpy as np
import os
import re

def URL_proccessor(URL):
    """Make sure the URL is in the right format"""
    punctation = '<>:"/\\|?*'
    for char in URL: 
        URL.replace(char, "")
    return URL

def download_website(URL):
    response = requests.get(URL)
    HTML = np.array(response.text.splitlines())
    return HTML

def load_website(URL):
    """ Load website from storage, if not there download the website"""
    if not os.path.isfile(f"data/{URL}.npy"):
        return download_website(URL)
    else:
        return np.load(f"data/{URL}.npy")

def extract_links(HTML):
    """Given a HTML page extract all the hyperlinks"""

    rule = np.char.find(lines, "href") != -1
    filtered_lines = lines[rule]
    applyall = np.vectorize(_extract_links)
    extracted_links = applyall(filtered_lines)
    return extracted_links

def _extract_links(l):
    link_match = re.search('href="([^"]*)"', l)
    if link_match:
        return link_match.group(1)
    else:
        return None

URL = "https://self-service.kcl.ac.uk"
HTML = download_website(URL)
parsed_links = _extract_links(HTML)
# print("HTML", HTML)
print(parsed_links)