from conans import ConanFile, CMake
from conans.tools import download, untargz, check_sha1, replace_in_file
import os
import shutil

class JsoncppConan(ConanFile):
    name = "jsoncpp"
    version = "1.7.7"
    url = "https://github.com/theirix/conan-jsoncpp"
    license = "https://github.com/open-source-parsers/jsoncpp/blob/master/LICENSE"
    FOLDER_NAME = 'jsoncpp-%s' % version
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports = "CMakeLists.txt"
    generators = "cmake", "txt"

    def source(self):
        tarball_name = self.FOLDER_NAME + '.tar.gz'
        download("https://github.com/open-source-parsers/jsoncpp/archive/%s.tar.gz" % self.version, tarball_name)
        check_sha1(tarball_name, "7bbb47e25b3aa7c4c8b579ca46b32d55f32cb46e")
        untargz(tarball_name)
        os.unlink(tarball_name)
        shutil.move("%s/CMakeLists.txt" % self.FOLDER_NAME, "%s/CMakeListsOriginal.cmake" % self.FOLDER_NAME)
        shutil.move("CMakeLists.txt", "%s/CMakeLists.txt" % self.FOLDER_NAME)

    def build(self):

        cmake = CMake(self.settings)

        # compose cmake options
        extra_command_line = '-DJSONCPP_WITH_CMAKE_PACKAGE=ON -DJSONCPP_WITH_TESTS=OFF'
        if self.options.shared:
            extra_command_line += " -DBUILD_SHARED_LIBS=ON -DBUILD_STATIC_LIBS=OFF"
        else:
            extra_command_line += " -DBUILD_SHARED_LIBS=OFF -DBUILD_STATIC_LIBS=ON"

        cmd = 'cmake %s/%s %s %s' % (self.conanfile_directory, self.FOLDER_NAME, cmake.command_line, extra_command_line)
        self.output.warn('Running CMake: ' + cmd)
        self.run(cmd)
        self.run("cmake --build . %s" % cmake.build_config)

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
