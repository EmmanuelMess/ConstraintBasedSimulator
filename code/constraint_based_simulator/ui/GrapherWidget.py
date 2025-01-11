from PySide6.QtCore import QSize, QRect, Qt, Signal, Slot
from PySide6.QtGui import QPen, QBrush, QPalette, QPainter, QResizeEvent, QColorConstants, QPaintEvent
from PySide6.QtWidgets import QWidget
from typing_extensions import Union

from constraint_based_simulator.common.MainLogger import MAIN_LOGGER
from constraint_based_simulator.events_manager import InitializationSignals
from constraint_based_simulator.grapher.drawables.BarDrawable import BarDrawable
from constraint_based_simulator.grapher.drawables.CircleDrawable import CircleDrawable
from constraint_based_simulator.grapher.drawables.DrawableScene import DrawableScene
from constraint_based_simulator.grapher.drawables.PointDrawable import PointDrawable


class GrapherWidget(QWidget):
    """
    Grapher Qt Widget, view for the simulator (model-view-presenter pattern)
    """
    newFrame = Signal(DrawableScene)

    def __init__(self, parent: Union[QWidget, None] = None) -> None:
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

    @Slot(DrawableScene)  # type: ignore
    def onNewFrame(self, drawableScene: DrawableScene) -> None:  # pylint: disable=missing-function-docstring
        self.scene = drawableScene
        MAIN_LOGGER.debug(self.scene)
        self.update()

    def paintEvent(self, _: QPaintEvent) -> None:
        # TODO fix the positioning inside the window

        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            painter.setRenderHint(QPainter.Antialiasing)  # type: ignore[attr-defined]

            for drawable in self.scene.allDrawables:
                if isinstance(drawable, PointDrawable):
                    radius = 2
                    painter.drawEllipse(drawable.x - radius, drawable.y - radius, radius*2, radius*2)
                    painter.drawText(drawable.x, drawable.y, drawable.identifier)
                elif isinstance(drawable, BarDrawable):
                    painter.drawLine(drawable.xStart, drawable.yStart, drawable.xEnd, drawable.yEnd)
                elif isinstance(drawable, CircleDrawable):
                    radius = drawable.radius
                    painter.setBrush(Qt.NoBrush)  # type: ignore[attr-defined]
                    painter.drawEllipse(drawable.x - radius, drawable.y - radius, radius*2, radius*2)
                    painter.setBrush(self.brush)

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)  # type: ignore[attr-defined]
            painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))
