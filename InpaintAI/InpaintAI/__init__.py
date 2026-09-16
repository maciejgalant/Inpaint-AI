def classFactory(iface):
    from .plugin import InpaintAIPlugin
    return InpaintAIPlugin(iface)
