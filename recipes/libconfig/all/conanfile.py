from conans import ConanFile, CMake, tools
import os
import textwrap


class LibconfigConan(ConanFile):
    name = "libconfig"
    license = "GNU LESSER GENERAL PUBLIC LICENSE"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "hyperrealm.github.io/libconfig/"
    description = "Libconfig is a simple library for processing structured configuration files. " \
                  "This file format is more compact and more readable than XML. And unlike XML, it is type-aware, " \
                  "so it is not necessary to do string parsing in application code."
    topics = ("libconfig", "structured", "configuration", "xml", "type")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": False}
    generators = "cmake"
    exports_sources = "*"
    no_copy_source = True

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("libconfig-%s" % self.version, "source_subfolder")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def build(self):
        tools.save(os.path.join(self.build_folder, "CMakeLists.txt"), textwrap.dedent("""\
            cmake_minimum_required(VERSION 2.8.12)
            project(cmake_wrapper)
            include("{}/conanbuildinfo.cmake")
            conan_basic_setup()
            add_subdirectory("{}/source_subfolder" libconfig)
            """).format(self.install_folder.replace("\\","/"), self.source_folder.replace("\\","/")))
        cmake = CMake(self)
        cmake.configure(source_folder=self.build_folder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.components["libconfig_c"].libs = ["libconfig" if self.settings.compiler == "Visual Studio" else "config"]
        if not self.options.shared:
            self.cpp_info.components["libconfig_c"].defines = ["LIBCONFIG_STATIC"]
        self.cpp_info.components["libconfig_c"].names["cmake_find_package"] = ["libconfig"]
        self.cpp_info.components["libconfig_c"].names["cmake_find_package_multi"] = ["libconfig"]
        self.cpp_info.components["libconfig_c"].names["pkg_config"] = "libconfig"
        self.cpp_info.components["libconfig_cpp"].libs = ["libconfig++" if self.settings.compiler == "Visual Studio" else "config++"]
        if not self.options.shared:
            self.cpp_info.components["libconfig_cpp"].defines = ["LIBCONFIGXX_STATIC"]
        self.cpp_info.components["libconfig_cpp"].names["cmake_find_package"] = ["libconfig++"]
        self.cpp_info.components["libconfig_cpp"].names["cmake_find_package_multi"] = ["libconfig++"]
        self.cpp_info.components["libconfig_cpp"].names["pg_config"] = "libconfig++"
