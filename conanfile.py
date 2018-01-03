from conans import ConanFile, CMake, tools
import os
import shutil

class JsoncppConan(ConanFile):
    name        = "jsoncpp"
    version     = "1.8.3"
    description = "A C++ library for interacting with JSON."
    url         = "https://github.com/theirix/conan-jsoncpp"
    license     = "Public Domain or MIT (https://github.com/open-source-parsers/jsoncpp/blob/master/LICENSE)"
    homepage    = "https://github.com/open-source-parsers/jsoncpp"
    FOLDER_NAME = 'jsoncpp-%s' % version
    settings    = "os", "compiler", "arch", "build_type"

    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators  = "cmake", "txt"

    # Workaround for long cmake binary path
    short_paths = True

    options = {
        "shared"              : [True, False],
        "use_pic"             : [True, False]
    }
    default_options = (
        "shared=False",
        "use_pic=False"
    )

    def configure(self):
        if self.options.shared:
            self.options.use_pic = True

    def source(self):
        tools.get("https://github.com/open-source-parsers/jsoncpp/archive/%s.tar.gz" % self.version)

        cmakefile = os.path.join(self.FOLDER_NAME, "CMakeLists.txt")
        shutil.move(cmakefile, os.path.join(self.FOLDER_NAME, "CMakeListsOriginal.txt"))
        shutil.move("CMakeLists.txt", cmakefile)

    def build(self):
        cmake = CMake(self)

        cmake.definitions['JSONCPP_WITH_CMAKE_PACKAGE'] = True
        cmake.definitions['JSONCPP_WITH_TESTS'] = False
        cmake.definitions['BUILD_SHARED_LIBS'] = self.options.shared
        cmake.definitions['BUILD_STATIC_LIBS'] = not self.options.shared

        if self.options.use_pic:
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = True

        cmake.configure(source_dir=self.FOLDER_NAME, build_dir="./")
        cmake.build()

    def package(self):
        self.copy("license*", src="%s" % (self.FOLDER_NAME), dst="licenses", ignore_case=True, keep_path=False)
        self.copy("*.h", dst="include", src="%s/include" % (self.FOLDER_NAME))
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            elif self.settings.os == "Windows":
                self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
                self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", keep_path=False)
        else:
            if self.settings.os == "Windows":
                self.copy(pattern="*.lib", dst="lib", src="lib", keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['jsoncpp']
