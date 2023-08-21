#include "main_app/ui/UiRunner.hpp"

#include <QApplication>
#include <QtWidgets>

#include "main_app/ui/MainWindow.hpp"

namespace ui {
int runUi(int argc, char *argv[]) {
    const QApplication app(argc, argv);
    ui::internal::MainWindow mainWindow;
    mainWindow.resize(1550, 600);
    mainWindow.show();
    mainWindow.setWindowTitle(QApplication::translate("toplevel", "Top-level widget"));
    return app.exec();
}
}
