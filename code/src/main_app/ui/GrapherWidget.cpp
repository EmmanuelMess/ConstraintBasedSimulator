#include "main_app/ui/GrapherWidget.hpp"

#include <QPainter>

namespace ui::internal {
GrapherWidget::GrapherWidget(QWidget *parent) : QWidget(parent) {}

void GrapherWidget::paintEvent(QPaintEvent *) {
    // Draw an arrow pointing downwards

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    // Draw a straight line
    painter.setPen(QPen(Qt::black, 0.1 * width()));
    painter.drawLine(width() / 2, 0, width() / 2, static_cast<int>(0.8 * height()));

    // Draw the arrow head
    painter.setPen(QPen(Qt::black, 1));
    painter.setBrush(Qt::black);
    painter.drawPolygon(QPolygonF() << QPointF(width() / 2, height())
                                    << QPointF(width() / 2 - 0.2 * width(), 0.8 * height())
                                    << QPointF(width() / 2 + 0.2 * width(), 0.8 * height()));



}

QSize GrapherWidget::sizeHint() const {
    if (width() < 20 || height() < 20) {
        return {20, 20};
    }

    return {width(), height()};
}
}