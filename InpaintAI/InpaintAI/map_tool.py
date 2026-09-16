import logging

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsGeometry, QgsWkbTypes
from qgis.gui import QgsMapTool, QgsRubberBand


LOGGER = logging.getLogger(__name__)


class InpaintPolygonTool(QgsMapTool):
    def __init__(self, canvas, callback):
        super().__init__(canvas)
        self.canvas = canvas
        self.callback = callback
        self.points = []
        self.finished = False
        self.rubber = QgsRubberBand(
            canvas,
            QgsWkbTypes.GeometryType.PolygonGeometry
        )
        self.rubber.setStrokeColor(QColor(0, 210, 150, 235))
        self.rubber.setFillColor(QColor(0, 210, 150, 45))
        self.rubber.setWidth(2)

    def canvasPressEvent(self, event):
        if self.finished:
            return

        if event.button() == Qt.MouseButton.LeftButton:
            point = self.toMapCoordinates(event.pos())
            self.points.append(point)
            self.rubber.addPoint(point, True)

        elif (
            event.button() == Qt.MouseButton.RightButton
            and len(self.points) >= 3
        ):
            self.finished = True
            self.callback(QgsGeometry.fromPolygonXY([self.points]))

    def clear(self):
        """Clear the visible selection but keep the tool reusable."""
        if self.rubber is not None:
            try:
                self.rubber.reset(
                    QgsWkbTypes.GeometryType.PolygonGeometry
                )
                self.rubber.hide()
            except RuntimeError:
                LOGGER.debug("Rubber band was already deleted during clear", exc_info=True)

        self.points = []
        self.finished = False

        try:
            self.canvas.refresh()
        except Exception:
            LOGGER.debug("Map canvas refresh failed during clear", exc_info=True)

    def dispose(self):
        """Remove the rubber band from the map canvas completely."""
        rubber = self.rubber
        self.rubber = None

        if rubber is not None:
            try:
                rubber.reset(
                    QgsWkbTypes.GeometryType.PolygonGeometry
                )
            except RuntimeError:
                LOGGER.debug("Rubber band was already deleted during reset", exc_info=True)

            try:
                rubber.hide()
            except RuntimeError:
                LOGGER.debug("Rubber band was already deleted during hide", exc_info=True)

            try:
                scene = self.canvas.scene()
                if scene is not None:
                    scene.removeItem(rubber)
            except (RuntimeError, TypeError):
                LOGGER.debug("Rubber band could not be removed from the scene", exc_info=True)

            try:
                rubber.deleteLater()
            except (AttributeError, RuntimeError):
                LOGGER.debug("Rubber band was already scheduled for deletion", exc_info=True)

        self.points = []
        self.finished = False

        try:
            self.canvas.refresh()
        except Exception:
            LOGGER.debug("Map canvas refresh failed during disposal", exc_info=True)
