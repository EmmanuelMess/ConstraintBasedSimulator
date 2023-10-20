#pragma once

#include <QWidget>

#include "main_app/grapher/DrawableSimulation.hpp"

namespace ui::internal {
class GrapherWidget : public QWidget {
    Q_OBJECT
public:
    explicit GrapherWidget(QWidget *parent = nullptr);

protected:
    [[nodiscard]] QSize sizeHint() const override;
    void paintEvent(QPaintEvent * event) override;

private:
    grapher::DrawableSimulation frame;

    void onNewFrame(const grapher::DrawableSimulation& state);

    friend class EventLatch;
};
}
