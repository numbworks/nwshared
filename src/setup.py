import nwshared as nwsh
from setuptools import setup

setup(
    name = nwsh.MODULE_NAME,
    version = nwsh.MODULE_VERSION,
    description = nwsh.MODULE_DESCRIPTION,
    author = nwsh.MODULE_AUTHOR,
    url = nwsh.MODULE_URL,
    install_requires = [
        "matplotlib",
        "numpy",
        "pandas"
    ]
)