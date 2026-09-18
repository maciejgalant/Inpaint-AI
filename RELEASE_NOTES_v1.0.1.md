# Inpaint AI v1.0.1

This is the first stable public release of Inpaint AI for QGIS 4. It is promoted from the fully tested `1.0.0-rc1` build. The working image-generation backend has not been changed for this stable release.

## Highlights

- Polygon-based generative editing of orthophotos in QGIS.
- Polish and English interface.
- Orthophoto-specific hidden prompts and Strict, Balanced and Creative matching modes.
- Presets for urban, transport, vegetation, agriculture, recreation and reconstruction workflows.
- OpenAI credentials stored through QGIS Authentication Manager.
- Explicit consent before image crops, masks and prompts are sent to OpenAI.
- Persistent output-folder selection and per-generation folders.
- PNG intermediates and georeferenced GeoTIFF output automatically added to QGIS.
- Extended timeout support for `high`, `xhigh` and `max` generations.
- Scrollable interface for smaller screens.
- Estimated per-image and session cost display.
- Stable QGIS repository metadata with `experimental=False`.

## Requirements

- QGIS 4.x.
- Internet access.
- An OpenAI API account with active billing.
- An OpenAI API key configured as an API Header in QGIS Authentication Manager.

## Installation

Download `InpaintAI.zip` from the release assets. In QGIS, open the plugin manager, choose installation from ZIP, select the downloaded archive and restart QGIS if requested.

## Stable release status

Version `1.0.1` is marked as non-experimental in QGIS plugin metadata.

Issues can be reported at:
https://github.com/maciejgalant/Inpaint-AI/issues

## Privacy

After explicit consent, the selected image crop, mask and generated instruction are sent to the external OpenAI Image Edit service. The repository and plugin package contain no API key.
