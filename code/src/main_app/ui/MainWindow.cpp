#include "main_app/ui/MainWindow.hpp"

#include <QtWidgets>
#include <spdlog/spdlog.h>

#include "main_app/events_manager/EventManager.hpp"

namespace ui::internal {
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , centralWidget(this)
    , layoutAllElements(&centralWidget)
    , pauseButton(QApplication::translate("MainWindow", "Pause"))
    , speedButton(QApplication::translate("MainWindow", "Change speed"))
    , isPaused(false)
    , currentSpeed(SimulationSpeed::SPEED_X1)
{
    layoutButtons.addWidget(&pauseButton);
    layoutButtons.addWidget(&speedButton);

    layoutAllElements.addLayout(&layoutButtons);
    layoutAllElements.addWidget(&grapherWidget);

    centralWidget.setLayout(&layoutAllElements);

    setCentralWidget(&centralWidget);

    connect(&pauseButton, &QPushButton::released, this, &MainWindow::onClickedPause);
    connect(&speedButton, &QPushButton::released, this, &MainWindow::onClickedSpeed);
}

void MainWindow::onClickedPause() {
    spdlog::debug("Pause clicked {} -> {}", isPaused, !isPaused);
    isPaused = !isPaused;
    events_manager::EventManager::getInstance().signalPause(isPaused);
}

void MainWindow::onClickedSpeed() {
    const auto newSpeed = static_cast<SimulationSpeed>((static_cast<unsigned int>(currentSpeed) + 1) % static_cast<unsigned int>(SimulationSpeed::LAST_ELEMENT));
    spdlog::debug("Speed clicked {} -> {}", currentSpeed, newSpeed);
    currentSpeed = newSpeed;
    events_manager::EventManager::getInstance().signalSetSpeed(currentSpeed);
}

}