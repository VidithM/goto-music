if (NOT WIN32)
# Set compiler paths below, or comment out to use default compiler
set (CMAKE_C_COMPILER "/usr/local/bin/gcc")
set (CMAKE_CXX_COMPILER "/usr/local/bin/g++")
endif ()

cmake_minimum_required (VERSION 3.0)
project (ParallelKDTree)

find_package (Python REQUIRED COMPONENTS Development)
find_package (OpenMP REQUIRED)

add_library (ParallelKDTree SHARED module.c)

if (NOT WIN32)
set_target_properties (ParallelKDTree PROPERTIES SUFFIX ".so")
endif()

# Add Python include/linker flags
target_include_directories (ParallelKDTree PRIVATE "${Python_INCLUDE_DIRS}")
target_link_libraries (ParallelKDTree PRIVATE "${Python_LIBRARIES}")

# Add OpenMP linker flags
target_link_libraries (ParallelKDTree PRIVATE "${OpenMP_C_FLAGS}")
target_compile_options (ParallelKDTree PRIVATE "${OpenMP_C_FLAGS}")