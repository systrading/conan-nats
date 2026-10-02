from conans import ConanFile, CMake, tools
import os
import re


class NatsCConan(ConanFile):
    name = "nats.c"
    version = "3.13.0"
    description = "A C client for the NATS messaging system"
    topics = ("conan", "nats.c", "communication", "messaging", "protocols")
    url = "https://github.com/systrading/conan-nats"
    homepage = "https://github.com/nats-io/nats.c"
    license = "https://github.com/nats-io/nats.c/blob/master/LICENSE"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake", "cmake_find_package"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "no_spin": [True, False],
        "tls": [True, False],
        "tls_force_host_verify": [True, False],
        "streaming": [True, False],
    }
    default_options = {
        "shared": False,
        "no_spin": False,
        "tls": False,
        "tls_force_host_verify": False,
        "streaming": False
    }
    _source_subfolder = "source_subfolder"

    def requirements(self):
        if self.options.tls:
            self.requires("openssl/[>=3.0.0]")

    def source(self):
        sha256 = "f6ec9ee2ab367594b56dd3265e3561074ade7c3d7410a6f45a77704c5e537024"
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = "-".join([self.name, self.version])
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["NATS_BUILD_NO_SPIN"] = self.options.no_spin
        cmake.definitions["NATS_BUILD_WITH_TLS"] = self.options.tls
        cmake.definitions["NATS_BUILD_STREAMING"] = self.options.streaming
        cmake.definitions["NATS_BUILD_TLS_FORCE_HOST_VERIFY"] = self.options.tls_force_host_verify
        cmake.definitions["NATS_BUILD_LIB_STATIC"] = not self.options.shared
        cmake.definitions["NATS_BUILD_EXAMPLES"] = False
        cmake.definitions["NATS_BUILD_STATIC_EXAMPLES"] = not self.options.shared
        cmake.definitions["NATS_BUILD_LIB_SHARED"] = self.options.shared
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
