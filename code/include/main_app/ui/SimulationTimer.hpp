#pragma once

#include <QtCore>

class SimulationTimer : public QObject {
    Q_OBJECT
public:
    SimulationTimer(QObject *parent = nullptr);

private slots:
    static void callback();

private:
    QTimer* timer;
};