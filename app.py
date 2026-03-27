import argparse
import requests
from pathlib import Path
from math import ceil

# Parse url from input user
def parse_url(url):
    # Remove protocol
    url = url.removeprefix("https://")
    # Split url into array
    url = url.split("/")

    # Check domain url
    if url[0] not in {"gamebanana.com", "www.gamebanana.com"}:
        raise ValueError("URL must use the gamebanana.com domain")
    
    # Check if url contain type and id
    if len(url) < 2:
        raise ValueError("URL must include a content type and ID, such as /mods/123")

    type_url = url[1]
    id_url = url[2]
    return type_url, id_url

# Get all url image from mods
def get_url_preview_mod(id):
    url = f"https://gamebanana.com/apiv13/Mod/{id}/ProfilePage"
    imgs_url = {}

    # Get data from api gamebanana
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_mods = response.json()
    except requests.RequestException as error:
        print.error(error)

    # Get preview file name
    mods_name = data_mods.get("_sName")
    imgs_data = data_mods.get("_aPreviewContent").get("screenshots")

    img_data = {
        "name": mods_name,
        "url_preview": []
    }
    for index, url in enumerate(imgs_data):
        base_url = "https://images.gamebanana.com/img/ss/mods"
        img_data["url_preview"].append(f"{base_url}/{url.get("_sFile")}")

    imgs_url[len(imgs_url)] = img_data.copy()
    return imgs_url

# Get all url image from user mod upload
def get_all_url_preview_mod_user(id):
    # User v11 api because because the api still provides 
    # all the preview images for the mod
    base_url = f"https://gamebanana.com/apiv11/Member/{id}/SubFeed"
    imgs_url = {}

    # Get data user from api
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        data_user = response.json()
    except requests.RequestException as error:
        print.error(error)

    # Get information about user
    total_mods = data_user.get("_aMetadata").get("_nRecordCount")
    per_pages = 10
    total_pages = ceil(total_mods / per_pages)

    # Looping based on total_pages
    for index in range(total_pages):
        url = f"{base_url}?_nPage={index+1}&_nPerpage={per_pages}"

        # Get data per page from api
        try:
            response = requests.get(url)
            response.raise_for_status()
            data_mod_per_page = response.json().get("_aRecords")
        except requests.RequestException as error:
            print.error(error)

        # Looping based on mod per page
        for data_mod in data_mod_per_page:
            # Get preview file name
            mods_name = data_mod.get("_sName")
            imgs_data = data_mod.get("_aPreviewMedia").get("_aImages")

            img_data = {
                "name": mods_name,
                "url_preview": []
            }

            # Add url preview mod to object img_data
            for url in imgs_data:
                base_img_url = "https://images.gamebanana.com/img/ss/mods"
                img_data["url_preview"].append(f"{base_img_url}/{url.get("_sFile")}")

            imgs_url[len(imgs_url)] = img_data.copy()

    return imgs_url


# Download file from url
def download_file(url, filename):
    with requests.get(url, stream=True, timeout=30) as response:
        response.raise_for_status() # Stop if return error
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        bar_width = 30

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if not chunk:
                    continue

                file.write(chunk)
                downloaded += len(chunk)

                if total_size:
                    percent = downloaded / total_size
                    filled = int(bar_width * percent)
                    bar = "#" * filled + "-" * (bar_width - filled)

                    print(f"\r{filename.split("/")[-1]} [{bar}] {percent:.0%}", end="", flush=True)
            print("")

def main():
    imgs_url = {}
    parse = argparse.ArgumentParser()
    parse.add_argument("url", help="A Gamebanana URL, such as https://gamebanana.com/mods/123")
    args = parse.parse_args()
    
    try:
        type_url, id_url = parse_url(args.url)
    except ValueError as error:
        parse.error(str(error))

    if type_url == "mods":
        imgs_url = get_url_preview_mod(id_url)
    elif type_url == "members":
        imgs_url = get_all_url_preview_mod_user(id_url)
    else:
        parse.error("Input URL not valid")

    # Create folder
    folder = Path("gamebanana")
    folder.mkdir(exist_ok=True)

    # Download all image mod
    for index in range(len(imgs_url)):
        img_url = imgs_url[index]
        name_mod = img_url.get("name")
        folder_mod = Path(f"{folder}/{name_mod}")
        folder_mod.mkdir(exist_ok=True)

        print(f"Name Mod: {name_mod}")
        for url in img_url.get("url_preview", []):
            filename = f"{folder_mod}/{url.split("/")[-1]}"

            download_file(url, filename)

if __name__ == "__main__":
    main()
