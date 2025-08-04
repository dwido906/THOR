# CMakeLists.txt for VRBLL localfirst module
add_library(localfirst STATIC localfirst.c)
target_include_directories(localfirst PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
