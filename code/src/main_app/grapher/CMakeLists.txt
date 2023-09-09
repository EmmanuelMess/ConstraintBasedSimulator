add_library(grapher
    Grapher.cpp)

add_library(ConstraintBasedSimulator::grapher ALIAS grapher)

target_link_libraries(
    grapher
    PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
            ConstraintBasedSimulator::ConstraintBasedSimulator_warnings)


target_include_directories(grapher ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                             $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_compile_features(grapher PUBLIC cxx_std_20)

set_target_properties(
    grapher
    PROPERTIES VERSION ${PROJECT_VERSION}
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES)

target_link_system_libraries(
    grapher
    PRIVATE
    spdlog::spdlog
    eigen)


if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(grapher PUBLIC SAMPLE_LIBRARY_STATIC_DEFINE)
endif()
