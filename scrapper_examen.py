import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_asp_links(url):

    # response -> soup object
    response = requests.get(url)
    # check for errors (404,403,etc)
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'html.parser')
    
    asp_links = []
    for link in soup.find_all('a', href=True):
        href_link = link['href']
        lower_href_link = href_link.lower()
        if lower_href_link.endswith('.asp'):
            if "index" not in lower_href_link:
            # convert incomplete urls to full ones, urljoin is smart
                full_url = urljoin(url, href_link)
                if "Examenes" in full_url:
                    asp_links.append(full_url)
    
    return asp_links

target_url = "https://www.altillo.com/Examenes/uba/exactas/index.asp"
links = get_asp_links(target_url)

for index, link in enumerate(links, 1):
    print(f"{index}. {link}")

print(f"se encontraron {len(links)} examenes!")