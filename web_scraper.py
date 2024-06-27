import requests
import numpy as np
import os
import time

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

def scrape_website(STARTING_URL, K, SLEEP_TIMER): 
    link_queue = [STARTING_URL]
    link_queue_depth = [0]
    links_already_visited = {STARTING_URL}

    while len(link_queue) > 0:
        LINK = link_queue.pop()
        DEPTH = link_queue_depth.pop()
        HTML = download_website(LINK)
        HTML_lines = np.array(HTML.splitlines())
        print(f"{DEPTH} | URL: {LINK}")
        extracted_links = extract_link(HTML_lines)
        for link in extracted_links:
            if DEPTH < K:
                if link not in links_already_visited:
                    link_queue.append(link)
                    link_queue_depth.append(DEPTH + 1)
                    links_already_visited.add(link)
        time.sleep(SLEEP_TIMER)
    print(f"Visited: {links_already_visited}")
    print(f"Last URL: {LINK}")

scrape_website("https://self-service.kcl.ac.uk", 1, 0.0)

c