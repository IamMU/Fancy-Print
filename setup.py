from setuptools import setup, find_packages
import codecs
import os

VERSION = "0.0.1"
DESCRIPTION = "A aesthetic replacement to print()"
LONG_DESCRIPTION = "A replacement to print() with added features, such as alignment, seperators, responsivity, ..."

# Setting up
setup(
    name="fancyprint",
    version=VERSION,
    author="IamMU",
    author_email="iammu@duck.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["print", "log", "logger", "printer", "aesthic", "colorama"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
