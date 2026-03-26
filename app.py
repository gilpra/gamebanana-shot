import argparse

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

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("url", help="A Gamebanana URL, such as https://gamebanana.com/mods/123")
    args = parse.parse_args()
    
    try:
        type_url, id_url = parse_url(args.url)
    except ValueError as error:
        parse.error(str(error))

    if type_url == "mods":
        print("run func for mods")
    elif type_url == "members":
        print("run func for members")
    else:
        parse.error("Input URL not valid")

if __name__ == "__main__":
    main()
