#include "main_app/ui/SimulationTimer.hpp"
#include "main_app/events_manager/EventManager.hpp"

#include <spdlog/spdlog.h>

#include <QTimer>

SimulationTimer::SimulationTimer(QObject *parent)
    : QObject(parent)
    , timer(new QTimer(this)) {
    connect(timer, &QTimer::timeout, this, &SimulationTimer::callback);
    timer->start(TIME_STEP);
}

void SimulationTimer::callback() {
    spdlog::debug("Update!");
    events_manager::EventManager::getInstance().signalRefresh(TIME_STEP);
}