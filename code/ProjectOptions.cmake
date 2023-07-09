include(cmake/SystemLink.cmake)
include(cmake/LibFuzzer.cmake)
include(CMakeDependentOption)
include(CheckCXXCompilerFlag)


macro(ConstraintBasedSimulator_supports_sanitizers)
  if((CMAKE_CXX_COMPILER_ID MATCHES ".*Clang.*" OR CMAKE_CXX_COMPILER_ID MATCHES ".*GNU.*") AND NOT WIN32)
    set(SUPPORTS_UBSAN ON)
  else()
    set(SUPPORTS_UBSAN OFF)
  endif()

  if((CMAKE_CXX_COMPILER_ID MATCHES ".*Clang.*" OR CMAKE_CXX_COMPILER_ID MATCHES ".*GNU.*") AND WIN32)
    set(SUPPORTS_ASAN OFF)
  else()
    set(SUPPORTS_ASAN ON)
  endif()
endmacro()

macro(ConstraintBasedSimulator_setup_options)
  option(ConstraintBasedSimulator_ENABLE_HARDENING "Enable hardening" ON)
  option(ConstraintBasedSimulator_ENABLE_COVERAGE "Enable coverage reporting" OFF)
  cmake_dependent_option(
    ConstraintBasedSimulator_ENABLE_GLOBAL_HARDENING
    "Attempt to push hardening options to built dependencies"
    ON
    ConstraintBasedSimulator_ENABLE_HARDENING
    OFF)

  ConstraintBasedSimulator_supports_sanitizers()

  if(NOT PROJECT_IS_TOP_LEVEL OR ConstraintBasedSimulator_PACKAGING_MAINTAINER_MODE)
    option(ConstraintBasedSimulator_ENABLE_IPO "Enable IPO/LTO" OFF)
    option(ConstraintBasedSimulator_WARNINGS_AS_ERRORS "Treat Warnings As Errors" OFF)
    option(ConstraintBasedSimulator_ENABLE_USER_LINKER "Enable user-selected linker" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_LEAK "Enable leak sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED "Enable undefined sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD "Enable thread sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_MEMORY "Enable memory sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_UNITY_BUILD "Enable unity builds" OFF)
    option(ConstraintBasedSimulator_ENABLE_CLANG_TIDY "Enable clang-tidy" OFF)
    option(ConstraintBasedSimulator_ENABLE_CPPCHECK "Enable cpp-check analysis" OFF)
    option(ConstraintBasedSimulator_ENABLE_PCH "Enable precompiled headers" OFF)
    option(ConstraintBasedSimulator_ENABLE_CACHE "Enable ccache" OFF)
  else()
    option(ConstraintBasedSimulator_ENABLE_IPO "Enable IPO/LTO" ON)
    option(ConstraintBasedSimulator_WARNINGS_AS_ERRORS "Treat Warnings As Errors" ON)
    option(ConstraintBasedSimulator_ENABLE_USER_LINKER "Enable user-selected linker" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS "Enable address sanitizer" ${SUPPORTS_ASAN})
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_LEAK "Enable leak sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED "Enable undefined sanitizer" ${SUPPORTS_UBSAN})
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD "Enable thread sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_SANITIZER_MEMORY "Enable memory sanitizer" OFF)
    option(ConstraintBasedSimulator_ENABLE_UNITY_BUILD "Enable unity builds" OFF)
    option(ConstraintBasedSimulator_ENABLE_CLANG_TIDY "Enable clang-tidy" ON)
    option(ConstraintBasedSimulator_ENABLE_CPPCHECK "Enable cpp-check analysis" ON)
    option(ConstraintBasedSimulator_ENABLE_PCH "Enable precompiled headers" OFF)
    option(ConstraintBasedSimulator_ENABLE_CACHE "Enable ccache" ON)
  endif()

  if(NOT PROJECT_IS_TOP_LEVEL)
    mark_as_advanced(
      ConstraintBasedSimulator_ENABLE_IPO
      ConstraintBasedSimulator_WARNINGS_AS_ERRORS
      ConstraintBasedSimulator_ENABLE_USER_LINKER
      ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS
      ConstraintBasedSimulator_ENABLE_SANITIZER_LEAK
      ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED
      ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD
      ConstraintBasedSimulator_ENABLE_SANITIZER_MEMORY
      ConstraintBasedSimulator_ENABLE_UNITY_BUILD
      ConstraintBasedSimulator_ENABLE_CLANG_TIDY
      ConstraintBasedSimulator_ENABLE_CPPCHECK
      ConstraintBasedSimulator_ENABLE_COVERAGE
      ConstraintBasedSimulator_ENABLE_PCH
      ConstraintBasedSimulator_ENABLE_CACHE)
  endif()

  ConstraintBasedSimulator_check_libfuzzer_support(LIBFUZZER_SUPPORTED)
  if(LIBFUZZER_SUPPORTED AND (ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS OR ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD OR ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED))
    set(DEFAULT_FUZZER ON)
  else()
    set(DEFAULT_FUZZER OFF)
  endif()

  option(ConstraintBasedSimulator_BUILD_FUZZ_TESTS "Enable fuzz testing executable" ${DEFAULT_FUZZER})

endmacro()

macro(ConstraintBasedSimulator_global_options)
  if(ConstraintBasedSimulator_ENABLE_IPO)
    include(cmake/InterproceduralOptimization.cmake)
    ConstraintBasedSimulator_enable_ipo()
  endif()

  ConstraintBasedSimulator_supports_sanitizers()

  if(ConstraintBasedSimulator_ENABLE_HARDENING AND ConstraintBasedSimulator_ENABLE_GLOBAL_HARDENING)
    include(cmake/Hardening.cmake)
    if(NOT SUPPORTS_UBSAN 
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_LEAK)
      set(ENABLE_UBSAN_MINIMAL_RUNTIME FALSE)
    else()
      set(ENABLE_UBSAN_MINIMAL_RUNTIME TRUE)
    endif()
    message("${ConstraintBasedSimulator_ENABLE_HARDENING} ${ENABLE_UBSAN_MINIMAL_RUNTIME} ${ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED}")
    ConstraintBasedSimulator_enable_hardening(ConstraintBasedSimulator_options ON ${ENABLE_UBSAN_MINIMAL_RUNTIME})
  endif()
endmacro()

macro(ConstraintBasedSimulator_local_options)
  if(PROJECT_IS_TOP_LEVEL)
    include(cmake/StandardProjectSettings.cmake)
  endif()

  add_library(ConstraintBasedSimulator_warnings INTERFACE)
  add_library(ConstraintBasedSimulator_options INTERFACE)

  include(cmake/CompilerWarnings.cmake)
  ConstraintBasedSimulator_set_project_warnings(
    ConstraintBasedSimulator_warnings
    ${ConstraintBasedSimulator_WARNINGS_AS_ERRORS}
    ""
    ""
    ""
    "")

  if(ConstraintBasedSimulator_ENABLE_USER_LINKER)
    include(cmake/Linker.cmake)
    configure_linker(ConstraintBasedSimulator_options)
  endif()

  include(cmake/Sanitizers.cmake)
  ConstraintBasedSimulator_enable_sanitizers(
    ConstraintBasedSimulator_options
    ${ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS}
    ${ConstraintBasedSimulator_ENABLE_SANITIZER_LEAK}
    ${ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED}
    ${ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD}
    ${ConstraintBasedSimulator_ENABLE_SANITIZER_MEMORY})

  set_target_properties(ConstraintBasedSimulator_options PROPERTIES UNITY_BUILD ${ConstraintBasedSimulator_ENABLE_UNITY_BUILD})

  if(ConstraintBasedSimulator_ENABLE_PCH)
    target_precompile_headers(
      ConstraintBasedSimulator_options
      INTERFACE
      <vector>
      <string>
      <utility>)
  endif()

  if(ConstraintBasedSimulator_ENABLE_CACHE)
    include(cmake/Cache.cmake)
    ConstraintBasedSimulator_enable_cache()
  endif()

  include(cmake/StaticAnalyzers.cmake)
  if(ConstraintBasedSimulator_ENABLE_CLANG_TIDY)
    ConstraintBasedSimulator_enable_clang_tidy(ConstraintBasedSimulator_options ${ConstraintBasedSimulator_WARNINGS_AS_ERRORS})
  endif()

  if(ConstraintBasedSimulator_ENABLE_CPPCHECK)
    ConstraintBasedSimulator_enable_cppcheck(${ConstraintBasedSimulator_WARNINGS_AS_ERRORS} "" # override cppcheck options
    )
  endif()

  if(ConstraintBasedSimulator_ENABLE_COVERAGE)
    include(cmake/Tests.cmake)
    ConstraintBasedSimulator_enable_coverage(ConstraintBasedSimulator_options)
  endif()

  if(ConstraintBasedSimulator_WARNINGS_AS_ERRORS)
    check_cxx_compiler_flag("-Wl,--fatal-warnings" LINKER_FATAL_WARNINGS)
    if(LINKER_FATAL_WARNINGS)
      # This is not working consistently, so disabling for now
      # target_link_options(ConstraintBasedSimulator_options INTERFACE -Wl,--fatal-warnings)
    endif()
  endif()

  if(ConstraintBasedSimulator_ENABLE_HARDENING AND NOT ConstraintBasedSimulator_ENABLE_GLOBAL_HARDENING)
    include(cmake/Hardening.cmake)
    if(NOT SUPPORTS_UBSAN 
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_UNDEFINED
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_ADDRESS
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_THREAD
       OR ConstraintBasedSimulator_ENABLE_SANITIZER_LEAK)
      set(ENABLE_UBSAN_MINIMAL_RUNTIME FALSE)
    else()
      set(ENABLE_UBSAN_MINIMAL_RUNTIME TRUE)
    endif()
    ConstraintBasedSimulator_enable_hardening(ConstraintBasedSimulator_options OFF ${ENABLE_UBSAN_MINIMAL_RUNTIME})
  endif()

endmacro()
