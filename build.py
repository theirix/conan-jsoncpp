from conan.packager import ConanMultiPackager
import copy

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds(shared_option_name="jsoncpp:shared", pure_c=False)

    builds = []
    for settings, options, env_vars, build_requires in builder.builds:
        new_settings = copy.copy(settings)
        if new_settings["arch"] == "x86":
            new_settings["cmake_installer:arch"] = "x86_64"
        builds.append([new_settings, options, env_vars, build_requires])
    builder.builds = builds

    builder.run()
