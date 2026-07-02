# Security

Strategic Intelligence Decision Companion is a local-first product. It is not designed as an internet-facing production service.

## Supported Use

Start the local app with the double-click launchers under `launch/`, or run:

```bash
./run_app.sh
python3 launch.py
```

The local product opens at:

```text
http://localhost:8000
```

## Security Limitations

The current repository does not include:

- Authentication.
- Authorization.
- Multi-user access control.
- Production hardening for public internet deployment.
- Secrets management.
- Rate limiting.
- Hosted audit logging.

Do not deploy this app publicly without a separate production security review.

## Local Trust Boundary

The app runs on the user's computer and stores local artifacts in repository folders such as `data/projects/` and `outputs/runs/`.

Evidence retrieval is user-triggered. The product does not perform autonomous browsing, background monitoring, or cloud hosting.

## Reporting Issues

For portfolio review, document security concerns as issues or pull request comments. Do not include private credentials, tokens, internal documents, or sensitive source material in public issues.
