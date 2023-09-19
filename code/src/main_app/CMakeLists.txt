add_subdirectory("events_manager")
add_subdirectory("grapher")
add_subdirectory("input_reader")
add_subdirectory("simulator")
add_subdirectory("ui")

add_executable(main_app
    main.cpp)

target_link_libraries(
  main_app
  PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
          ConstraintBasedSimulator::ConstraintBasedSimulator_warnings
          ConstraintBasedSimulator::input_reader
          ConstraintBasedSimulator::events_manager
          ConstraintBasedSimulator::ui)


target_include_directories(main_app ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                            $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_link_system_libraries(
  main_app
  PRIVATE
          spdlog::spdlog
)

target_include_directories(main_app PRIVATE "${CMAKE_BINARY_DIR}/configured_files/include")
