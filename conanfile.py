from conans import ConanFile, CMake
from conans.tools import download, untargz, check_sha1, replace_in_file
import os
import shutil
from os import path

class JsoncppConan(ConanFile):
    name        = "jsoncpp"
    version     = "1.8.0"
    description = "A C++ library for interacting with JSON. "
    url         = "https://github.com/theirix/conan-jsoncpp"
    license     = "Public Domain or MIT (https://github.com/open-source-parsers/jsoncpp/blob/master/LICENSE)"
    FOLDER_NAME = 'jsoncpp-%s' % version
    settings    = "os", "compiler", "arch", "build_type"

    exports     = "CMakeLists.txt"
    generators  = "cmake", "txt"

    # Workaround for long cmake binary path
    short_paths = True

    options         = {
        "shared"    : [True, False],
        "use_pic"   : [True, False]
    }
    default_options = (
        "shared=False",
        "use_pic=False"
    )

    SHA1 = "40f7f34551012f68e822664a0b179e7e6cac5a97"

    requires = "cmake_installer/0.1@lasote/stable"

    def configure(self):
        if self.options.shared:
            self.options.use_pic = True

    def source(self):
        self.output.info("downloading source ...")

        tarball_name = self.FOLDER_NAME + '.tar.gz'
        download("https://github.com/open-source-parsers/jsoncpp/archive/%s.tar.gz" % self.version, tarball_name)
        check_sha1(tarball_name, self.SHA1)
        untargz(tarball_name)
        os.unlink(tarball_name)

        cmakefile = path.join(self.FOLDER_NAME, "CMakeLists.txt")
        shutil.move(cmakefile, path.join(self.FOLDER_NAME, "CMakeListsOriginal.cmake"))
        shutil.move("CMakeLists.txt", cmakefile)

    def build(self):
        cmake = CMake(self.settings)

        cmakefile_path = path.join(self.conanfile_directory, self.FOLDER_NAME)
        cmake_path = path.join(self.deps_cpp_info["cmake_installer"].bin_paths[0], 'cmake')

        cmd = '%s %s %s %s' % (cmake_path, cmakefile_path, cmake.command_line, self.cmake_options())
        self.output.info('Running CMake: ' + cmd)
        self.run(cmd)
        self.run("%s --build . %s" % (cmake_path, cmake.build_config))

    def package(self):
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

    def cmake_options(self):
        extra_command_line = '-DJSONCPP_WITH_CMAKE_PACKAGE=ON -DJSONCPP_WITH_TESTS=OFF'
        if self.options.shared:
            extra_command_line += " -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF"
        else:
            extra_command_line += " -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON"

        if self.options.use_pic:
            extra_command_line += " -DCMAKE_POSITION_INDEPENDENT_CODE=ON"

        return extra_command_line
