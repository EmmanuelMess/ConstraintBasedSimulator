cmake_minimum_required(VERSION 3.15...3.23)

project(CmakeConfigPackageTests LANGUAGES CXX)

# ---- Test as standalone project the exported config package ----

if(PROJECT_IS_TOP_LEVEL OR TEST_INSTALLED_VERSION)
  enable_testing()

  find_package(ConstraintBasedSimulator CONFIG REQUIRED) # for intro, project_options, ...

  if(NOT TARGET ConstraintBasedSimulator_options)
    message(FATAL_ERROR "Requiered config package not found!")
    return() # be strictly paranoid for Template Janitor github action! CK
  endif()
endif()

# ---- Dependencies ----

include(${Catch2_SOURCE_DIR}/extras/Catch.cmake)

# Provide a simple smoke test to make sure that the CLI works and can display a --help message
add_test(NAME cli.has_help COMMAND intro --help)

# Provide a test to verify that the version being reported from the application
# matches the version given to CMake. This will be important once you package
# your program. Real world shows that this is the kind of simple mistake that is easy
# to make, but also easy to test for.
add_test(NAME cli.version_matches COMMAND intro --version)
set_tests_properties(cli.version_matches PROPERTIES PASS_REGULAR_EXPRESSION "${PROJECT_VERSION}")

add_executable(ui_tests
    tests.cpp)

target_link_libraries(
  ui_tests
  PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_warnings
          ConstraintBasedSimulator::ConstraintBasedSimulator_options
          ConstraintBasedSimulator::ui
          foonathan::lexy
          Catch2::Catch2WithMain)

target_include_directories(ui_tests ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                         $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

if(WIN32 AND BUILD_SHARED_LIBS)
  add_custom_command(
    TARGET ui_tests
    PRE_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:ui_tests> $<TARGET_FILE_DIR:ui_tests>
    COMMAND_EXPAND_LISTS)
endif()

# automatically discover tests that are defined in catch based test files you can modify the unittests. Set TEST_PREFIX
# to whatever you want, or use different for different binaries
catch_discover_tests(
  ui_tests
  TEST_PREFIX
  "unittests."
  REPORTER
  XML
  OUTPUT_DIR
  .
  OUTPUT_PREFIX
  "unittests."
  OUTPUT_SUFFIX
  .xml)
