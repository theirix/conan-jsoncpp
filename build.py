from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="jsoncpp:shared", pure_c=False)
    for settings, options in builder.builds:
        if settings["arch"] == "x86":
            settings["cmake_installer:arch"] = "x86_64"
    builder.run()
