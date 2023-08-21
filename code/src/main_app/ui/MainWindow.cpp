#include "main_app/ui/MainWindow.hpp"

#include <QtWidgets>

namespace ui::internal {
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , centralWidget(this)
    , layoutAllElements(&centralWidget)
    , layoutButtons()
    , grapherWidget()
    , pauseButton(QApplication::translate("MainWindow", "Pause"))
    , speedButton(QApplication::translate("MainWindow", "Change speed"))
{
    layoutButtons.addWidget(&pauseButton);
    layoutButtons.addWidget(&speedButton);

    layoutAllElements.addLayout(&layoutButtons);
    layoutAllElements.addWidget(&grapherWidget);

    centralWidget.setLayout(&layoutAllElements);

    setCentralWidget(&centralWidget);
}
}