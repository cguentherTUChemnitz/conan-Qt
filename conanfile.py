from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.tools import cpu_count
import platform
import os

class QtConan(ConanFile):
    name = "Qt"
    QtVersion = "5.10.1"
    PackageVersion = "1"
    version = QtVersion + "-" + PackageVersion
    sourceDir = "qt5"
    description = """This is a fully optionalized configured Qt library.
                     Most Qt config flags, as well as Qt modules can be set as compile options."""
    # settings = "os", "arch", "compiler", "build_type", "glibc_version"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/cguentherTUChemnitz/conan-Qt"
    license = "http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True
    isMingwCrosscompilation = False
    #platforms obtained from qt5/qtbase/mkspecs
    __platforms = ["auto-configured", "aix-g++", "aix-g++-64", "aix-xlc", "aix-xlc-64",
        "android-clang", "android-g++", "cygwin-g++", "darwin-g++", "freebsd-clang",
        "freebsd-g++", "haiku-g++", "hpux-acc", "hpux-acc-64", "hpux-acc-o64",
        "hpux-g++", "hpux-g++-64", "hpuxi-acc-32", "hpuxi-acc-64", "hpuxi-g++-64",
        "hurd-g++", "integrity-armv7", "integrity-armv7-imx6", "integrity-x86",
        "irix-cc", "irix-cc-64", "irix-g++", "irix-g++-64", "linux-arm-gnueabi-g++",
        "linux-clang", "linux-clang-libc++", "linux-cxx", "linux-g++", "linux-g++-32",
        "linux-g++-64", "linux-icc", "linux-icc-32", "linux-icc-64", "linux-kcc",
        "linux-llvm", "linux-lsb-g++", "linux-pgcc", "lynxos-g++", "macx-clang",
        "macx-clang-32", "macx-g++", "macx-g++-32", "macx-g++40", "macx-g++42",
        "macx-icc", "macx-ios-clang", "macx-llvm", "macx-tvos-clang", "macx-watchos-clang",
        "macx-xcode", "netbsd-g++", "openbsd-g++", "qnx-aarch64le-qcc", "qnx-armle-v7-qcc",
        "qnx-x86-64-qcc", "qnx-x86-qcc", "sco-cc" "sco-g++", "solaris-cc", "solaris-cc-64",
        "solaris-cc-64-stlport", "solaris-cc-stlport", "solaris-g++", "solaris-g++-64",
        "tru64-cxx", "tru64-g++", "unixware-cc", "unixware-g++",
        "win32-clang-msvc2015", "win32-g++", "win32-icc", "win32-msvc2005",
        "win32-msvc2008", "win32-msvc2010", "win32-msvc2012", "win32-msvc2013",
        "win32-msvc2015", "win32-msvc2017", "winphone-arm-msvc2013", "winphone-x86-msvc2013",
        "winrt-arm-msvc2013", "winrt-arm-msvc2015", "winrt-x64-msvc2013",
        "winrt-x64-msvc2015", "winrt-x86-msvc2013", "winrt-x86-msvc2015" ]
    #devices obtained from qt5/qtbase/mkspecs/devices
    # __devices = [ "common", "linux-archos-gen8-g++", "linux-arm-amlogic-8726M-g++",
    #     "linux-arm-generic-g++", "linux-arm-hisilicon-hix5hd2-g++",
    #     "linux-arm-trident-pnx8473-g++", "linux-beagleboard-g++",
    #     "linux-colibri-vf-g++", "linux-drive-cx-g++", "linux-imx53qsb-g++",
    #     "linux-imx6-g++", "linux-imx7-g++", "linux-jetson-tk1-g++",
    #     "linux-jetson-tk1-pro-g++", "linux-mipsel-broadcom-97425-g++",
    #     "linux-nuc-g++", "linux-odroid-xu3-g++", "linux-rasp-pi2-g++",
    #     "linux-rasp-pi-g++", "linux-rpi3-g++", "linux-rpi3-vc4-g++",
    #     "linux-sh4-stmicro-ST7108-g++", "linux-sh4-stmicro-ST7540-g++",
    #     "linux-snowball-g++", "linux-tegra2-g++" ]
    _qtConfigurationOptions = {
        #build options
        "gui" : ["no", "yes"], # gui support
        "widgets" : ["no", "yes"], # widgets support
        "accessibility" : ["yes", "no"],# Qt configure shows for "no": WARNING: Accessibility disabled. This configuration of Qt is unsupported.
        "optimized-tools" : ["no", "yes"], # TODO: why the configure note stated that it is not useful in release build?
        "separate-debug-info" : ["no", "yes"], # splits up debug info into seperate files
        "strip" : ["yes", "no"], # remove unnecessary symbols from libs
        "force-asserts" : ["no", "yes"],
        "shared" : ["yes", "no"], # shared or static linked lib
        "static" : ["no", "yes"], # shared or static linked lib
        "rpath" : ["yes", "no"],
        "reduce-exports" : ["yes", "no"],
        "reduce-relocations" : ["yes", "no"], # -pic flag to use relative jumps
        "pch" : ["yes", "no"], # precompiled headers
        "ltcg" : ["yes", "no"], # link time code generation
        #component selection
        #3rd party core options
        "doubleconversion" : ["qt", "system", "no"],
        "glib" : ["no", "yes"], # low-level system C library
        "eventfd" : ["no", "yes"],
        "inotify" : ["no", "yes"],
        "iconv" : ["no", "posix", "sun", "gnu"],  # convert between international codings
        "pcre" : ["qt", "system"],
        "zlib" : ["qt", "system"],
        #  logging backends
        "journald" : ["no", "yes"],
        "syslog" : ["no", "yes"],
        #3rd party network
        "ssl" : ["no", "yes"], # TODO: how does this flag interact with openssl?
        "sctp" : ["no", "yes"],
        "libproxy" : ["no", "yes"], # proxy configuration management
        "system-proxies" : ["yes", "no"], # use system procies for network access
        #3rd party gui, printing, widget
        "cups" : ["no", "yes"], # support for cups printer serve
        "fontconfig" : ["no", "yes"], # system font handling
        "freetype" : ["no", "qt", "system"],
        "harfbuzz" : ["no", "qt", "system"],
        "gtk" : ["no", "yes"], # gtk theming support
        "angle" : ["no", "yes"], # directx wrapper for opengl es
        "xcb-xlib" : ["no", "yes"],  # some X server and xlib stuff
        #3rd party platform backends
        "direct2d" : ["no", "yes"],
        "directfb" : ["no", "yes"], # direct frame buffer
        "eglfs" : ["no", "yes"], # embedded OpenGL backend
        "gbm" : ["no", "yes"], # generic buffer manager
        "kms" : ["no", "yes"], # kernel mode settings
        "linuxfb" : ["no", "yes"], # /dev/fb0 linux framebuffer
        "mirclient" : ["no", "yes"], # mir server client (ubuntu graphics server)
        "xcb" : ["no", "system", "qt"],
        #3rd party input backends
        "evdev" : ["no", "yes"], # mouse input handling for modern hardware
        "libinput" : ["no", "yes"], # inputhandling for X11, weston and wayland
        "mtdev" : ["no", "yes"], # multitouch device handling
        "tslib" : ["no", "yes"], # touchscreen access library
        "xinput2" : ["no", "yes"], # X server input handling
        "xkbcommon-x11" : ["no", "qt", "system"],
        "xkbcommon-evdev" : ["no", "yes"], # X server keyboard handling
        #3rd party image formats
        "gif" : ["no", "yes"], # gif image support
        "ico" : ["no", "yes"],
        "libpng" : ["no", "qt", "system"], # png image support
        "libjpeg" : ["no", "qt", "system"], # jpeg image support
        #database options
        "sqlite" : ["qt", "system"],
    }
    _spaceAssignmentOptions = {
        "c++std" : ["c++1z", "c++14", "c++11"], # c++ compiler version
        "qreal"  : ["double", "float"],
        #Qt platform abstraction list extracted from http://code.qt.io/cgit/qt/qtbase.git/tree/src/plugins/platforms
        "qpa" : ["xcb", "android", "bsdfb", "cocoa", "direct2d", \
                 "directfb", "eglfs", "haiku", "integrity", \
                 "ios", "linuxfb", "minimal", "minimalegl", "mirclient", \
                 "offscreen", "openwfd", "qnx", "vnc", "windows", "winrt"],
        "platform" : __platforms,
        "xplatform" : __platforms,
        # "device" : __devices,
    }
    _specialHandledOptions = {
        "sanitize" : ["no", "address", "thread", "memory", "undefined"], #TODO: how to handle appandable option values
        #component selection
        "dbus" : ["no", "linked", "runtime"], # linux interprozesskommunikation
        "openssl" : ["no", "linked", "runtime"], # openssl support # TODO: link against openssl is problematic in some countries
        #3rd party gui
        "opengl" : ["no", "desktop", "es2", "es3", "dynamic"], # opengl version #TODO: dynamic is windows only
        "icu" : ["no", "shared", "static"], # international components for unicode
    }
    _dbOptions = {
        #databse options
        "db2": ["no", "yes"],
        "ibase": ["no", "yes"],
        "mysql": ["no", "yes"], # TODO: define MYSQL_PATH
        "oci": ["no", "yes"],
        "odbc": ["no", "yes"],
        "psql": ["no", "yes"], # TODO: define PSQL_LIBS
        "sqlite2": ["no", "yes"],
        "sqlite": ["no", "yes"],
        "tds": ["no", "yes"],
    }
    _qtModules = {
        #"qtbase" : [True, False], # qt-base is implicit active
        "qt3d" : [False, True],
        "qtactiveqt" : [False, True],
        "qtandroidextras" : [False, True],
        "qtcanvas3d" : [False, True],
        "qtcharts" : [False, True],
        "qtconnectivity" : [False, True],
        "qtdatavis3d" : [False, True],
        "qtdeclarative" : [False, True],
        "qtdoc" : [False, True],
        "qtdocgallery" : [False, True],
        "qtenginio" : [False, True],
        "qtfeedback" : [False, True],
        "qtgamepad" : [False, True],
        "qtgraphicaleffects" : [False, True],
        "qtimageformats" : [False, True],
        "qtlocation" : [False, True],
        "qtmacextras" : [False, True],
        "qtmultimedia" : [False, True],
        "qtnetworkauth" : [False, True],
        "qtpim" : [False, True],
        "qtpurchasing" : [False, True],
        "qtqa" : [False, True],
        "qtquick1" : [False, True],
        "qtquickcontrols" : [False, True],
        "qtquickcontrols2" : [False, True],
        "qtremoteobjects" : [False, True],
        "qtrepotools" : [False, True],
        "qtscript" : [False, True],
        "qtscxml" : [False, True],
        "qtsensors" : [False, True],
        "qtserialbus" : [False, True],
        "qtserialport" : [False, True],
        "qtspeech" : [False, True],
        "qtsvg" : [False, True],
        "qtsystems" : [False, True],
        "qttools" : [False, True],
        "qttranslations" : [False, True],
        "qtvirtualkeyboard" : [False, True],
        "qtwayland" : [False, True],
        "qtwebchannel" : [False, True],
        "qtwebengine" : [False, True],
        "qtwebkit" : [False, True],
        "qtwebkit-examples" : [False, True],
        "qtwebsockets" : [False, True],
        "qtwebview" : [False, True],
        "qtwinextras" : [False, True],
        "qtx11extras" : [False, True],
        "qtxmlpatterns" : [False, True],
    }

    options = {**_qtConfigurationOptions, **_specialHandledOptions, **_qtModules, **_spaceAssignmentOptions, **_dbOptions}
    default_options = tuple("%s=%s" % (k, v[0]) for k, v in options.items())

    def requirements(self):
        if self.options.icu == "shared":
            self.requires("icu/57.1@annulen/testing")
            self.options["icu"].shared=True
        if self.options.icu == "static":
            #TODO: this functionality is blocked by https://bugreports.qt.io/browse/QTBUG-58301
            self.requires("icu/57.1@annulen/testing", "private")
            self.options["icu"].shared=False


    def source(self):
        self.run("git clone https://code.qt.io/qt/qt5.git")
        self.run("cd %s && git checkout %s" % (self.sourceDir, "v"+self.QtVersion))
        self.run("cd %s && perl init-repository -f --module-subset=qtbase" % self.sourceDir )

        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.sourceDir)

    def config_options(self):
        """
        change the configuration set based on the os setting
        """
        self.isMingwCrosscompilation = platform.system() == "Linux" and \
                                  self.settings.os == "Windows" and \
                                  self.settings.compiler in ["gcc", "g++"]

        if self.settings.os != "Linux":
            del self.options.iconv
            del self.options.journald
            del self.options.syslog
            del self.options.gtk
            del self.options.directfb
            del self.options.mirclient
        elif self.settings.os != "Windows":
            del self.options.qtactiveqt
            del self.options.angle
            del self.options.direct2d

        #TODO: delete, because of missing cross compiled packages
        if self.settings.os == "Windows":
            del self.options.rpath
            self.options.remove("reduce-exports")
            self.options.remove("reduce-relocations")
            self.options.qpa = "windows"
            self.options.xcb = "no"

        #handle debug only options
        if self.settings.build_type != "Debug":
            self.options.remove("separate-debug-info")

        #handle release only options
        if self.settings.build_type != "Release":
            self.options.remove("force-asserts")

        if self.options.freetype == "qt" and self.options.fontconfig == "yes":
            print ("Warning: Freetype is defined as bundled static linked copy and fontconfig is enbabled. \n" + \
                   "Fontconfig enforces systemlib Freetype! Therefore Freetype is now switched to system mode.")
            self.options.freetype = "system"

        #Qt has c++11 as a minimum requirements
        self.settings.compiler.libcxx = "libstdc++11"

        #linux to windows cross compilation
        if self.options.platform == "auto-configured":
            self.options.platform = self._determinePlatform(platform.system())
        if self.options.xplatform == "auto-configured":
            self.options.xplatform = self._determinePlatform(str(self.settings.os))

    def _determinePlatform(self, system: str) -> str :
        _gccArchitectureDecision = {"x86" : "linux-g++-32", "x86_64" : "linux-g++-64"}
        decisionMap = { "Linux" : {"clang" : "linux-clang-libc++",
                                   "gcc" : _gccArchitectureDecision,
                                   "g++" : _gccArchitectureDecision},
                        "Windows" : {"clang" : "win32-clang-msvc2015",
                                     "gcc" : "win32-g++",
                                     "g++" : "win32-g++"}
                      }
        return self._recursiveDictTraversal(decisionMap, system, str(self.settings.compiler), str(self.settings.arch))

    def _recursiveDictTraversal(self, potentialDict, *args):
        # print(potentialDict, args) TODO: use for debugging
        if not isinstance(potentialDict, dict) or not args:
            return potentialDict
        else:
            return self._recursiveDictTraversal(potentialDict[args[0]], *args[1:])

    def _generateQtConfig(self) -> list:
        # configuration independent args
        args = ["-silent", "-opensource", "-confirm-license", "-nomake examples", "-nomake tests",
                "-no-warnings-are-errors", "-prefix %s" % self.package_folder]

        if self.deps_cpp_info.include_paths:
            args.append("-I " + " ".join(self.deps_cpp_info.include_paths))
        if self.deps_cpp_info.defines:
            args.append("-D " + " ".join(self.deps_cpp_info.defines))
        if self.deps_cpp_info.lib_paths:
            args.append("-L " + " ".join(self.deps_cpp_info.lib_paths))
        if self.deps_cpp_info.lib_paths:
            args.append("-R " + " ".join(self.deps_cpp_info.lib_paths))

        # settings dependend args
        if self.settings.build_type == "Debug":
            args += ["-debug", "-qml-debug", "-optimize-debug"]
        else:
            args += ["-release", "-no-qml-debug"]

        # configuration dependend args
        args += ["-%s" % k if v == "yes" else "-%s-%s" % (v,k) for k, v in self.options.items() if k in self._qtConfigurationOptions ]
        args += ["-%s %s" % (k, v) for k, v in self.options.items() if k in self._spaceAssignmentOptions ]

        #special handled options
        args += ["-no-openssl" if self.options.openssl == "no" else
                 "-openssl-%s" % self.options.openssl]

        args += ["" if self.options.sanitize == "no" else
                 "-sanitize %s" % self.options.sanitize]
        args += ["-no-dbus" if self.options.dbus == "no" else
                 "-dbus-%s" % self.options.dbus]
        args += ["-no-opengl" if self.options.opengl == "no" else
                 "-opengl es2" if self.options.opengl == "es3" else
                 "-opengl %s" % self.options.opengl]
        args += ["-opengles3" if self.options.opengl == "es3" else ""]
        args += ["-sql-%s" % k if v == "yes" else "" for k, v in self.options.items() if k in self._dbOptions ]
        #special handled options encapsulating dependency options
        args += ["-icu" if self.options.icu in ["shared", "static"] else "-no-icu" ]

        # platform depended options
        #TODO: QMAKE_LINK_OBJECT_MAX is a dirty hack to avoid mri scripts, remove when following bug is solved:
        #https://sourceware.org/bugzilla/show_bug.cgi?id=21702 and https://bugreports.qt.io/browse/QTBUG-61335
        #TODO: allow-multiple-definition is a dirty hack to avoid multiple reference erros with LTO enabled for Windows:
        #https://sourceware.org/bugzilla/show_bug.cgi?id=12762
        if self.isMingwCrosscompilation:
            args += ["QMAKE_LINK_OBJECT_MAX=1000", "-device-option CROSS_COMPILE=x86_64-w64-mingw32-",
            "QMAKE_LFLAGS+=-Wl,-allow-multiple-definition"]

        return args

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        self.config_options()

        modules = "qtbase" + "".join([",%s" % k for k,v in self.options.items() if k in self._qtModules.keys() and v == "True"])
        self.run("cd %s && perl init-repository -f --module-subset=%s" % (self.sourceDir, modules) )

        args = self._generateQtConfig()

        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self.run("cd %s && ./configure%s %s" % (self.sourceDir, ".bat" if platform.system() == "Windows"  else " ", " ".join(args) ) )
            self.run("cd %s && make -Wno-error -j %s" % ( self.sourceDir, str(cpu_count())))

    def package(self):
        self.run("cd %s && make install -j %s" % (self.sourceDir, str(cpu_count())))
        fontsPath = os.path.join(self.package_folder, "lib", "fonts")
        os.makedirs(fontsPath)
        with open(os.path.join(fontsPath, "placeFontsHere.txt"), "w") as f:
            f.write("Fonts should be placed in this directory.")

    def package_info(self):
        #if reduce relocations is used, following binaries and libs must be build with -fPIC
        self.cpp_info.cppflags += ["-fPIC"]
        self.cpp_info.cflags += ["-fPIC"]
