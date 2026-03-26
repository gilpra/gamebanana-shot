import argparse

def main():
    parse = argparse.ArgumentParser()
    parse.add_argument("url", help="A GameBanana URL, such as https://gamebanana.com/mods/123")
    args = parse.parse_args()

if __name__ == "__main__":
    main()
