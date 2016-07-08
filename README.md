[![Build Status](https://travis-ci.org/theirix/conan-jsoncpp.svg)](https://travis-ci.org/theirix/conan-jsoncpp)

# conan-jsoncpp

[Conan.io](https://conan.io) package for [jsoncpp](https://github.com/open-source-parsers/jsoncpp) library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/jsoncpp/1.7.3/theirix/stable).

## Build packages

    $ pip install conan_package_tools
    $ python build.py
    
## Upload packages to server

    $ conan upload jsoncpp/1.7.3@theirix/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install jsoncpp/1.7.3@theirix/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    jsoncpp/1.7.3@theirix/stable

    [options]
    jsoncpp:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
