from PySide6.QtCore import QPoint, QSize, QRect, qVersion, Qt, Signal, Slot
from PySide6.QtGui import QPolygon, QPen, QBrush, QPixmap, QPalette, QPainterPath, QPainter, QResizeEvent, QColor, \
    QColorConstants
from PySide6.QtWidgets import QWidget

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable


class GrapherWidget(QWidget):
    newFrame = Signal(DrawableScene)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = DrawableScene([])

        self.pen = QPen()
        self.brush = QBrush()
        self.brush.setColor(QColorConstants.Black)
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

        self.newFrame.connect(self.onNewFrame)

    def minimumSizeHint(self):
        return QSize(100, 100)

    def sizeHint(self):
        return QSize(400, 200)

    def resizeEvent(self, event: QResizeEvent):
        InitializationSignals.grapherParameters.emit(event.size().width(), event.size().height())

    @Slot()
    def onNewFrame(self, drawableScene: DrawableScene):
        self.scene = drawableScene
        MAIN_LOGGER.debug(self.scene)
        self.update()

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.setRenderHint(QPainter.Antialiasing)

            for point in self.scene.allDrawables:
                if isinstance(point, PointDrawable):
                    painter.drawEllipse(point.x, point.y, 5, 5)
                    # TODO add identifier

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))
