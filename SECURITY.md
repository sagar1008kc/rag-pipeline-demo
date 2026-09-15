# Security Notes

This repository is a tutorial. It is not legal, compliance, privacy, or
security advice.

The Northline Trust Company corpus is fictional. Names, account numbers, phone
numbers, watch-book entries, issuers, and vendors are synthetic test fixtures.

Before publishing or opening a pull request:

- Do not commit `.env` or any real API key.
- Do not replace the synthetic corpus with real client, employee, deal, or
  security data.
- Do not paste live secrets into notebooks to test redaction.
- Treat generated `.data/` indexes as local cache only.

If you accidentally commit a key, revoke it at the provider and rotate it.
