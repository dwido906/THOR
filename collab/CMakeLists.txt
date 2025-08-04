# CMakeLists.txt for VRBLL collab module
add_library(collab STATIC collab.c)
target_include_directories(collab PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
