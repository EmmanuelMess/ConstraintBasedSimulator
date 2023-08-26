#include "main_app/ui/UiRunner.hpp"

#include <QApplication>
#include <QtWidgets>

#include "main_app/ui/MainWindow.hpp"

namespace ui {
// NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
int runUi(int argc, char *argv[]) {
    const unsigned int width = 1550;
    const unsigned int height = 600;

    const QApplication app(argc, argv);
    ui::internal::MainWindow mainWindow;
    mainWindow.resize(width, height);
    mainWindow.show();
    mainWindow.setWindowTitle(QApplication::translate("toplevel", "Top-level widget"));
    return app.exec();
}
}
