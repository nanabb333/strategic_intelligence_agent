# Localization Design

V4.5 adds deterministic localization for the user experience layer. The core analysis workflow remains unchanged.

## Design Choices

- Locale strings live in `locales/en.json`, `locales/zh-CN.json`, and `locales/zh-TW.json`.
- Dashboard labels are localized through static browser-side mappings for file-based local demo compatibility.
- Generated file outputs are adapted through `src/output_adapter.py`.
- No external translation APIs are used.

## Scope

Localization covers app title, paste and upload instructions, guided question labels, output modes, section headings, disclaimers, buttons, example prompts, and error text.

## Limitations

The output adapter uses deterministic templates. It localizes framing, headings, disclaimers, and selected summary structure; it does not perform free-form machine translation of every retrieved evidence item.
