from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="theirix", channel="ci")
    builder.add_common_builds(shared_option_name="jsoncpp:shared", pure_c=False)
    for build in builder.builds:
        if build.settings["arch"] == "x86":
            build.settings["cmake_installer:arch"] = "x86_64"
    builder.run()
