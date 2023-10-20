#include "main_app/ui/GrapherWidget.hpp"

#include <spdlog/spdlog.h>

#include <QPainter>

#include "main_app/events_manager/EventManager.hpp"

namespace ui::internal {
GrapherWidget::GrapherWidget(QWidget *parent) : QWidget(parent) {
    events_manager::EventManager::getInstance().signalNewFrame.connect([this](const grapher::DrawableSimulation& state) {
        this->onNewFrame(state);
    });
}

void GrapherWidget::paintEvent(__attribute__((unused)) QPaintEvent * event) {
    const double MARGIN = 20.0;
    const double WIDTH = width() - MARGIN * 2;
    const double HEIGHT = height() - MARGIN * 2;
    const double PARTICLE_RADIUS = 10.0;

      QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    painter.setBrush(Qt::black);
    for(const auto& particlePosition : frame.particlePositions) {
        const double drawnPositionX = MARGIN + particlePosition.x * WIDTH;
        const double drawnPositionY = MARGIN + particlePosition.y * HEIGHT;
        painter.drawEllipse(QPointF(drawnPositionX, drawnPositionY),  PARTICLE_RADIUS, PARTICLE_RADIUS);
        spdlog::debug("Drawn ({}, {})", drawnPositionX, drawnPositionY);
    }

}

QSize GrapherWidget::sizeHint() const {
    constexpr int MIN_WIDTH = 20;
    constexpr int MIN_HEIGHT = 20;

    if (width() < MIN_WIDTH || height() < MIN_HEIGHT) {
        return {MIN_WIDTH, MIN_HEIGHT};
    }

    return {width(), height()};
}

void GrapherWidget::onNewFrame(const grapher::DrawableSimulation& state) {
    spdlog::debug("New frame!");
    this->frame = state;
    update();
}
}