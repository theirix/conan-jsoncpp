project(testapp)
cmake_minimum_required(VERSION 2.8.12)

add_definitions(-std=c++11)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(testapp testapp.cxx)
target_link_libraries(testapp ${CONAN_LIBS})

