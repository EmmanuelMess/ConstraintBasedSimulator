include(cmake/CPM.cmake)

# Done as a function so that updates to variables like
# CMAKE_CXX_FLAGS don't propagate out to other
# targets
function(ConstraintBasedSimulator_setup_dependencies)

  # For each dependency, see if it's
  # already been provided to us by a parent project

  if(NOT TARGET fmtlib::fmtlib)
    cpmaddpackage("gh:fmtlib/fmt#9.1.0")
  endif()

  if(NOT TARGET spdlog::spdlog)
    cpmaddpackage(
      NAME
      spdlog
      VERSION
      1.11.0
      GITHUB_REPOSITORY
      "gabime/spdlog"
      OPTIONS
      "SPDLOG_FMT_EXTERNAL ON")
  endif()

  if(NOT TARGET Catch2::Catch2WithMain)
    cpmaddpackage("gh:catchorg/Catch2@3.3.2")
  endif()

  if(NOT TARGET CLI11::CLI11)
    cpmaddpackage("gh:CLIUtils/CLI11@2.3.2")
  endif()

  if(NOT TARGET tools::tools)
    cpmaddpackage("gh:lefticus/tools#update_build_system")
  endif()

  if(NOT TARGET foonathan::lexy)
    CPMAddPackage("gh:foonathan/lexy#7e583fe0c717715a10227d2d4ba14581143cf0af")
  endif()

  if(NOT TARGET Eigen3::Eigen)
    set(EIGEN_BUILD_DOC OFF)
    set(BUILD_TESTING OFF)
    set(EIGEN_BUILD_PKGCONFIG OFF)
    cpmaddpackage("https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip")
  endif()

  if(NOT TARGET qt6)
    message(STATUS "Adding qt6")

    # Download and extract archive of Qt
    set( QT_VERSION "6.5.2" )
    set( QT_COMPRESSED_FILE "qtbase-everywhere-src-${QT_VERSION}" )
    set( QT_ARCHIVE_URL "https://download.qt.io/official_releases/qt/6.5/${QT_VERSION}/submodules/${QT_COMPRESSED_FILE}.tar.xz" )
    set( QT_ARCHIVE_PATH "/tmp/${QT_COMPRESSED_FILE}.tar.xz" )
    set( QT_BASE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps" )
    set( QT_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps/${QT_COMPRESSED_FILE}" )
    set( QT_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps/${QT_COMPRESSED_FILE}-build" )

    file( DOWNLOAD ${QT_ARCHIVE_URL} ${QT_ARCHIVE_PATH}
        SHOW_PROGRESS
        EXPECTED_HASH MD5=0c184f5a9bdf166c3811cd2d51feda45)
    execute_process( COMMAND ${CMAKE_COMMAND} -E tar xvf ${QT_ARCHIVE_PATH}
        WORKING_DIRECTORY ${QT_BASE_DIR}
        OUTPUT_QUIET)


    # Configure Qt (skip building of useless modules)
    file( MAKE_DIRECTORY ${QT_BUILD_DIR} )

    if (CMAKE_SYSTEM_NAME STREQUAL "Linux")
      message(STATUS "Configuring Qt for Linux")
      execute_process( COMMAND ${QT_SOURCE_DIR}/configure -release -c++std c++20 -prefix ${QT_BUILD_DIR} WORKING_DIRECTORY ${QT_BUILD_DIR} )
    endif ()
    if (CMAKE_SYSTEM_NAME STREQUAL "Windows")
      message(STATUS "Configuring Qt for Windows")
      execute_process( COMMAND ${QT_SOURCE_DIR}/configure.bat -release -c++std c++20 -prefix ${QT_BUILD_DIR} WORKING_DIRECTORY ${QT_BUILD_DIR} )
    endif ()

    message(STATUS "Building Qt")
    execute_process( COMMAND cmake --build . --parallel ${JOBS_OPTION} WORKING_DIRECTORY ${QT_BUILD_DIR} )

    # Set necessary environment variables to use Qt
    set( ENV{QTDIR} ${QT_BUILD_DIR} )
    set( ENV{PATH} ${QT_BUILD_DIR}/bin:$ENV{PATH})
    set( ENV{CMAKE_PREFIX_PATH} ${QT_BUILD_DIR}/bin:$ENV{CMAKE_PREFIX_PATH})
  endif()

  if(NOT TARGET autodiff)
    set(AUTODIFF_BUILD_PYTHON OFF)
    cpmaddpackage("gh:autodiff/autodiff@1.0.3")
  endif()

  if(NOT TARGET backward)
    cpmaddpackage("gh:bombela/backward-cpp@1.6")
  endif()

endfunction()
