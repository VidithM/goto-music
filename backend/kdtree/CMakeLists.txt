if (NOT WIN32)
# Set compiler paths below, or comment out to use default compiler
set (CMAKE_C_COMPILER "/usr/local/bin/gcc")
set (CMAKE_CXX_COMPILER "/usr/local/bin/g++")
endif ()

cmake_minimum_required (VERSION 3.0)
project (pkd)

find_package (Python REQUIRED COMPONENTS Development)
find_package (OpenMP REQUIRED)

add_library (pkd SHARED module.c)

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