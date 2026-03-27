import argparse
from os.path import exists
import requests
from pathlib import Path

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

    imgs_url = [{
        "name": mods_name,
        "url_preview": []
    }]
    for url in imgs_data:
        base_url = "https://images.gamebanana.com/img/ss/mods"
        imgs_url[0]["url_preview"].append(f"{base_url}/{url.get("_sFile")}")

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
        print("run func for members")
    else:
        parse.error("Input URL not valid")

    # Create folder
    folder = Path("gamebanana")
    folder.mkdir(exist_ok=True)

    # Download all image mod
    for img_url in imgs_url:
        name_mod = img_url.get("name")
        folder_mod = Path(f"{folder}/{name_mod}")
        folder_mod.mkdir(exist_ok=True)
        
        print(f"Name Mod: {name_mod}")
        for url in img_url.get("url_preview", []):
            filename = f"{folder_mod}/{url.split("/")[-1]}"

            download_file(url, filename)
        print("\n")


if __name__ == "__main__":
    main()
