find_package(Qt6 REQUIRED COMPONENTS Core Widgets)
qt_standard_project_setup()

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

if (NOT CMAKE_PREFIX_PATH)
  message(WARNING "CMAKE_PREFIX_PATH is not defined, you may need to set it "
      "(-DCMAKE_PREFIX_PATH=\"path/to/Qt/lib/cmake\" or -DCMAKE_PREFIX_PATH=/usr/include/{host}/qt{version}/ on Ubuntu)")
endif ()

qt_add_library(ui STATIC
    UiRunner.cpp
    MainWindow.cpp
    GrapherWidget.cpp
    SimulationTimer.cpp

    # HACK adding headers here is required for Q_OBJECT
    ${PROJECT_SOURCE_DIR}/include/main_app/ui/UiRunner.hpp
    ${PROJECT_SOURCE_DIR}/include/main_app/ui/MainWindow.hpp
    ${PROJECT_SOURCE_DIR}/include/main_app/ui/GrapherWidget.hpp
    ${PROJECT_SOURCE_DIR}/include/main_app/ui/SimulationTimer.hpp
)

add_library(ConstraintBasedSimulator::ui ALIAS ui)

target_link_libraries(
    ui
    PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
            ConstraintBasedSimulator::ConstraintBasedSimulator_warnings
            ConstraintBasedSimulator::grapher)


target_include_directories(ui ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                      $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_compile_features(ui PUBLIC cxx_std_20)

set_target_properties(
    ui
    PROPERTIES VERSION ${PROJECT_VERSION}
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES)

target_link_system_libraries(
    ui
    PRIVATE
    spdlog::spdlog
    Qt6::Core
    Qt6::Widgets
)


if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(ui PUBLIC SAMPLE_LIBRARY_STATIC_DEFINE)
endif()
