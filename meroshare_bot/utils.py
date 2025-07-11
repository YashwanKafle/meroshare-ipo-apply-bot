import csv

from meroshare_bot.models import Account


def get_accounts(path: str):
    accounts: list[Account] = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = Account(
                name=row["Name"],
                capital_id=row["CapitalID"],
                username=row["Username"],
                password=row["Password"],
                quantity=row["Quantity"],
                crn_number=row["crn_number"],
            )
            accounts.append(a)
    return accounts
