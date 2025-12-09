# Security Policy

## Reporting a Vulnerability
- Please email security@trendnest.example.com (replace with your security contact).
- Include a description, steps to reproduce, and any relevant logs or trace IDs.

## Handling Secrets
- Do not commit secrets. Use `.env.example` as a template and keep `.env` out of git.
- Prefer cloud secret storage (e.g., GCP Secret Manager) and short-lived credentials.

## Dependencies
- Run `pip install -r requirements.txt` regularly and keep CI green.
- Use the included CI workflow to catch regressions and basic security scans when added.
