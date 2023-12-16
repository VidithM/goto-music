if (NOT WIN32)
    # Set compiler paths below, or comment out to use default compiler
    # set (CMAKE_C_COMPILER "/usr/bin/gcc")
    # set (CMAKE_CXX_COMPILER "/usr/bin/g++")
endif ()

cmake_minimum_required (VERSION 3.0)
project (pkd)

set (PYTHON_VERSION "3.9")

# Find Python and OpenMP
find_package (Python "${PYTHON_VERSION}" EXACT REQUIRED COMPONENTS Development)
find_package (OpenMP REQUIRED)

# Set project include/src paths, get all headers and source files, configure final library
set (PKD_SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src")
set (PKD_INCLUDE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/include")
message (STATUS "USING INCLUDE DIR: ${PKD_INCLUDE_DIR}")
message (STATUS "USING SOURCE DIR: ${PKD_SOURCE_DIR}")

file (GLOB PKD_SOURCE_FILES "${PKD_SOURCE_DIR}/*.c")
add_library (pkd SHARED "${PKD_SOURCE_FILES}")
target_include_directories (pkd PRIVATE "${PKD_INCLUDE_DIR}")

set_target_properties (pkd PROPERTIES PREFIX "")
if (NOT WIN32)
    set_target_properties (pkd PROPERTIES SUFFIX ".so")
endif()

# Add Python include/linker flags
target_include_directories (pkd PRIVATE "${Python_INCLUDE_DIRS}")
target_link_libraries (pkd PRIVATE "${Python_LIBRARIES}")

# Add OpenMP linker flags
target_link_libraries (pkd PRIVATE "${OpenMP_C_FLAGS}")
target_compile_options (pkd PRIVATE "${OpenMP_C_FLAGS}")