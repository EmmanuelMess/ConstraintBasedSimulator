#pragma once

#include <QtCore>

class SimulationTimer : public QObject {
    Q_OBJECT
public:
    explicit SimulationTimer(QObject *parent = nullptr);

private slots:
    static void callback();

private:
    static constexpr std::chrono::milliseconds TIME_STEP = std::chrono::milliseconds(1000);

    QTimer* timer;
};