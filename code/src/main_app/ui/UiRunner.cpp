#include "main_app/ui/UiRunner.hpp"

#include <QApplication>

#include "main_app/events_manager/EventManager.hpp"
#include "main_app/grapher/Grapher.hpp"
#include "main_app/ui/MainWindow.hpp"
#include "main_app/ui/SimulationTimer.hpp"

namespace ui {
// NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
int runUi(int argc, char *argv[]) {
    const unsigned int width = 1550;
    const unsigned int height = 600;

    QApplication app(argc, argv);
    new SimulationTimer(dynamic_cast<QObject *>(&app));

    internal::MainWindow mainWindow;
    mainWindow.resize(width, height);
    mainWindow.show();
    mainWindow.setWindowTitle(QApplication::translate("toplevel", "Top-level widget"));
    return app.exec();
}
}
