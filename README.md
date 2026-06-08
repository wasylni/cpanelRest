## Run with variables populated

You can run the script in two ways:

1. By setting environment variables before running the script.
2. By editing the Python file and hardcoding the variables directly.

The safer option is to use environment variables.

---

## Option 1: Run with environment variables

### Windows PowerShell

```powershell
$env:CPANEL_HOST="abc.com"
$env:CPANEL_PORT="2083"
$env:CPANEL_USERNAME="your_cpanel_username"
$env:CPANEL_TOKEN="your_api_token"
$env:OUTPUT_CSV="cpanel_email_accounts.csv"

python export_cpanel_emails.py