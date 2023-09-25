#include "main_app/ui/SimulationTimer.hpp"
#include "main_app/events_manager/EventManager.hpp"

#include <spdlog/spdlog.h>

#include <QTimer>

SimulationTimer::SimulationTimer(QObject *parent)
    : QObject(parent)
    , timer(new QTimer(this)) {
    connect(timer, &QTimer::timeout, this, &SimulationTimer::callback);
    timer->start(1000);
}

void SimulationTimer::callback() {
    spdlog::debug("Update!");
    events_manager::EventManager::getInstance().signalRefresh(std::chrono::milliseconds(1000));
}