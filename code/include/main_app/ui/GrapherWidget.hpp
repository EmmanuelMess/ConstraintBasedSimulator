#ifndef CONSTRAINTBASEDSIMULATOR_GRAPHERWIDGET_HPP
#define CONSTRAINTBASEDSIMULATOR_GRAPHERWIDGET_HPP

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

#endif// CONSTRAINTBASEDSIMULATOR_GRAPHERWIDGET_HPP
