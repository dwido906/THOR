# CMakeLists.txt for VRBLL aimoderation module
add_library(aimoderation STATIC aimoderation.c)
target_include_directories(aimoderation PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
