import requests
import numpy as np
import os
import time
import json

def download_website(URL: str):
    response = requests.get(URL)
    return response.text

def _extract_candidate_lines(HTML_lines):
    condition = np.char.find(HTML_lines, "href") != -1
    filtered_one = HTML_lines[condition]
    condition_two = np.char.find(filtered_one, "<a") != -1
    filtered_two = filtered_one[condition_two]
    return filtered_two

def _extract_link(line):
    line = line[line.find("href=") + 6:]
    line = line[:line.find('"')]

    if line.startswith("http") and "self-service.kcl.ac.uk" not in line:
        return ""
    if "www" in line or "#" in line:
        return ""

    if line.startswith("https://") == False and line.startswith("http://") == False:
        if line.startswith("~"):
            return "https://self-service.kcl.ac.uk/" + line
        else:
            return "https://self-service.kcl.ac.uk" + line
    else:
        return line

_extract_link_vec = np.vectorize(_extract_link)

def extract_link(HTML_lines: np.array):
    if len(HTML_lines) == 0:
        return []
    candidate_lines = _extract_candidate_lines(HTML_lines)
    if len(candidate_lines) == 0:
        return []
    extracted_links = _extract_link_vec(candidate_lines)
    filter = "" != extracted_links
    return extracted_links[filter]

def save_as_json(DATA, filename):
    JSON_DATA = json.dumps(DATA)
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, "x") as file:
        file.writelines(JSON_DATA)

def scrape_website(STARTING_URL, K, SLEEP_TIMER): 
    link_queue = [STARTING_URL]
    link_queue_depth = [0]
    links_already_visited = {STARTING_URL}
    DATA_DICT = {}
    
    last_url = ""

    while len(link_queue) > 0:
        link = link_queue.pop(0)
        depth = link_queue_depth.pop(0)

        page = {"Parent_URL": last_url}
        page += {"URL": link}
        last_url = link

        HTML = download_website(link)
        HTML_lines = np.array(HTML.splitlines())
        print(f"{depth} | URL: {link}")
        extracted_links = extract_link(HTML_lines)
        for l in extracted_links:
            if depth < K:
                if l not in links_already_visited:
                    link_queue.append(l)
                    link_queue_depth.append(depth + 1)
                    links_already_visited.add(l)
        time.sleep(SLEEP_TIMER)

    print(f"Visited: {links_already_visited}")
    print(f"Last URL: {link}")
    return DATA_DICT

data = scrape_website("https://self-service.kcl.ac.uk", 1, 0.0)
save_as_json(data, "webdata.json")