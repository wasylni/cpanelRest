# cPanel Email Accounts CSV Exporter

This Python script connects to the cPanel UAPI and exports all email accounts from a cPanel account to a CSV file.

It uses this cPanel endpoint:

```text
https://CPANEL_HOST:2083/execute/Email/list_pops_with_disk