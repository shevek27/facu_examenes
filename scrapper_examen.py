# create folders/write files
import os
# urls and html
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# convert from .gif to png
from PIL import Image
from io import BytesIO

# tips: [url].asp .gif images are actually in [url]/[filename].gif . we have to remove the .asp

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


# exams are images in .gif format
def get_exam_image_url(asp_link):
    try:
        response = requests.get(asp_link)
        soup = BeautifulSoup(response.text, "html.parser")
        for img in soup.find_all("img", src=True):                
            image_link_list = img["src"].split('/')
            if len(image_link_list) > 1:
                image_link = image_link_list[1]
            else:
                image_link = image_link_list[0]
            print(image_link)
            if image_link.lower().endswith(".gif"):
                asp_link = asp_link.replace(".asp", "")
                full_url = asp_link + "/" + image_link
                #print(f"asp_link={asp_link}, image_link= {image_link}, full_url = {full_url}")
                return full_url

    except Exception as e:
        print(f"error with file {asp_link}, error= {e}")


def download_image_as_jpg(image_url, save_folder, save_as="jpg", quality=100):
    filename = image_url
    name_without_extension = os.path.splitext(filename)[0]
    name_with_desired_extension = f"{name_without_extension}.{save_as}"
    save_path = os.path.join(save_folder, name_with_desired_extension)
    if os.path.exists(save_path):
        print("image already exists!")
        return

    else:   
        try:
            response = requests.get(image_url, stream=True)

            # data to Pillow
            img = Image.open(BytesIO(response.content))
            # convert to RGB (.GIF uses 'P' palette mode)
            if save_as.lower() != "gif":
                if img.mode in ("RGBA", 'P'):
                    img = img.convert("RGB")

                save_options = {}   

                if save_as.lower() == "jpg":
                    save_options["quality"] = quality
                    img.save(save_path, format="JPEG", quality=quality)
                print("no error here")

        except Exception as e:
            print(f"error! {e}")


def save_as_asp(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # save as HTML 
        base_name = os.path.bas(url)

    except Exception as e:
        print(f"error! {e}")
        return



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
        full_exam_url = get_exam_image_url(link)
        download_image_as_jpg(full_exam_url, save_path)

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
