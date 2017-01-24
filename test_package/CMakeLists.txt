project(qtlibtest)
cmake_minimum_required(VERSION 3.0.2)

#execute conan to install / build the dependencies
execute_process(COMMAND /usr/bin/conan install ${PROJECT_SOURCE_DIR} )

#load dependencies and propagate flags
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(Qt5Core 5.8 REQUIRED)
find_package(Qt5Widgets 5.8 REQUIRED)

configure_file(qt.conf.in ${CMAKE_BINARY_DIR}/bin/qt.conf)
configure_file(DejaVuSans.ttf ${CMAKE_BINARY_DIR}/bin/DejaVuSans.ttf COPYONLY)

add_executable(qtlibtest main.cpp )
target_link_libraries(qtlibtest Qt5::Widgets )
