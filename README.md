# MeroShare IPO Application Bot

A Python automation bot that uses Playwright to log in to [MeroShare](https://meroshare.cdsc.com.np) and apply for IPOs.

## Features

- Automated login to MeroShare
- Applies from multiple accounts via CSV input
- Supports all issue types: Ordinary Shares, Mutual Funds, Bonds

## Prerequisites

- Python 3.10 or higher
- A MeroShare account with valid credentials

## Setup Guide

### 1. Fork the Repository

Click the **Fork** button at the top-right corner of the [repository page](https://github.com/YashwanKafle/meroshare-ipo-apply-bot) to create your own copy.

### 2. Clone Your Fork

```bash
git clone https://github.com/<your-username>/meroshare-ipo-apply-bot.git
cd meroshare-ipo-apply-bot
```

### 3. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuration

### CSV Format

The bot reads account details from a CSV file. Create a file (e.g., `accounts.csv`) with the following format:

```csv
name,capital_id,username,password,quantity,crn_number,bank,transcation_pin
John,123,example_user,password123,10,123456,NABIL,1234
```

> **Note:** The bank name must match exactly as it appears on MeroShare (e.g., `NIC ASIA BANK LTD.`).

## Usage

```bash
python -m meroshare_bot -f accounts.csv [--apply-all]
```

| Flag          | Description                                                                    |
| ------------- | ------------------------------------------------------------------------------ |
| `-f`          | (Required) Path to the CSV file with account data                              |
| `--apply-all` | (Optional) If set, applies for all issue types (default: only ordinary shares) |

### Examples

Apply only for ordinary shares:

```bash
python -m meroshare_bot -f accounts.csv
```

Apply for all available issues:

```bash
python -m meroshare_bot -f accounts.csv --apply-all
```

## How It Works

1. Logs in to MeroShare using each account from the CSV file.
2. Navigates to **My ASBA**.
3. Detects active IPOs, mutual funds, and bonds.
4. Applies based on the `--apply-all` flag.
5. Fills the form with bank, account number, CRN, quantity, and transaction PIN.
6. Submits the application.

## Contributing

Contributions are welcome! Please read the [Contributing Guidelines](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

## License

This project is licensed under the [MIT License](LICENSE).

## Disclaimer

This project is intended for **personal and educational purposes only**.

- By using this tool, **you agree** that you are fully responsible for any consequences resulting from its use.
- Automating actions on the [MeroShare portal](https://meroshare.cdsc.com.np) **may violate its terms of service**. Use it **at your own risk**.

## Security

If you discover a security vulnerability, please report it responsibly. See [SECURITY.md](SECURITY.md) for details.
