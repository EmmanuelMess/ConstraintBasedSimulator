#pragma once

#include <QWidget>

namespace ui::internal {
class GrapherWidget : public QWidget {
    Q_OBJECT
  public:
    explicit GrapherWidget(QWidget *parent = nullptr);

  protected:
    [[nodiscard]] QSize sizeHint() const override;
    void paintEvent(QPaintEvent *) override;
};
}
