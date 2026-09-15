# Privacy and external processing

Inpaint AI Cloud uses an external OpenAI image-editing service.

When the user starts a generation, the plugin sends:
- a rendered crop of the current QGIS map,
- a mask corresponding to the selected polygon,
- the generated text instruction,
- model and quality parameters required by the API.

The API key is stored through QGIS Authentication Manager and is not hardcoded into the plugin.

The plugin requires an explicit consent checkbox before transmitting the crop and mask.

Working images are written to the operating system temporary directory under `InpaintAICloud`.

Use of the external service is subject to the service provider's applicable API terms and data policies.
