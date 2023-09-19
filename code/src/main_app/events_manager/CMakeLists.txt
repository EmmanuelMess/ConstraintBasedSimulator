add_library(events_manager
    EventsInitializer.cpp)

add_library(ConstraintBasedSimulator::events_manager ALIAS events_manager)

target_link_libraries(
    events_manager
    PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
            ConstraintBasedSimulator::ConstraintBasedSimulator_warnings)


target_include_directories(events_manager ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                             $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_compile_features(events_manager PUBLIC cxx_std_20)

set_target_properties(
    events_manager
    PROPERTIES VERSION ${PROJECT_VERSION}
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES)

target_link_system_libraries(
    events_manager
    PRIVATE
    spdlog::spdlog
)


if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(events_manager PUBLIC SAMPLE_LIBRARY_STATIC_DEFINE)
endif()
