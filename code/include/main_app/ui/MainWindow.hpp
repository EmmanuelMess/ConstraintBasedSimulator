#pragma once

#include <QMainWindow>
#include <QtCore>
#include <QtWidgets>

#include "main_app/ui/SimulationSpeed.hpp"
#include "main_app/ui/GrapherWidget.hpp"

namespace ui::internal {
class MainWindow : public QMainWindow {
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);

private slots:
    void onClickedPause();
    void onClickedSpeed();

private:
    QWidget centralWidget;
    QVBoxLayout layoutAllElements;
    QHBoxLayout layoutButtons;
    GrapherWidget grapherWidget;
    QPushButton pauseButton;
    QPushButton speedButton;

    bool isPaused;
    SimulationSpeed currentSpeed;
};
}
