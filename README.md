# MeroShare IPO Application Bot

A Python automation bot that uses Playwright to log in to [MeroShare](https://meroshare.cdsc.com.np) and apply for IPOs.

---

## Features

- Automated login to MeroShare
- Applies from multiple accounts via CSV input
- Supports all issue types: Ordinary Shares, Mutual Funds, Bonds

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/meroshare-bot.git
cd meroshare-bot
```

### 2. Set Up Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
playwright install 
```

### CSV Format
The bot reads account details from a CSV file. Each row should look like:
```bash
name,capital_id,username,password,quantity,crn_number,bank,transcation_pin
John,123,example_user,password123,10,123456,NABIL,1234
```
Bank name should be exact like: `NIC ASIA BANK LTD.`

### Usage
Run the bot:

```bash
python main.py -f accounts.csv [--apply-all]
```

| Flag                     | Description                                                                    |
| ------------------------ | ------------------------------------------------------------------------------ |
| `-f`                     | (Required) Path to the CSV file with account data                              |
| `--apply-all`            | (Optional) If set, applies for all issue types (default: only ordinary shares) |

### Examples
Apply only for ordinary shares:
```bash
python main.py -f accounts.csv
```
Apply for all available issues:
```bash
python main.py -f accounts.csv --apply-all
```


## How It Works

- Logs in to MeroShare using each account.
- Navigates to My ASBA.
- Detects active IPOs/funds/bonds.
- Applies based on `apply_all` flag.
- Fills form: bank, account number, CRN, quantity, transaction PIN.
- Submits application.


## Disclaimer

This project is intended for **personal and educational purposes only**.

- By using this tool, **you agree** that you are fully responsible for any consequences resulting from its use.
- Automating actions on the [MeroShare portal](https://meroshare.cdsc.com.np) **may violate its terms of service**. Use it **at your own risk**.
