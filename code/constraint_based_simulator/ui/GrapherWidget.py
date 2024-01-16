from PySide6.QtCore import QPoint, QSize, QRect, qVersion, Qt
from PySide6.QtGui import QPolygon, QPen, QBrush, QPixmap, QPalette, QPainterPath, QPainter
from PySide6.QtWidgets import QWidget


class GrapherWidget(QWidget):
    points = QPolygon([
        QPoint(10, 80),
        QPoint(20, 10),
        QPoint(80, 30),
        QPoint(90, 70)
    ])

    (Line, Points, Polyline, Polygon, Rect, RoundedRect, Ellipse,
     Arc, Chord, Pie, Path, Text, Pixmap) = range(13)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.pen = QPen()
        self.brush = QBrush()
        self.pixmap = QPixmap()

        self.shape = GrapherWidget.Polygon
        self.antialiased = False
        self.transformed = False
        self.pixmap.load(':/images/qt-logo.png')

        self.setBackgroundRole(QPalette.Base)
        self.setAutoFillBackground(True)

    def minimumSizeHint(self):
        return QSize(100, 100)

    def sizeHint(self):
        return QSize(400, 200)

    def set_shape(self, shape):
        self.shape = shape
        self.update()

    def set_pen(self, pen):
        self.pen = pen
        self.update()

    def set_brush(self, brush):
        self.brush = brush
        self.update()

    def set_antialiased(self, antialiased):
        self.antialiased = antialiased
        self.update()

    def set_transformed(self, transformed):
        self.transformed = transformed
        self.update()

    def paintEvent(self, event):
        rect = QRect(10, 20, 80, 60)

        path = QPainterPath()
        path.moveTo(20, 80)
        path.lineTo(20, 30)
        path.cubicTo(80, 0, 50, 50, 80, 80)

        start_angle = 30 * 16
        arc_length = 120 * 16

        with QPainter(self) as painter:
            painter.setPen(self.pen)
            painter.setBrush(self.brush)
            if self.antialiased:
                painter.setRenderHint(QPainter.Antialiasing)

            for x in range(0, self.width(), 100):
                for y in range(0, self.height(), 100):
                    painter.save()
                    painter.translate(x, y)
                    if self.transformed:
                        painter.translate(50, 50)
                        painter.rotate(60.0)
                        painter.scale(0.6, 0.9)
                        painter.translate(-50, -50)

                    if self.shape == GrapherWidget.Line:
                        painter.drawLine(rect.bottomLeft(), rect.topRight())
                    elif self.shape == GrapherWidget.Points:
                        painter.drawPoints(GrapherWidget.points)
                    elif self.shape == GrapherWidget.Polyline:
                        painter.drawPolyline(GrapherWidget.points)
                    elif self.shape == GrapherWidget.Polygon:
                        painter.drawPolygon(GrapherWidget.points)
                    elif self.shape == GrapherWidget.Rect:
                        painter.drawRect(rect)
                    elif self.shape == GrapherWidget.RoundedRect:
                        painter.drawRoundedRect(rect, 25, 25, Qt.RelativeSize)
                    elif self.shape == GrapherWidget.Ellipse:
                        painter.drawEllipse(rect)
                    elif self.shape == GrapherWidget.Arc:
                        painter.drawArc(rect, start_angle, arc_length)
                    elif self.shape == GrapherWidget.Chord:
                        painter.drawChord(rect, start_angle, arc_length)
                    elif self.shape == GrapherWidget.Pie:
                        painter.drawPie(rect, start_angle, arc_length)
                    elif self.shape == GrapherWidget.Path:
                        painter.drawPath(path)
                    elif self.shape == GrapherWidget.Text:
                        qv = qVersion()
                        painter.drawText(rect, Qt.AlignCenter,
                                         f"PySide 6\nQt {qv}")
                    elif self.shape == GrapherWidget.Pixmap:
                        painter.drawPixmap(10, 10, self.pixmap)

                    painter.restore()

            painter.setPen(self.palette().dark().color())
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(QRect(0, 0, self.width() - 1, self.height() - 1))

