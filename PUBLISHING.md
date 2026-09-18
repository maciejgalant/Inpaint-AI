# Publishing checklist — QGIS Plugin Repository

Repository prepared for:

- Repository: https://github.com/maciejgalant/Inpaint-AI
- Homepage: https://github.com/maciejgalant/Inpaint-AI
- Issues: https://github.com/maciejgalant/Inpaint-AI/issues
- Author: Maciej Galant
- Publication email: magal.pl@wp.pl

## Metadata already configured

`InpaintAI/metadata.txt` now contains:

- `email=magal.pl@wp.pl`
- `homepage=https://github.com/maciejgalant/Inpaint-AI`
- `repository=https://github.com/maciejgalant/Inpaint-AI`
- `tracker=https://github.com/maciejgalant/Inpaint-AI/issues`
- useful plugin tags
- `category=Raster`
- QGIS 4 compatibility declarations

## Before the first official QGIS Plugin Repository upload

1. Push this source tree to the public GitHub repository.
2. Confirm that the repository, README and Issues URLs work without authentication.
3. Confirm that `InpaintAI/metadata.txt` contains `version=1.0.1`.
4. Confirm `experimental=False` for the stable release.
5. Test at minimum on Windows with the exact intended QGIS 4 release.
6. If possible, test on Linux with QGIS 4 as well.
7. Test:
   - local raster input,
   - XYZ/WMS imagery,
   - a saved QGIS project,
   - an unsaved project,
   - custom output directory,
   - low/high/max image quality,
   - cancellation,
   - invalid API key,
   - no network connection.
8. Run `python scripts/validate_plugin.py`.
9. Run `python scripts/build_plugin_zip.py`.
10. Install and test the exact generated `dist/InpaintAI.zip`.
11. Create the Git tag and GitHub Release `v1.0.1`, using `RELEASE_NOTES_v1.0.1.md`.
12. Upload the exact tested ZIP to the QGIS Plugin Repository.
13. Review any automated security or metadata feedback from the QGIS repository.

## External-service disclosure

Documentation must continue to state that the plugin requires:

- an OpenAI API account,
- an OpenAI API key,
- active API billing,
- internet connectivity,
- transmission of the selected image crop, mask and prompt to the external OpenAI Image Edit service after explicit user consent.

The API key must remain stored through QGIS Authentication Manager and must never be hardcoded into repository files.
