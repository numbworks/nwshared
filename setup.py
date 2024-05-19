from setuptools import setup

setup(
    name = "nwshared",
    version = "1.1.0",
    description = "A collection of shared components.",
    author = "numbworks",
    url = "https://github.com/numbworks/nwshared",
    packages = [ "nwshared" ],
    install_requires = [
        "matplotlib",
        "numpy",
        "pandas"
    ]
)