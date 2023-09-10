#include "main_app/grapher/Grapher.hpp"
#include "main_app/grapher/EventManager.hpp"

namespace grapher {

Grapher::Grapher() {
    EventManager::getInstance().signalRefresh.connect([this]() { onRequireFrame(); });
    EventManager::getInstance().signalRequireFrame.connect([this]() { onRequireFrame(); });
}



void Grapher::onRequireFrame() {

}

} // grapher