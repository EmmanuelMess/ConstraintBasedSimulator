add_library(ui
    UiRunner.cpp
    MainWindow.cpp)

add_library(ConstraintBasedSimulator::ui ALIAS ui)

target_link_libraries(
    ui
    PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
            ConstraintBasedSimulator::ConstraintBasedSimulator_warnings)


target_include_directories(ui ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                      $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_compile_features(ui PUBLIC cxx_std_20)

set_target_properties(
    ui
    PROPERTIES VERSION ${PROJECT_VERSION}
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES)

find_package(Qt6 REQUIRED COMPONENTS Core Widgets)

target_link_system_libraries(
    ui
    PRIVATE
    spdlog::spdlog
    Qt6::Core
    Qt6::Widgets)


if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(ui PUBLIC SAMPLE_LIBRARY_STATIC_DEFINE)
endif()
