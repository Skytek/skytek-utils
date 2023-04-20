import re
from os import path

from setuptools import find_packages, setup


def long_description():
    with open("README.md", "r") as fh:
        return fh.read()


def get_about():
    """Parses __init__ on main module in search of all dunder names"""
    regex = re.compile(r"^__\w+__\s*=.*$")
    about = dict()
    with open("skytek_utils/__init__.py", "r") as f:
        dunders = list()
        for l in f.readlines():
            if regex.match(l):
                dunders.append(l)
        exec("\n".join(dunders), about)

    with open(path.join(path.dirname(__file__), "skytek_utils", "VERSION")) as f:
        about["__version__"] = f.read().strip()

    return about

about = get_about()


setup(
    name="skytek-utils",
    version=about["__version__"],
    description="skytek-utils - a set of small util functions",
    url="http://github.com/Skytek/skytek-utils",
    author=about["__author__"],
    author_email="wiktor.latanowicz@skytek.com",
    license="LGPLv3",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*",]),
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    test_suite="tests",
    include_package_data=True,
)
