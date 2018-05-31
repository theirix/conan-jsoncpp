#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from bincrafters import build_template_default

if __name__ == "__main__":
    os.environ["CONAN_USERNAME"] = os.getenv("CONAN_USERNAME", "theirix")
    os.environ["CONAN_LOGIN_USERNAME"] = os.getenv("CONAN_LOGIN_USERNAME", "theirix")
    os.environ["CONAN_UPLOAD"] = os.getenv("CONAN_UPLOAD", "https://api.bintray.com/conan/theirix/conan-repo")
    builder = build_template_default.get_builder(pure_c=False)
    builder.run()
