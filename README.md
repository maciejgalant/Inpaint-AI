# Inpaint AI for QGIS

**Inpaint AI Cloud** is a QGIS 4 plugin for generative editing of orthophotos with the OpenAI Image Edit API. Version **1.0.0-rc1** is the first public release candidate, based on the functionally tested Alpha 4.5 code.

The plugin lets the user draw a polygon directly on the QGIS map canvas, describe the requested change, send the rendered crop and mask after explicit consent, receive the edited image, georeference the result and add it back to the current QGIS project.

## Current capabilities

- QGIS 4 / Qt 6 plugin.
- Polygon-based orthophoto inpainting.
- Polish and English interface.
- Orthophoto-specific hidden prompt for matching color, exposure, shadows, texture, scale and source-image character.
- Presets for urban development, transport, vegetation, agriculture, recreation and object removal/reconstruction.
- Strict / Balanced / Creative source-matching modes.
- GPT Image Sunburst and Flare model selection with multiple quality levels.
- OpenAI credentials stored through QGIS Authentication Manager.
- Explicit consent before sending an image crop and mask to the external API.
- Configurable persistent output directory.
- Per-generation folders containing input, mask, PNG result and georeferenced GeoTIFF.
- Georeferenced GeoTIFF result automatically added to QGIS.
- Scrollable UI for smaller screens.
- Estimated per-image and session cost display.

## Requirements

- QGIS 4.x
- Internet connection
- OpenAI API account with active API billing
- OpenAI API key configured in QGIS Authentication Manager as an API Header

The plugin does **not** bundle an API key and does not store an API key in its source code.

## OpenAI authentication

Create a QGIS Authentication configuration of type **API Header** and set:

```text
Authorization: Bearer YOUR_OPENAI_API_KEY
```

Then select that authentication configuration from the Inpaint AI settings window.

## Data sent to OpenAI

Only after explicit user consent, the plugin sends the external OpenAI image-edit service:

- the rendered QGIS crop,
- the polygon mask,
- the generated text instruction,
- required model and quality parameters.

See `InpaintAI/PRIVACY.md` for additional information.

## Development installation

Copy the `InpaintAI` directory to your QGIS profile plugin directory and restart QGIS, or build a plugin ZIP:

```bash
python scripts/build_plugin_zip.py
```

The generated QGIS installation package is:

```text
dist/InpaintAI.zip
```

## Validation

Run:

```bash
python scripts/validate_plugin.py
```

The repository also contains a GitHub Actions workflow which performs the same validation and builds the plugin package on pushes and pull requests.

## Documentation

- Polish guide: `InpaintAI/INSTRUKCJA_PL.md`
- English guide: `InpaintAI/USER_GUIDE_EN.md`
- Privacy information: `InpaintAI/PRIVACY.md`
- Changelog: `CHANGELOG.md`
- Publishing notes: `PUBLISHING.md`
- Security policy: `SECURITY.md`

## Project links

- Repository: https://github.com/maciejgalant/Inpaint-AI
- Issues: https://github.com/maciejgalant/Inpaint-AI/issues

## Author

**Maciej Galant**  
Contact: `magal.pl@wp.pl`

## Release status

Current version: **1.0.0-rc1**.

This is a release candidate. The plugin remains marked as `experimental=True` until the final repository review and broader platform testing are complete. No functional backend changes were introduced between the tested Alpha 4.5 build and this RC.

Release notes: `RELEASE_NOTES_v1.0.0-rc1.md`.

## License

MIT License. See `LICENSE`.
