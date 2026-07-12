# Security

- No secrets are committed to source control.
- The OpenAI API key is stored in Secrets Manager and never exposed to the browser.
- Cognito JWTs are required for protected routes.
- Admin mutations are enforced in Lambda.
- Sensitive borrower data is limited to non-sensitive scenario fields only.
