import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rave_python",
    version="1.0.0",
    author="Flutterwave",
    author_email="developers@flutterwavego.com",
    description="Official Rave Python Wrapper By Flutterwave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flutterwave/rave-python",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = [
        'pycryptodome',
        'requests'
    ]
)