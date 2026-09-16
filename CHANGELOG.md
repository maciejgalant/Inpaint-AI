# Changelog

All notable changes to Inpaint AI Cloud are documented here.

## 1.0.0-rc1 — 2026-09-16

- Prepared the first public release candidate from the tested Alpha 4.5 codebase.
- Updated QGIS plugin metadata and publication links.
- Finalized repository and in-package README files.
- Added release notes and completed the MIT license text.
- Kept the working image-generation backend unchanged.
- Confirmed the PL/EN interface, orthophoto prompts, output-folder workflow, georeferenced output, authentication flow, explicit consent and extended request timeouts from Alpha 4.5.
- Added release validation for archive structure, unwanted files and likely secrets.

## 2.0.0-alpha4.5 — 2026-09-15

- Added configurable persistent output folder.
- Added Browse/Open output-folder controls.
- Added per-generation subfolders containing input, mask, PNG result and georeferenced GeoTIFF.
- Preserved longer request timeout for high-cost quality modes.
- Preserved scrollable UI for smaller screens.
- Kept PL/EN interface, help dialog, cost estimate and session-cost counter.
- Improved selection cleanup and OpenAI/QGIS authentication workflow.

## 2.0.0-alpha4.4

- Increased request timeout for long-running `xhigh`/`max` image edits.

## 2.0.0-alpha4.3

- Added scrollable panel support.
- Hardened QObject parenting for the OpenAI network client.

## 2.0.0-alpha4.2

- Added help dialog and estimated/session cost display.
- Improved visual hierarchy of the panel.

## 2.0.0-alpha4.1

- Improved selection overlay cleanup.
- Moved language and OpenAI setup to Settings.
- Added privacy and user documentation.

## 2.0.0-alpha4

- Added Polish/English UI.
- Added orthophoto-specific hidden prompting.
- Expanded GIS/orthophoto presets.
- Added Strict/Balanced/Creative matching modes.
