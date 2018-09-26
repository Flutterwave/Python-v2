import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_rave",
    version="1.0.10-alpha",
    author="Tofunmi Kupoluyi",
    author_email="tofunmi@flutterwavego.com",
    description="A python wrapper for Flutterwave's Rave",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TofunmiKupoluyi/python_rave",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires = [
        # 'PyCrypto',
        'pycryptodome',
        'requests'
    ]
)