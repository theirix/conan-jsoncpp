from conans import ConanFile, CMake
from conans.tools import download, untargz, check_sha1
import os
import shutil

class JsoncppConan(ConanFile):
    name        = "jsoncpp"
    version     = "1.8.1"
    description = "A C++ library for interacting with JSON."
    url         = "https://github.com/theirix/conan-jsoncpp"
    license     = "Public Domain or MIT (https://github.com/open-source-parsers/jsoncpp/blob/master/LICENSE)"
    FOLDER_NAME = 'jsoncpp-%s' % version
    settings    = "os", "compiler", "arch", "build_type"

    exports     = "CMakeLists.txt"
    generators  = "cmake", "txt"

    # Workaround for long cmake binary path
    short_paths = True

    options = {
        "shared"              : [True, False],
        "use_pic"             : [True, False],
        "use_cmake_installer" : [True, False]
    }
    default_options = (
        "shared=False",
        "use_pic=False",
        "use_cmake_installer=False"
    )

    def configure(self):
        if self.options.shared:
            self.options.use_pic = True

    def requirements(self):
        if self.options.use_cmake_installer:
            self.requires.add("cmake_installer/0.1@lasote/stable", private=False)

    def source(self):
        self.output.info("downloading source ...")

        tarball_name = self.FOLDER_NAME + '.tar.gz'
        download("https://github.com/open-source-parsers/jsoncpp/archive/%s.tar.gz" % self.version, tarball_name)
        check_sha1(tarball_name, "c91541b2dcc575ff8004e69caa5d2360bd4d042a")
        untargz(tarball_name)
        os.unlink(tarball_name)

        cmakefile = os.path.join(self.FOLDER_NAME, "CMakeLists.txt")
        shutil.move(cmakefile, os.path.join(self.FOLDER_NAME, "CMakeListsOriginal.cmake"))
        shutil.move("CMakeLists.txt", cmakefile)

    def build(self):
        cmake = CMake(self.settings)

        if self.options.use_cmake_installer:
            cmake_path = os.path.join(self.deps_cpp_info["cmake_installer"].bin_paths[0], 'cmake')
        else:
            cmake_path = 'cmake'

        cmd = '%s %s %s %s' % (cmake_path, self.FOLDER_NAME, cmake.command_line, self.cmake_options())
        self.output.info('Running CMake: ' + cmd)
        self.run(cmd)
        self.run("%s --build . %s" % (cmake_path, cmake.build_config))

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
        # cmake_installer lib directory doesn't exist
        if self.options.use_cmake_installer and self.deps_cpp_info["cmake_installer"].libdirs:
            self.deps_cpp_info["cmake_installer"].libdirs = []

    def cmake_options(self):
        extra_command_line = '-DJSONCPP_WITH_CMAKE_PACKAGE=ON -DJSONCPP_WITH_TESTS=OFF'
        if self.options.shared:
            extra_command_line += " -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF"
        else:
            extra_command_line += " -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON"

        if self.options.use_pic:
            extra_command_line += " -DCMAKE_POSITION_INDEPENDENT_CODE=ON"

        return extra_command_line
