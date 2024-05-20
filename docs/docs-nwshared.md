# nwshared
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2024-05-19 | numbworks | Created. |

## Introduction

`nwshared` is a collection of shared components for Python modules.

## Getting Started

In order to edit the `src/nwshared.py` module:

1. Download and install [Python 3.x](https://www.python.org/downloads/);
      - This has been tested with the following Python version: `3.12.1`
2. Download and install [Visual Studio Code](https://code.visualstudio.com/Download);
3. Open a terminal and run the following commands:
    - ```python.exe -m pip install --upgrade pip```
4. Launch Visual Studio Code and open `src/nwshared.py`;
5. Done!

In order to import the `src/nwshared.py` module in other projects:

1. Install [Git for Windows](https://git-scm.com/download/win);
2. Open `Windows Powershell` (or `Windows Terminal` or similar) and type:

```powershell
PS C:\> pip install -e 'git+https://github.com/numbworks/nwshared.git#egg=nwshared&subdirectory=src'
```

3. launch the Python interpreter:

```powershell
PS C:\> python
```

4. try out if the module has been correctly installed by executing the following snippet of code:

```python
from nwshared import VersionChecker

vc : VersionChecker = VersionChecker()
print(vc.get_python_version_status())
```

5. Done!

## For Developers

To run the unit tests, open a terminal and run the following commands:

- `cd <base_folder>\nwshared\tests`
- `coverage run -m unittest nwsharedtests.py`
- `coverage report`

To enable the unit test runner in `Visual Studio Code`:

1. create a `.vscode` folder in `cd <base_folder>\nwshared\`;
2. add a `settings.json` file and paste the following content in it:

  ```json
  {
      "python.testing.unittestArgs": [
          "-v",
          "-s",
          "./tests",
          "-p",
          "*tests.py"
      ],
      "python.testing.pytestEnabled": false,
      "python.testing.unittestEnabled": true
  }  
  ```
3. save the file and close `Visual Studio Code`;
4. open `Visual Studio Code` -> `File` -> `Open Folder` and select `cd <base_folder>\nwshared\`;
5. if the testing icon doesn't appear on the sidebar, just open whatever `*.py` file;
6. Done!

To run type checking:

- `cd <base_folder>\nwshared\`
- `mypy src --disable-error-code import-untyped --disable-error-code func-returns-value --disable-error-code import-untyped --disable-error-code annotation-unchecked`
- `mypy tests --disable-error-code import-untyped --disable-error-code func-returns-value --disable-error-code import-untyped --disable-error-code annotation-unchecked`

In order to perform development work on this project in a comfortable way, you might want to enable the auto-reload / auto-refresh of the content of `Python` modules used in `Jupyter Notebook`:

1.	`Visual Studio Code` > `File` > `Preferences` > `Settings`;
2.	Search for the following setting and change it as below:

  ```json
    "jupyter.runStartupCommands": [
        "%load_ext autoreload", "%autoreload 2"
    ]
  ```

3.	Done!

## Known Issues - Python 3.12.x on Ubuntu 24.04 LTS

I used a machine with `Ubuntu 24.04 LTS` to try out the module installation in a clean environment. `Ubuntu 24.04 LTS` offers `Python 3.12.x` as default Python interpreter (which it's good), but it suggests to use virtual environments to install extra packages on the machine.

In order to do so, please run the following commands:

```sh
sudo apt install python3-venv -y
python3 -m venv venv_nwshared
source venv_nwshared/bin/activate
```

Once you are in the virtual environment, you can proceed installing the package:

```sh
pip install -e 'git+https://github.com/numbworks/nwshared.git#egg=nwshared&subdirectory=src'
```

Other useful commands:

```sh
deactivate
pip uninstall nwshared
pip list
pip show nwshared
```

## Known Issues - "Import nwshared could not be resolved Pylance (reportMissingImports)"

If while trying to import `nwshared` in `Visual Studio Code` the following warning appears:

```
Import nwshared could not be resolved Pylance (reportMissingImports)
```

please:

1. in `Windows Terminal` (or similar), launch the Python interpreter:

```powershell
PS C:\> python
```

2. run the following command:

```python
import nwshared
print(nwshared.__file__)
```

3. the console will output something like this:

```
C:\Users\Rubèn\src\nwshared\src\nwshared.py
```

4. open `Visual Studio Code` > `File` > `Preferences` > `Settings` and search for `Python › Analysis: Extra Paths`;

5. click on `Add item` and add the path above without the python file name: 

```
C:\Users\Rubèn\src\nwshared\src\
```

6. restart `Visual Studio Code`;
7. Done!

## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)