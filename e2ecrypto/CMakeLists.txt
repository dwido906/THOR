# CMakeLists.txt for VRBLL e2ecrypto module
add_library(e2ecrypto STATIC e2ecrypto.c)
target_include_directories(e2ecrypto PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(e2ecrypto sodium)
