#include "main_app/ui/UiRunner.hpp"

#include <QApplication>
#include <QtWidgets>

namespace ui {
int runUi(int argc, char *argv[]) {
    QApplication app(argc, argv);
    QWidget window;
    window.resize(320, 240);
    window.show();
    window.setWindowTitle(QApplication::translate("toplevel", "Top-level widget"));
    return app.exec();
}
}
