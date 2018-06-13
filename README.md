# conan-Qt
Work in progress for fully configurable Qt package for conan. Standard config is optimized for low amount of dependencies and most possible amount of optimization.

The design goal was to handle a manual copy of (nearly) all qt configuration options and provide them to the conan options interface.

The default configuration behaves as follows:
 - disable as most as possible (Qt modules and external dependencies)
 - enable as most as possible optimizations
 - prefere the qt provided libs, where needed.

The goal was to create a qt conan package which is small (especially interesting for shared linking) and ships only stuff you really need for your project. This package is actively used for linux compilation and cross-compilation for windows. Sadly it is tested only by a small set of configuration options and the compilation path for mac OS is not present.
