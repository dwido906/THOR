# CMakeLists.txt for VRBLL botsystem module
add_library(botsystem STATIC botsystem.c)
target_include_directories(botsystem PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
