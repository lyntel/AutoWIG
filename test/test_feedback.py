##################################################################################
#                                                                                #
# AutoWIG: Automatic Wrapper and Interface Generator                             #
#                                                                                #
# Homepage: http://autowig.readthedocs.io                                        #
#                                                                                #
# Copyright (c) 2016 Pierre Fernique                                             #
#                                                                                #
# This software is distributed under the CeCILL license. You should have       #
# received a copy of the legalcode along with this work. If not, see             #
# <http://www.cecill.info/licences/Licence_CeCILL_V2.1-en.html>.                 #
#                                                                                #
# File authors: Pierre Fernique <pfernique@gmail.com> (5)                        #
#                                                                                #
##################################################################################

import autowig

import unittest
from nose.plugins.attrib import attr

import subprocess
from path import path

@attr(linux=True,
      osx=True,
      win=False,
      level=1)
class TestFeedback(unittest.TestCase):
    """Test the feedback of a SCons results"""

    @classmethod
    def setUpClass(cls):
        with open('test.h', 'w') as filehandler:
            filehandler.write("""
#include <string>

namespace test
{
    template<class T, class U>
    class Pair
    {
        public:
            Pair(const std::string& first, const std::string& second)
            { 
                this->first = first;
                this->second = second;
            };

            void swap(const Pair< T, U >& pair)
            { this->first = pair.first; this->second = pair.second; }

        protected:
            T first;
            U second;
    };

    typedef Pair< const double, double > Point;

    enum {
        RED,
        GREEN,
        BLUE
    };

    int color;
}""")

        with open('SConstruct', 'w') as filehandler:
            filehandler.write("""
from distutils import sysconfig
import sys

variables = Variables()

env = Environment()
variables.Update(env)

env.AppendUnique(LIBS = ['boost_python', 'python' + sysconfig.get_python_version()])
env.AppendUnique(CPPPATH = [sysconfig.get_python_inc()])
env.AppendUnique(CPPDEFINES = ['BOOST_PYTHON_DYNAMIC_LIB'])

env.Prepend(CPPPATH=sys.prefix + '/include')
env.Prepend(CPPPATH='.')
env.Prepend(LIBPATH=sys.prefix + '/lib')

env.AppendUnique(CXXFLAGS = ['-x', 'c++',
                             '-std=c++0x',
                             '-Wwrite-strings'])

pyenv = env.Clone()
#pyenv.AppendUnique(LIBS = ['basic'])
pyenv.AppendUnique(CXXFLAGS = ['-ftemplate-depth-100'])

wrap = pyenv.LoadableModule('_module', pyenv.Glob('wrapper_*.cpp') + ['_module.cpp'],
                            LDMODULESUFFIX = '.so',
                            FRAMEWORKSFLAGS = '-flat_namespace -undefined suppress')
Alias("py", wrap)
Alias("build", wrap)

Default("build")
""")
        autowig.parser.plugin = 'pyclanglite'
        autowig.generator.plugin = 'boost_python_internal'
        autowig.feedback.plugin = 'edit'
        cls.srcdir = path('.').abspath()

    def test_with_none_overload_export(self, overload="none"):
        """Test `feedback` with 'none' overload"""

        for wrapper in self.srcdir.walkfiles('wrapper_*.cpp'):
            wrapper.unlink()
        wrapper = self.srcdir/'_module.h'
        if wrapper.exists():
            wrapper.unlink()
        wrapper = self.srcdir/'_module.py'
        if wrapper.exists():
            wrapper.unlink()
        wrapper = self.srcdir/'_module.cpp'
        if wrapper.exists():
            wrapper.unlink()

        asg = autowig.AbstractSemanticGraph()

        asg = autowig.parser(asg, [self.srcdir/'test.h'],
                                  ['-x', 'c++', '-std=c++11', '-I' + str(self.srcdir)],
                                  silent = True)

        autowig.controller.plugin = 'default'
        autowig.controller(asg, overload=overload)

        module = autowig.generator(asg, module = self.srcdir/'_module.cpp',
                                     decorator = self.srcdir/'_module.py',
                                     prefix = 'wrapper_')

        from autowig._controller import cleaning
        cleaning(asg)

        module.write()


        s = subprocess.Popen(['scons', 'py'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        prev, curr = s.communicate()

        while not prev == curr:
            prev = curr
            code = autowig.feedback(curr, '.', asg)
            if code:
                exec(code, locals())

    @attr(level=2)
    def test_with_all_overload_export(self):
        """Test `feedback` with 'all' overload"""
        self.test_with_none_overload_export(overload="all")

    @attr(level=2)
    def test_with_class_overload_export(self):
        """Test `feedback` with 'class' overload"""
        self.test_with_none_overload_export(overload="class")

    @attr(level=2)
    def test_with_namespace_overload_export(self):
        """Test `feedback` with 'namespace' overload"""
        self.test_with_none_overload_export(overload="namespace")