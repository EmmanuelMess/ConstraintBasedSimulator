from PySide6.QtCore import QSize, QRect, Qt, Signal, Slot, QObject
from PySide6.QtGui import QPen, QBrush, QPalette, QPainter, QResizeEvent, QColorConstants, QPaintEvent
from PySide6.QtWidgets import QWidget
from typing_extensions import Union

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable


class GrapherWidget(QWidget):
    """
    Grapher Qt Widget, view for the simulator (model-view-presenter pattern)
    """
    newFrame = Signal(DrawableScene)

    def __init__(self, parent:Union[QWidget, None]=None) -> None:
        super().__init__(parent)

        self.scene = DrawableScene([])

        self.pen = QPen()
        self.brush = QBrush()
        self.brush.setColor(QColorConstants.Black)  # type: ignore[attr-defined]
        self.brush.setStyle(Qt.BrushStyle.SolidPattern)

        self.setBackgroundRole(QPalette.Base)  # type: ignore[attr-defined]
        self.setAutoFillBackground(True)

        self.newFrame.connect(self.onNewFrame)

    def minimumSizeHint(self) -> QSize:
        return QSize(100, 100)

    def sizeHint(self) -> QSize:
        return QSize(400, 200)

    def resizeEvent(self, event: QResizeEvent) -> None:
        InitializationSignals.grapherParameters.emit(event.size().width(), event.size().height())

    @Slot()
    def onNewFrame(self, drawableScene: DrawableScene) -> None:  # pylint: disable=missing-function-docstring
        self.scene = drawableScene
        MAIN_LOGGER.debug(self.scene)
        self.update()

    def paintEvent(self, _: QPaintEvent) -> None:
        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.setRenderHint(QPainter.Antialiasing)  # type: ignore[attr-defined]

            for point in self.scene.allDrawables:
                if isinstance(point, PointDrawable):
                    painter.drawEllipse(point.x, point.y, 5, 5)
                    # TODO add identifier

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)  # type: ignore[attr-defined]
            painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))
