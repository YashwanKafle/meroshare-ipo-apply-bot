import csv

from meroshare_bot.models import Account


def get_accounts(path: str):
    accounts: list[Account] = []
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            a = Account(
                name=row["name"],
                capital_id=row["capital_id"],
                username=row["username"],
                password=row["password"],
                quantity=row["quantity"],
                crn_number=row["crn_number"],
                bank=row["bank"],
                transcation_pin=row["transcation_pin"],
            )
            accounts.append(a)
    return accounts
