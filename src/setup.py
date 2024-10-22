'''Contains packaging information about nwshared.py.'''

# GLOBAL MODULES
from setuptools import setup

# INFORMATION
MODULE_ALIAS : str = "nwsh"
MODULE_NAME : str = "nwshared"
MODULE_VERSION : str = "1.5.0"

# SETUP
setup(
    name = MODULE_NAME,
    version = MODULE_VERSION,
    description = "A collection of shared components.",
    author = "numbworks",
    url = "https://github.com/numbworks/nwshared",
    py_modules = [ MODULE_NAME ],
    install_requires = [
        "matplotlib>=3.8.2",
        "numpy>=1.26.3",
        "pandas>=2.2.0",
        "requests>=2.32.3",
        "jinja2>=3.1.4"
    ],
    python_requires = ">=3.12",
    license = "MIT"
)