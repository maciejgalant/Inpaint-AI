# Contributing

Contributions, bug reports and focused feature proposals are welcome.

## Issues

Use the GitHub issue tracker:

https://github.com/maciejgalant/Inpaint-AI/issues

Please include:

- QGIS version,
- operating system,
- Inpaint AI version,
- steps to reproduce,
- relevant QGIS log/traceback,
- expected and actual behavior.

Do **not** include OpenAI API keys or authentication secrets.

## Development checks

Before opening a pull request run:

```bash
python scripts/validate_plugin.py
python scripts/build_plugin_zip.py
```

Then test installation from the generated `dist/InpaintAI.zip`.

## Scope

Changes should preserve:

- QGIS Authentication Manager for credentials,
- `QgsNetworkAccessManager` for network access,
- explicit user consent before transmitting image data,
- PL/EN interface support,
- QGIS 4 compatibility.
