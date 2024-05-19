from setuptools import setup, find_packages

setup(
    name = "nwshared",
    version = "1.1.0",
    description = "A collection of shared components.",
    author = "numbworks",
    url = "https://github.com/numbworks/nwshared",
    packages = find_packages(),
    install_requires = [
        "matplotlib>=3.8.2",
        "numpy>=1.26.3",
        "pandas>=2.2.0"
    ],
    python_requires = ">=3.12"
)