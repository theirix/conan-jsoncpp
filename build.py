from conan.packager import ConanMultiPackager
import copy
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="jsoncpp:shared", pure_c=False)

    builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        # skip mingw cross-builds
        if not (platform.system() == "Windows" and settings["compiler"] == "gcc" and settings["arch"] == "x86"):
            builds.append([settings, options, env_vars, build_requires])
    builder.builds = builds

    builder.run()
