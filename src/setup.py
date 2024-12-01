'''Contains packaging information about nwshared.py.'''

# GLOBAL MODULES
from setuptools import setup

# INFORMATION
MODULE_ALIAS : str = "nwsh"
MODULE_NAME : str = "nwshared"
MODULE_VERSION : str = "1.8.0"

# SETUP
setup(
    name = MODULE_NAME,
    version = MODULE_VERSION,
    description = "A collection of shared components.",
    author = "numbworks",
    url = "https://github.com/numbworks/nwshared",
    py_modules = [ MODULE_NAME ],
    install_requires = [
        "matplotlib>=3.9.2",
        "numpy>=2.1.2",
        "pandas>=2.2.3",
        "requests>=2.32.3",
        "jinja2>=3.1.4",
        "ipykernel==6.29.5"
    ],
    python_requires = ">=3.12",
    license = "MIT"
)