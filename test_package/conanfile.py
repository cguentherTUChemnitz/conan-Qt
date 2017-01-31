from conans import ConanFile, CMake
import os

# This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "dev")
username = os.getenv("CONAN_USERNAME", "cguenther")

class QtLibTest(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "Qt/5.8.0@%s/%s" % (username, channel)
    generators = "cmake"
    default_options = "Qt:xkbcommon-x11=qt", \
                      "Qt:xcb=qt", "Qt:opengl=desktop", \
                      "Qt:gif=yes", "Qt:libpng=qt", \
                      "Qt:doubleconversion=qt", \
                      "Qt:gui=yes", "Qt:widgets=yes", \
                      "Qt:freetype=qt", "Qt:harfbuzz=qt"

    def build(self):
        self.run("mkdir -p build")
        cmake = CMake(self.settings)
        self.run('cd build && cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cd build && cmake --build . %s" % cmake.build_config)

    def test(self):
        self.run("cd build/bin && " + os.sep.join([".", "qtlibtest"]) )
