from argparse import ArgumentParser

from meroshare_bot.playwright import Playwright
from meroshare_bot.utils import get_accounts


def main(csv_file_path: str):
    accounts = get_accounts(csv_file_path)
    for account in accounts:
        playwright = Playwright(account)
        playwright.launch_playwright()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--csv-file-path", required=True)
    args = parser.parse_args()
    main(args.csv_file_path)
