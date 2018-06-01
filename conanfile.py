#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class JsoncppConan(ConanFile):
    name        = "jsoncpp"
    version     = "1.0.0"
    description = "A C++ library for interacting with JSON."
    url         = "https://github.com/theirix/conan-jsoncpp"
    license     = "Public Domain or MIT (https://github.com/open-source-parsers/jsoncpp/blob/master/LICENSE)"
    homepage    = "https://github.com/open-source-parsers/jsoncpp"
    author      = "theirix"
    settings    = "os", "compiler", "arch", "build_type"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators  = "cmake"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = ("shared=False", "fPIC=True")
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove('fPIC')

    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['JSONCPP_WITH_CMAKE_PACKAGE'] = True
        cmake.definitions['JSONCPP_WITH_TESTS'] = False
        cmake.definitions['JSONCPP_WITH_PKGCONFIG_SUPPORT'] = False
        # since 1.6.5
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_STATIC_LIBS'] = not self.options.shared
        # before 1.6.5
        cmake.definitions['JSONCPP_LIB_BUILD_SHARED'] = self.options.shared
        cmake.configure(build_folder=self.build_subfolder)
        return cmake

    def build(self):
        if self.settings.compiler == "Visual Studio" and self.settings.compiler.version == "11":
            tools.replace_in_file(os.path.join(self.source_subfolder, "include", "json", "value.h"),
                                  "explicit operator bool()",
                                  "operator bool()")
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", src=self.source_subfolder, dst="licenses")
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
