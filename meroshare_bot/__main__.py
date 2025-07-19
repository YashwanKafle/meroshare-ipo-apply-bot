from argparse import ArgumentParser

from meroshare_bot.playwright import Playwright
from meroshare_bot.utils import get_accounts


def main(csv_file_path: str, apply_all: bool):
    accounts = get_accounts(csv_file_path)
    for account in accounts:
        playwright = Playwright(account, apply_all)
        playwright.launch_playwright()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--csv-file-path", "-f", required=True)
    parser.add_argument(
        "--apply-all",
        action="store_true",
        help="Apply all issues (bonds,ordinary shares,mutual funds)",
    )
    args = parser.parse_args()
    main(args.csv_file_path, args.apply_all)
