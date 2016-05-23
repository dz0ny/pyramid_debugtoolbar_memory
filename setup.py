"""pyramid_debugtoolbar_memory installation script.
"""
import os
from setuptools import setup
from setuptools import find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md")).read()
    README = README.split("\n\n", 1)[0] + "\n"
except:
    README = ''

requires = ['pyramid_debugtoolbar>=2.2', 'pympler']

setup(
    name="pyramid_debugtoolbar_memory",
    author="Janez Troha",
    author_email="dz0ny@ubuntu.si",
    url="https://github.com/dz0ny/pyramid_debugtoolbar_memory",
    version="0.0.1",
    description="memory support for pyramid_debugtoolbar",
    keywords="web pyramid",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    test_suite="tests",
)
