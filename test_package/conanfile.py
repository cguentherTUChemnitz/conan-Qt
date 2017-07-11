from conans import ConanFile, CMake
from conans.tools import os_info, SystemPackageTool
import os, platform

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "dev")
username = os.getenv("CONAN_USERNAME", "cguenther")

class QtLibTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "Qt/5.9.0@%s/%s" % (username, channel)
    generators = "cmake"
    default_options = "Qt:xkbcommon-x11=qt", \
                      "Qt:xcb=qt", "Qt:opengl=desktop", \
                      "Qt:gif=yes", "Qt:libpng=qt", \
                      "Qt:doubleconversion=qt", \
                      "Qt:gui=yes", "Qt:widgets=yes", \
                      "Qt:freetype=qt", "Qt:harfbuzz=qt" \

    def system_requirements(self):
        if os_info.linux_distro == "Arch":
            installer = SystemPackageTool()
            installer.update() # Update the package database
            installer.install(mingw-w64-gcc) # Install the package
            installer.install(wine) # Install the package

    def build(self):
        self.isMingwCrosscompilation = platform.system() == "Linux" and \
                                  self.settings.os == "Windows" and \
                                  self.settings.compiler in ["gcc", "g++", "clang"]
        self.run("mkdir -p build")
        cmake = CMake(self.settings)
        self.run('cd build && cmake "%s" %s' % (self.conanfile_directory, cmake.command_line + "-DMingwLinuxToWindowsCrossCompilation=on" if self.isMingwCrosscompilation else " "))
        self.run("cd build && cmake --build . %s" % cmake.build_config)

    def test(self):
        self.isMingwCrosscompilation = platform.system() == "Linux" and \
                                  self.settings.os == "Windows" and \
                                  self.settings.compiler in ["gcc", "g++", "clang"]

        if self.isMingwCrosscompilation:
            self.run("cd build/bin && wine " + os.sep.join([".", "qtlibtest.exe"]) )
        else:
            self.run("cd build/bin && " + os.sep.join([".", "qtlibtest"]) )
