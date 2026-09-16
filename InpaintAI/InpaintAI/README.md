# Inpaint AI Cloud

Inpaint AI Cloud is an experimental QGIS 4 plugin for generative editing of orthophotos using OpenAI Image Edit.

## Main features

- polygon-based image inpainting directly from the QGIS map canvas,
- georeferenced GeoTIFF output added back to the current QGIS project,
- Polish and English interface,
- specialized hidden orthophoto prompt for source-image matching,
- presets for urban, transport, vegetation, agricultural and reconstruction tasks,
- Strict / Balanced / Creative source-matching modes,
- Sunburst / Flare image model selection and multiple quality levels,
- OpenAI credentials stored through QGIS Authentication Manager,
- explicit user consent before sending the image crop and mask,
- configurable output folder,
- timestamped generation folders containing `input.png`, `mask.png`, `result.png` and `result.tif`,
- extended timeout support for longer `xhigh` / `max` generations,
- scrollable interface for smaller screens.

## Documentation

- `INSTRUKCJA_PL.md` — instrukcja po polsku,
- `USER_GUIDE_EN.md` — English user guide,
- `PRIVACY.md` — external-processing and privacy information,
- `REPO_CHECKLIST_PL.md` — preparation checklist for the official QGIS Plugin Repository.

## Version

1.0.0-rc1 — first public release candidate, based on the tested Alpha 4.5 code without functional backend changes.

## Repository

- Source: https://github.com/maciejgalant/Inpaint-AI
- Issues: https://github.com/maciejgalant/Inpaint-AI/issues

## Author

Maciej Galant — `magal.pl@wp.pl`

## Security

Do not hardcode an OpenAI API key in the plugin.
Use QGIS Authentication Manager with an API Header configuration:

`Authorization: Bearer YOUR_API_KEY`

## Output folder

The plugin lets the user select a persistent output folder. Each generation is stored in its own timestamped subfolder containing `input.png`, `mask.png`, `result.png` and georeferenced `result.tif`. If no folder is selected, the plugin defaults to `<QGIS project folder>/InpaintAI_Output` or the user's Documents folder when the project has not been saved yet.

## License

See `LICENSE`.
