# Inpaint AI Cloud — User Guide

## 1. Purpose

Inpaint AI Cloud provides generative orthophoto editing directly inside QGIS.
The user selects a polygon, describes the requested modification, and the plugin:
1. renders an image crop and mask,
2. sends them to OpenAI Image Edit,
3. receives the generated image,
4. georeferences the result,
5. adds it to the QGIS project as a raster layer.

The plugin is specialized for orthophoto editing. A hidden technical orthophoto prompt is
automatically added to the user's instruction to improve matching of color, exposure, texture,
shadows, object scale and source-image character.

## 2. Requirements

- QGIS 4.x,
- internet access,
- an OpenAI API account with active billing,
- an OpenAI API key,
- QGIS Authentication Manager configured.

ChatGPT subscriptions and OpenAI API billing are separate.

## 3. Initial OpenAI setup

1. Create an API key in OpenAI Platform.
2. Open **Settings** in Inpaint AI.
3. In the OpenAI section click **Configure OpenAI connection…**.
4. Create or select a QGIS **API Header** authentication configuration.
5. Set:
   - header: `Authorization`
   - value: `Bearer YOUR_API_KEY`
6. Save the configuration.

The API key is not stored in the plugin source code. It is stored by QGIS Authentication Manager.

Never put the API key in a prompt or publish a screenshot containing the key.

## 4. Basic workflow

### Step 1 — Area
Click **Select area on map**.

- LMB — add polygon vertices,
- RMB — finish the polygon.

The selection remains visible until:
- generation finishes,
- **Undo selection** is pressed,
- **Cancel** is pressed.

### Step 2 — What to generate?
Choose a preset or write your own instruction.

The plugin automatically adds technical orthophoto constraints, so you do not need to repeat
phrases such as “match colors”, “top-down view” or “preserve orthophoto appearance”.

### Step 3 — Generation
Accept sending the crop and mask to OpenAI and press **GENERATE**.

The returned image is georeferenced and added to QGIS as a GeoTIFF layer.

## 5. Advanced options

### Model
**Sunburst** — preferred for more precise image editing and inpainting.

**Flare** — faster option for simpler tests.

### Quality
Higher quality can increase generation time and cost.

Recommended for testing:
- `medium`,
- `high`.

### Context
Controls how much surrounding imagery is sent as visual reference.

Default: `2.0×`.

### Matching
**Strict** — prioritizes seamless matching to the source orthophoto.

**Balanced** — compromise between source matching and reconstruction freedom.

**Creative** — more freedom while retaining aerial perspective and photorealism.

For normal orthophoto work, **Strict** is recommended.

## 6. Language

The plugin supports:
- Polski,
- English.

Language can be changed in **Settings** and is remembered.

## 7. Data sent to OpenAI

For each generation the plugin sends:
- the rendered image crop,
- the selection mask,
- the final text instruction,
- model/quality parameters required for the request.

The plugin does not store the API key in its source code.

## 8. Temporary files

Working crops, masks and generated images are placed in the operating system's temporary directory
under `InpaintAICloud`.

## 9. Troubleshooting

### HTTP 401
Usually means the Authorization header is missing or incorrect.
Check the QGIS API Header authentication configuration.

### The result does not match source colors
Try:
- **Strict** matching,
- a larger context,
- a shorter instruction,
- a more appropriate preset.

### Selection remains visible
Use **Undo selection** or start a new selection.
Alpha 4.1 additionally removes the selection overlay from the canvas after successful generation.

## 10. Important

Generated imagery is synthetic and should not be presented as original survey or archival imagery
without clear disclosure.
