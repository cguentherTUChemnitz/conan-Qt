OPTION(MingwLinuxToWindowsCrossCompilation "Build windows binary using linux mingw cross compiler " OFF)
if(MingwLinuxToWindowsCrossCompilation)
   set(CMAKE_TOOLCHAIN_FILE ./toolchain-x86_64-w64-mingw32.cmake)
endif()

project(qtlibtest)
cmake_minimum_required(VERSION 3.0.2)

#execute conan to install / build the dependencies
if(MingwLinuxToWindowsCrossCompilation)
  execute_process(COMMAND /usr/bin/conan install ${PROJECT_SOURCE_DIR} -s os=Windows )
else()
  execute_process(COMMAND /usr/bin/conan install ${PROJECT_SOURCE_DIR} )
endif()


#load dependencies and propagate flags
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set (CMAKE_PREFIX_PATH ${CONAN_LIB_DIRS_QT}/cmake/)
#TODO: check why those pathes are not determined, when os=Windows
if(MingwLinuxToWindowsCrossCompilation)
 set(Qt5Core_DIR ${CONAN_LIB_DIRS_QT}/cmake/Qt5Core)
 set(Qt5Widgets_DIR ${CONAN_LIB_DIRS_QT}/cmake/Qt5Widgets)
 set(Qt5Gui_DIR ${CONAN_LIB_DIRS_QT}/cmake/Qt5Gui)
endif()

find_package(Qt5Core 5.8 REQUIRED)
find_package(Qt5Widgets 5.8 REQUIRED)

configure_file(qt.conf.in ${CMAKE_BINARY_DIR}/bin/qt.conf)
configure_file(DejaVuSans.ttf ${CMAKE_BINARY_DIR}/bin/DejaVuSans.ttf COPYONLY)

add_executable(qtlibtest main.cpp )
target_link_libraries(qtlibtest Qt5::Widgets )
