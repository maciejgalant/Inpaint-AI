# Security Policy

## Reporting a vulnerability

Please do not publish API keys, authentication secrets or sensitive image data in a public GitHub issue.

For security-sensitive reports contact:

**Maciej Galant** — `magal.pl@wp.pl`

For non-sensitive bugs and feature requests use:

https://github.com/maciejgalant/Inpaint-AI/issues

## Credential handling

Inpaint AI is designed to store the OpenAI API credential through QGIS Authentication Manager. API keys must not be hardcoded into the source tree, documentation, screenshots, issue reports or test fixtures.

## External network service

The plugin uses the OpenAI Image Edit API. Image crops, masks and prompts are transmitted only after user consent.
