from setuptools import find_packages, setup

from rave_python import __version__

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rave_python",
    version=__version__,
    author="Flutterwave",
    author_email="developers@flutterwavego.com",
    description="Python library for Flutterwave for Business (F4B) v2 APIs.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flutterwave/rave-python",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "pycryptodome>=3.10.0",
        "requests>=2.20.0",
    ],
)
