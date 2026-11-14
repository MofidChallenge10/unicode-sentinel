# Unicode Sentinel

Scan source and text files for invisible Unicode formatting/control characters that can obscure code review or alter text display.

```bash
python -m pip install .
unicode-sentinel src/*.py
unicode-sentinel --json README.md
```

Reports line, column, code point, Unicode name and category. Tabs are allowed. This scanner detects selected invisible/control classes; it does not attempt broad homoglyph/confusable-language detection.

## Tests
```bash
python -m unittest discover -s tests -v
```

MIT License.
