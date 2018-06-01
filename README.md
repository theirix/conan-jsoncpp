[ ![Download](https://api.bintray.com/packages/theirix/conan-repo/jsoncpp%3Atheirix/images/download.svg) ](https://bintray.com/theirix/conan-repo/jsoncpp%3Atheirix/_latestVersion)
[![Build Status](https://travis-ci.org/theirix/conan-jsoncpp.svg)](https://travis-ci.org/theirix/conan-jsoncpp)
[![Build status](https://ci.appveyor.com/api/projects/status/2tpjv6nibq4o0ogk?svg=true)](https://ci.appveyor.com/project/theirix/conan-jsoncpp)

# conan-jsoncpp

[Conan.io](https://conan.io) package for [jsoncpp](https://github.com/open-source-parsers/jsoncpp) library

The packages generated with this **conanfile** can be found in [bintray](https://bintray.com/theirix/conan-repo/jsoncpp%3Atheirix).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Reuse the packages

### basic setup

    $ conan install jsoncpp/1.0.0@theirix/stable

### Prerequirements

    JsonCpp needs at least cmake 3.1 for building.
    If you do not have one, specify flag jsoncpp:use_cmake_installer=True
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    jsoncpp/1.0.0@theirix/stable

    [options]
    jsoncpp:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
