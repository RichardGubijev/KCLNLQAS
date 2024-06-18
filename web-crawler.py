import requests
import numpy as np
import os
import re

lines = []

if not os.path.isfile("data/lines.npy"):
    print("Scrapped File")
    url = "https://self-service.kcl.ac.uk/"
    response = requests.get(url)
    html = response.text
    lines = np.array(html.splitlines())
    np.save("data/lines", lines)
else: 
    print("Loaded File")
    lines = np.load("data/lines.npy")

def extractLink(l):
    link_match = re.search('href="([^"]*)"', l)
    if link_match:
        return link_match.group(1)
    else:
        return None

rule = np.char.find(lines, "href") != -1
filtered_lines = lines[rule]

applyall = np.vectorize(extractLink)
extracted_links = applyall(filtered_lines)

print(extracted_links)