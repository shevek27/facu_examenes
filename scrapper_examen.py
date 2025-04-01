# create folders/write files
import os
# urls and html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_asp_links(url):

    # response -> soup object
    response = requests.get(url)
    # git
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


def get_save_path(link):
    components = link.split('/')
    # uba url example: https://www.altillo.com/Examenes/uba/exactas/algebra/alg_2015_2pb.asp
    # normal url example: https://www.altillo.com/Examenes/unlp/logica/log_2015_2pa.asp
    exam_name = components[-1]
    materia = components[-2]
    facultad = components[-3]
    uba = ""
    if components[-4] == "uba":
        uba = "uba"
    

    save_path = os.path.join(uba, facultad, materia)
    
    return save_path



def write_exams(links, save_path):
    # create folder

    os.makedirs(save_path, exist_ok=True)
    
    # write each exam
    for link in links:
        components = link.split('/')
        exam_name = components[-1]
        response = requests.get(link)
        full_path = os.path.join(save_path, exam_name)
        with open(full_path, "wb") as exam_file:
            exam_file.write(response.content)
        print(f"downloaded exam: {exam_name}")


def main():
    target_url = "https://www.altillo.com/Examenes/uba/exactas/index.asp"
    links = get_asp_links(target_url)

    for index, link in enumerate(links, 1):
        print(f"{index}. {link}")

    print(f"se encontraron {len(links)} examenes!")
    print("wtf")
    save_path = get_save_path(links[0])
    write_exams(links, save_path)

    


if __name__ == "__main__":
    main()
