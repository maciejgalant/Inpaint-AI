from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsGeometry, QgsWkbTypes
from qgis.gui import QgsMapTool, QgsRubberBand


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
                pass

        self.points = []
        self.finished = False

        try:
            self.canvas.refresh()
        except Exception:
            pass

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
                pass

            try:
                rubber.hide()
            except RuntimeError:
                pass

            try:
                scene = self.canvas.scene()
                if scene is not None:
                    scene.removeItem(rubber)
            except (RuntimeError, TypeError):
                pass

            try:
                rubber.deleteLater()
            except (AttributeError, RuntimeError):
                pass

        self.points = []
        self.finished = False

        try:
            self.canvas.refresh()
        except Exception:
            pass
