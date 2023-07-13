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
    cpmaddpackage("https://github.com/foonathan/lexy/releases/download/v2022.12.1/lexy-src.zip")
  endif()

  if(NOT TARGET eigen)
    cpmaddpackage("https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.zip")
  endif()

  if(NOT TARGET qt6)
    message("-- Adding qt6")

    # Download and extract archive of Qt 6.4.2
    set( QT_VERSION "6.4.2" )
    set( QT_ARCHIVE_URL "https://download.qt.io/official_releases/qt/6.4/${QT_VERSION}/submodules/qtbase-everywhere-src-${QT_VERSION}.tar.xz" )
    set( QT_ARCHIVE_FILE "/tmp/qtbase-everywhere-src-${QT_VERSION}.tar.xz" )
    set( QT_BASE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps" )
    set( QT_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps/qtbase-everywhere-src-${QT_VERSION}" )
    set( QT_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/_deps/qtbase-everywhere-src-${QT_VERSION}-build" )

    file( DOWNLOAD ${QT_ARCHIVE_URL} ${QT_ARCHIVE_FILE}
        SHOW_PROGRESS
        EXPECTED_HASH MD5=01f3938ca797d0e5a578c7786c618fb7)
    execute_process( COMMAND ${CMAKE_COMMAND} -E tar xvf ${QT_ARCHIVE_FILE}
        WORKING_DIRECTORY ${QT_BASE_DIR}
        OUTPUT_QUIET)

    # Configure Qt (skip building of useless modules)
    file( MAKE_DIRECTORY ${QT_BUILD_DIR} )
    execute_process( COMMAND ${QT_SOURCE_DIR}/configure -prefix ${QT_BUILD_DIR} WORKING_DIRECTORY ${QT_BUILD_DIR} )

    # Check if system supports parallelization
    if( DEFINED ENV{NUMBER_OF_PROCESSORS} )
      set( JOBS_OPTION "-j$ENV{NUMBER_OF_PROCESSORS}" )
    elseif( DEFINED ENV{PROCESSOR_COUNT} )
      set( JOBS_OPTION "-j$ENV{PROCESSOR_COUNT}" )
    else()
      set( JOBS_OPTION "" )
    endif()

    # Use -j option to compile if possible (qt is very big)
    if( JOBS_OPTION )
      execute_process( COMMAND ninja ${JOBS_OPTION} WORKING_DIRECTORY ${QT_BUILD_DIR} )
    else()
      execute_process( COMMAND ninja WORKING_DIRECTORY ${QT_BUILD_DIR} )
    endif()

    # Set necessary environment variables to use Qt
    set( ENV{QTDIR} ${QT_BUILD_DIR} )
    set( ENV{PATH} ${QT_BUILD_DIR}/bin:$ENV{PATH})
  endif()

endfunction()
