from pathlib import Path

from qgis.PyQt.QtCore import QSize, Qt, QPointF
from qgis.PyQt.QtGui import QImage, QPainter, QColor, QPolygonF
from qgis.core import QgsMapSettings, QgsMapRendererParallelJob, QgsRectangle


def render_crop(canvas, geometry, output_png, mask_png, resolution=1024, context=2.0):
    bbox = geometry.boundingBox()
    side = max(bbox.width(), bbox.height()) * float(context)
    cx = (bbox.xMinimum() + bbox.xMaximum()) / 2.0
    cy = (bbox.yMinimum() + bbox.yMaximum()) / 2.0
    extent = QgsRectangle(cx - side/2, cy - side/2, cx + side/2, cy + side/2)

    settings = QgsMapSettings()
    settings.setLayers(canvas.layers())
    settings.setBackgroundColor(QColor(255, 255, 255))
    settings.setOutputSize(QSize(resolution, resolution))
    settings.setExtent(extent)
    settings.setDestinationCrs(canvas.mapSettings().destinationCrs())

    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    image = job.renderedImage()
    if image.isNull():
        raise RuntimeError("Nie udało się wyrenderować fragmentu mapy.")
    if not image.save(str(output_png), "PNG"):
        raise RuntimeError("Nie udało się zapisać cropu PNG.")

    mask = QImage(resolution, resolution, QImage.Format.Format_ARGB32)
    mask.fill(QColor(255, 255, 255, 255))  # opaque = zachowaj

    ring = geometry.asPolygon()[0]
    poly = QPolygonF([
        QPointF(
            (p.x() - extent.xMinimum()) / extent.width() * resolution,
            (extent.yMaximum() - p.y()) / extent.height() * resolution
        )
        for p in ring
    ])

    painter = QPainter(mask)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
    painter.setBrush(QColor(0, 0, 0, 0))  # transparent = edytuj
    painter.drawPolygon(poly)
    painter.end()

    if not mask.save(str(mask_png), "PNG"):
        raise RuntimeError("Nie udało się zapisać maski PNG.")

    return extent


def georeference_png_to_tiff(png_path, tiff_path, extent, crs):
    try:
        from osgeo import gdal
    except Exception as exc:
        raise RuntimeError(f"Brak GDAL w środowisku QGIS: {exc}")

    src = gdal.Open(str(png_path))
    if src is None:
        raise RuntimeError("Nie można otworzyć wygenerowanego PNG.")

    width = src.RasterXSize
    height = src.RasterYSize

    pixel_w = extent.width() / width
    pixel_h = extent.height() / height

    driver = gdal.GetDriverByName("GTiff")
    dst = driver.CreateCopy(
        str(tiff_path),
        src,
        strict=0,
        options=["TILED=YES", "COMPRESS=DEFLATE"]
    )
    if dst is None:
        raise RuntimeError("Nie udało się utworzyć GeoTIFF.")

    dst.SetGeoTransform([
        extent.xMinimum(), pixel_w, 0.0,
        extent.yMaximum(), 0.0, -pixel_h
    ])
    dst.SetProjection(crs.toWkt())
    dst.FlushCache()
    dst = None
    src = None
