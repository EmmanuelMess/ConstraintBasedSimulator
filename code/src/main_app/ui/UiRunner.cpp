#include "main_app/ui/UiRunner.hpp"

#include <QApplication>
#include <QtWidgets>

#include "main_app/ui/GrapherWidget.hpp"

namespace ui {
int runUi(int argc, char *argv[]) {
    const QApplication app(argc, argv);
    internal::GrapherWidget window;
    window.resize(320, 240);
    window.show();
    window.setWindowTitle(QApplication::translate("toplevel", "Top-level widget"));
    return app.exec();
}
}
