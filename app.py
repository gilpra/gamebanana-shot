import argparse
import requests

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
    url = f"https://gamebanana.com/apiv11/Mod/{id}/ProfilePage"

    # Get data from api gamebanana
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_mods = response.json()
    except requests.RequestException as error:
        print.error(error)

    # Get preview file name
    mods_name = data_mods.get("_sName")
    imgs_data = data_mods.get("_aPreviewMedia").get("_aImages")

    imgs_url = [{
        "name": mods_name,
        "url_preview": []
    }]
    for url in imgs_data:
        base_url = "https://images.gamebanana.com/img/ss/mods"
        imgs_url[0]["url_preview"].append(f"{base_url}/{url.get("_sFile")}")

    return imgs_url

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

if __name__ == "__main__":
    main()
