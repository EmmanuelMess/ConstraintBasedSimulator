add_library(simulator
    EventLatch.cpp
    Simulator.cpp
    StateLoader.cpp)

add_library(ConstraintBasedSimulator::simulator ALIAS simulator)

target_link_libraries(
    simulator
    PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
            ConstraintBasedSimulator::ConstraintBasedSimulator_warnings
            input_reader)


target_include_directories(simulator ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                             $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_compile_features(simulator PUBLIC cxx_std_20)

set_target_properties(
    simulator
    PROPERTIES VERSION ${PROJECT_VERSION}
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES)

target_link_system_libraries(
    simulator
    PRIVATE
    spdlog::spdlog
    Eigen3::Eigen
    autodiff)


if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(simulator PUBLIC SAMPLE_LIBRARY_STATIC_DEFINE)
endif()
