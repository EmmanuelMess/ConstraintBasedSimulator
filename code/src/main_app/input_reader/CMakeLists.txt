add_library(input_reader
    ReadInput.cpp
    Parser.cpp
    SemanticsCheck.cpp)

add_library(ConstraintBasedSimulator::input_reader ALIAS input_reader)

target_link_libraries(
    input_reader
    PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
            ConstraintBasedSimulator::ConstraintBasedSimulator_warnings)


target_include_directories(input_reader ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                                $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_compile_features(input_reader PUBLIC cxx_std_20)

set_target_properties(
    input_reader
    PROPERTIES VERSION ${PROJECT_VERSION}
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN YES)

target_link_system_libraries(
    input_reader
    PRIVATE
    spdlog::spdlog
    foonathan::lexy)


if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(input_reader PUBLIC SAMPLE_LIBRARY_STATIC_DEFINE)
endif()
