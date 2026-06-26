## Summary

Describe the change in 2-4 sentences.

## Type Of Change

- [ ] Documentation only
- [ ] Tests or CI only
- [ ] Behavior-preserving engineering change
- [ ] Product behavior change

## Behavior Impact

- [ ] No API routes changed
- [ ] No request or response schemas changed
- [ ] No analysis logic changed
- [ ] No unsupported capabilities were claimed

If any box is unchecked, explain why.

## Validation

Paste the commands run and results:

```bash
python3 -m ruff check .
python3 -m compileall app.py src tests
python3 -m pytest
```

## Documentation

- [ ] README updated if needed
- [ ] Product docs updated if needed
- [ ] Architecture/testing docs updated if needed
- [ ] Limitations remain clear
