#include "main_app/ui/UiRunner.hpp"

#include <QApplication>
#include <QtWidgets>

#include "main_app/events_manager/EventManager.hpp"
#include "main_app/grapher/Grapher.hpp"
#include "main_app/ui/MainWindow.hpp"

namespace ui {
// NOLINTNEXTLINE(cppcoreguidelines-avoid-c-arrays,hicpp-avoid-c-arrays,modernize-avoid-c-arrays)
int runUi(int argc, char *argv[]) {
    const unsigned int width = 1550;
    const unsigned int height = 600;

    {
        // TODO test
        events_manager::EventManager::getInstance().signalPause(false);
        events_manager::EventManager::getInstance().signalRefresh(std::chrono::milliseconds(100));
        events_manager::EventManager::getInstance().signalRefresh(std::chrono::milliseconds(100));
        events_manager::EventManager::getInstance().signalRefresh(std::chrono::milliseconds(100));
        events_manager::EventManager::getInstance().signalRefresh(std::chrono::milliseconds(100));
        events_manager::EventManager::getInstance().signalRefresh(std::chrono::milliseconds(100));
    }

    const QApplication app(argc, argv);
    ui::internal::MainWindow mainWindow;
    mainWindow.resize(width, height);
    mainWindow.show();
    mainWindow.setWindowTitle(QApplication::translate("toplevel", "Top-level widget"));
    return app.exec();
}
}
