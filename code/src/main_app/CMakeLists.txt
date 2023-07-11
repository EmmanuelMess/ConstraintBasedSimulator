add_executable(main_app main.cpp input_file.cpp)

target_link_libraries(
  main_app
  PRIVATE ConstraintBasedSimulator::ConstraintBasedSimulator_options
          ConstraintBasedSimulator::ConstraintBasedSimulator_warnings)


target_include_directories(main_app ${WARNING_GUARD} PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                                                            $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}/include>)

target_link_system_libraries(
  main_app
  PRIVATE
          spdlog::spdlog
          foonathan::lexy
          eigen)

target_include_directories(main_app PRIVATE "${CMAKE_BINARY_DIR}/configured_files/include")
