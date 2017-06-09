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
                      "Qt:freetype=qt", "Qt:harfbuzz=qt"

    def system_requirements(self):
        if os_info.linux_distro == "Arch":
            installer = SystemPackageTool()
            installer.update() # Update the package database
            installer.install(mingw-w64-gcc) # Install the package
            installer.install(wine) # Install the package

    def build(self):
        self.run("mkdir -p build")
        cmake = CMake(self.settings)
        self.run('cd build && cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cd build && cmake --build . %s" % cmake.build_config)
        if platform.system() == "Linux":
            self._build_crossCompile()

    def _build_crossCompile(self):
        self.run("mkdir -p build-win64")
        cmake = CMake(self.settings)
        self.run('cd build && cmake "%s" %s' % (self.conanfile_directory, cmake.command_line + "-DMingwLinuxToWindowsCrossCompilation=on"))
        self.run("cd build && cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run("cd build/bin && " + os.sep.join([".", "qtlibtest"]) )
        # if platform.system() == "Linux":
        # TODO: there are missing libs here
        #     self.run("cd build-win64/bin && wine" + os.sep.join([".", "qtlibtest.exe"]) )
