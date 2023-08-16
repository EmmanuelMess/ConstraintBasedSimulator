#ifndef CONSTRAINTBASEDSIMULATOR_MAINWINDOW_HPP
#define CONSTRAINTBASEDSIMULATOR_MAINWINDOW_HPP

#include <QtCore>
#include <QMainWindow>

namespace ui::internal {
class MainWindow : public QMainWindow {
    Q_OBJECT

  public:
    MainWindow(QWidget *parent = nullptr);

};
}

#endif// CONSTRAINTBASEDSIMULATOR_MAINWINDOW_HPP
