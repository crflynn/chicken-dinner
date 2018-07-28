"""Setup."""
import io
from os import path
from setuptools import setup
from setuptools import find_packages


here = path.abspath(path.dirname(__file__))


# io.open for py27
with io.open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


# import __version__ attributes
about = {}
with open(path.join(here, "chicken_dinner", "__version__.py")) as f:
    exec(f.read(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    url=about["__url__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    license=about["__license__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords="pubg api wrapper playback animation chicken dinner",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    extras_require={
        "visual": [
            "matplotlib",
            "pillow",
        ]
    },
    include_package_data=True,
    package_data={
        "": ["*lowres.jpg", "dictionary.json"]
    },
    zip_safe=False,
)
