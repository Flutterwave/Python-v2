import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rave_python",
    version="1.2.12",
    author="Flutterwave",
    author_email="developers@flutterwavego.com",
    description="Official Rave Python Wrapper By Flutterwave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flutterwave/rave-python",
    license="MIT",
    packages=setuptools.find_packages(),
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    classifiers=(
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = [
        'pycryptodome',
        'requests'
    ]
)