# Security

Strategic Intelligence Agent is currently a local development application. It is not designed as an internet-facing production service.

## Supported Use

Run the app locally:

```bash
python3 -m uvicorn app:app --reload
```

The dashboard is intended for local use at:

```text
http://127.0.0.1:8000/dashboard/
```

## Security Limitations

The current repository does not include:

- Authentication.
- Authorization.
- Multi-user access control.
- Production hardening for public internet deployment.
- Secrets management.
- Rate limiting.
- Audit logging.

Do not deploy this app publicly without a separate production security review.

## Reporting Issues

For portfolio review, document security concerns as issues or pull request comments. Do not include private credentials, tokens, internal documents, or sensitive source material in public issues.
