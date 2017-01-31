OPTION(MingwLinuxToWindowsCrossCompilation "Build windows binary using linux mingw cross compiler " OFF)
if(MingwLinuxToWindowsCrossCompilation)
   set(CMAKE_TOOLCHAIN_FILE /usr/share/mingw/toolchain-x86_64-w64-mingw32.cmake)
endif()

project(qtlibtest)
cmake_minimum_required(VERSION 3.0.2)

#execute conan to install / build the dependencies
# execute_process(COMMAND /usr/bin/conan install ${PROJECT_SOURCE_DIR} )
execute_process(COMMAND /usr/bin/conan install ${PROJECT_SOURCE_DIR} -s os=Windows )

#load dependencies and propagate flags
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# set (CMAKE_PREFIX_PATH ${CONAN_LIB_DIRS_QT}/cmake/)
set(Qt5Core_DIR /home/cguenther/.conan/data/Qt/5.8/cguenther/testing/package/505f0d3dea76fb05616d5d4b1fac667d75fb9f32/lib/cmake/Qt5Core)
set(Qt5Widgets_DIR /home/cguenther/.conan/data/Qt/5.8/cguenther/testing/package/505f0d3dea76fb05616d5d4b1fac667d75fb9f32/lib/cmake/Qt5Widgets)
set(Qt5Gui_DIR /home/cguenther/.conan/data/Qt/5.8/cguenther/testing/package/505f0d3dea76fb05616d5d4b1fac667d75fb9f32/lib/cmake/Qt5Gui)

find_package(Qt5Core 5.8 REQUIRED)
find_package(Qt5Widgets 5.8 REQUIRED)

configure_file(qt.conf.in ${CMAKE_BINARY_DIR}/bin/qt.conf)
configure_file(DejaVuSans.ttf ${CMAKE_BINARY_DIR}/bin/DejaVuSans.ttf COPYONLY)

add_executable(qtlibtest main.cpp )
target_link_libraries(qtlibtest Qt5::Widgets )
