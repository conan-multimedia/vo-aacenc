from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
from shutil import copyfile
import os

class VoaacencConan(ConanFile):
    name = "vo-aacenc"
    version = "0.1.3"
    description = "This library contains an encoder implementation of the Advanced Audio Coding (AAC) audio codec"
    url = "https://github.com/conan-multimedia/vo-aacenc"
    homepage = 'https://github.com/mstorsjo/vo-aacenc'
    license = "Apachev2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    source_subfolder = "source_subfolder"

    def source(self):
        #tools.get('http://downloads.sourceforge.net/project/opencore-amr/{name}/{name}-{version}.tar.gz'.format(name=self.name,version=self.version))
        tools.get('https://github.com/mstorsjo/{name}/archive/v{version}.tar.gz'.format(name=self.name,version=self.version))
        extracted_dir = self.name + '-' + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            self.run("autoreconf -f -i")

            _args = ["--prefix=%s/builddir"%(os.getcwd())]
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            autotools = AutoToolsBuildEnvironment(self)
            autotools.configure(args=_args)
            autotools.make(args=["-j4"])
            autotools.install()

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

