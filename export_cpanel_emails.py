import csv
import os
import sys
from urllib.parse import urljoin

import requests


CPANEL_HOST = os.getenv("CPANEL_HOST", "abc.com")
CPANEL_PORT = int(os.getenv("CPANEL_PORT", "2083"))

CPANEL_USERNAME = os.getenv("CPANEL_USERNAME")
CPANEL_TOKEN = os.getenv("CPANEL_TOKEN")

OUTPUT_CSV = os.getenv("OUTPUT_CSV", "cpanel_email_accounts.csv")


def require_env(name: str, value: str | None) -> str:
    if not value:
        print(f"Missing environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def cpanel_get(module: str, function: str, params: dict | None = None) -> dict:
    username = require_env("CPANEL_USERNAME", CPANEL_USERNAME)
    token = require_env("CPANEL_TOKEN", CPANEL_TOKEN)

    base_url = f"https://{CPANEL_HOST}:{CPANEL_PORT}/execute/"
    url = urljoin(base_url, f"{module}/{function}")

    headers = {
        "Authorization": f"cpanel {username}:{token}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, params=params or {}, timeout=30)
    response.raise_for_status()
    return response.json()


def normalise_email_account(row: dict) -> dict:
    return {
        "email": row.get("email") or row.get("login") or "",
        "domain": row.get("domain") or "",
        "user": row.get("user") or "",
        "diskused": row.get("diskused") or row.get("humandiskused") or "",
        "diskquota": row.get("diskquota") or row.get("humandiskquota") or "",
        "suspended_incoming": row.get("suspended_incoming") or "",
        "suspended_login": row.get("suspended_login") or "",
        "mtime": row.get("mtime") or "",
    }


def export_email_accounts() -> None:
    result = cpanel_get("Email", "list_pops_with_disk")

    if result.get("status") != 1:
        errors = result.get("errors") or result.get("messages") or result
        raise RuntimeError(f"cPanel API error: {errors}")

    rows = [normalise_email_account(item) for item in result.get("data", [])]

    fieldnames = [
        "email",
        "domain",
        "user",
        "diskused",
        "diskquota",
        "suspended_incoming",
        "suspended_login",
        "mtime",
    ]

    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Exported {len(rows)} email accounts to {OUTPUT_CSV}")


if __name__ == "__main__":
    export_email_accounts()