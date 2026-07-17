# Security

Strategic Intelligence Decision Companion is a local-first product. It is not designed as an internet-facing production service.

## Supported Use

Start the local app with the double-click launchers under `launch/`, or run:

```bash
./run_app.sh
python3 launch.py
```

The launcher binds to loopback by default and opens at:

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

Reviewer-supplied URLs are limited to public HTTP(S) targets. Localhost, private, loopback, link-local, multicast, reserved, unspecified, and common cloud-metadata targets are blocked before retrieval and after redirects. Responses are read in bounded chunks and stopped once the configured byte limit is exceeded, regardless of missing or inaccurate `Content-Length` metadata.

DNS rebinding is not completely prevented because validation lookup and socket connection are not pinned to the same resolved address. Hostile public servers and parser-level attacks also remain reasons to treat URL retrieval as untrusted input.

## Reporting Issues

For portfolio review, document security concerns as issues or pull request comments. Do not include private credentials, tokens, internal documents, or sensitive source material in public issues.
