# nwshared
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2024-05-19 | numbworks | Created. |
| 2024-08-13 | numbworks | Updated to v1.2.0. |
| 2024-09-17 | numbworks | Updated to v1.3.0. |
| 2024-09-24 | numbworks | Updated to v1.4.0. |
| 2024-10-22 | numbworks | Updated to v1.5.0. |
| 2024-10-28 | numbworks | Updated to v1.6.0. |
| 2024-11-05 | numbworks | Updated to v1.7.0. |
| 2024-11-26 | numbworks | Updated to v1.7.1. |
| 2024-12-01 | numbworks | Updated to v1.8.0. |
| 2024-12-27 | numbworks | Updated to v1.8.1. |
| 2025-05-26 | numbworks | Updated to v1.8.2. |

## Introduction

`nwshared` is a collection of shared components for Python modules.

## Getting Started

To run this application on Windows and Linux:

1. Download and install [Visual Studio Code](https://code.visualstudio.com/Download);
2. Download and install [Docker](https://www.docker.com/products/docker-desktop/);
3. Download and install [Git](https://git-scm.com/downloads);
4. Open your terminal application of choice and type the following commands:

    ```
    mkdir nwshared
    cd nwshared
    git clone https://github.com/numbworks/nwshared.git
    ```

5. Launch Visual Studio Code and install the following extensions:

    - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    - [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)
    - [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter)
    - [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
    - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

6. In order for the Jupyter Notebook to automatically detect changes in the underlying library, click on <ins>File</ins> > <ins>Preferences</ins> > <ins>Settings</ins> and change the following setting as below:

    ```
    "jupyter.runStartupCommands": [
        "%load_ext autoreload", "%autoreload 2"
    ]
    ```

7. In order for Pylance to perform type checking, set the `python.analysis.typeCheckingMode` setting to `basic`;
8. Click on <ins>File</ins> > <ins>Open folder</ins> > `nwcommitaverages`;
9. Click on <ins>View</ins> > <ins>Command Palette</ins> and type:

    ```
    > Dev Container: Reopen in Container
    ```

10. Wait some minutes for the container defined in the <ins>.devcointainer</ins> folder to be built;
11. Done!

## Unit Tests

To run the unit tests in Visual Studio Code (while still connected to the Dev Container):

1. click on the <ins>Testing</ins> icon on the sidebar, right-click on <ins>tests</ins> > <ins>Run Test</ins>;
2. select the Python interpreter inside the Dev Container (if asked);
3. Done! 

To calculate the total unit test coverage in Visual Studio Code (while still connected to the Dev Container):

1. <ins>Terminal</ins> > <ins>New Terminal</ins>;
2. Run the following commands to get the total unit test coverage:

    ```
    cd tests
    coverage run -m unittest nwsharedtests.py
    coverage report --omit=nwsharedtests.py
    ```

3. Run the following commands to get the unit test coverage per class:

    ```
    cd tests
    coverage run -m unittest nwsharedtests.py
    coverage html --omit=nwsharedtests.py && sed -n '/<table class="index" data-sortable>/,/<\/table>/p' htmlcov/class_index.html | pandoc --from html --to plain && sleep 3 && rm -rf htmlcov
    ```

4. Done!

## The makefile

This software package ships with a `makefile` that include all the pre-release verification actions:

1. Launch Visual Studio Code;
2. Click on <ins>File</ins> > <ins>Open folder</ins> > `nwshared`;
3. <ins>Terminal</ins> > <ins>New Terminal</ins>;
4. Run the following commands:

    ```
    cd /workspaces/nwshared/scripts
    make -f makefile <target_name>
    ```
5. Done!

The avalaible target names are:

| Target Name | Description |
|---|---|
| type-verbose | Runs a type verification task and logs everything. |
| coverage-verbose | Runs a unit test coverage calculation task and logs the % per class. |
| tryinstall-verbose | Simulates a "pip install" and logs everything. |
| compile-verbose | Runs "python -m py_compile" command against the module file. |
| unittest-verbose | Runs "python" command against the test files. |
| codemetrics-verbose | Runs a cyclomatic complexity analysis against all the nw*.py files in /src. |
| update-codecoverage | Updates the codecoverage.txt/.svg files according to the total unit test coverage. |
| create-classdiagram | Creates a class diagram in Mermaid format that shows only relationships. |

The expected outcome for `all-concise` is:

```
MODULE_NAME: nwshared
MODULE_VERSION: 1.8.2
COVERAGE_THRESHOLD: 70%
[OK] type-concise: passed!
[OK] changelog-concise: 'CHANGELOG' updated to current version!
[OK] setup-concise: 'setup.py' updated to current version!
[OK] coverage-concise: unit test coverage >= 70%.
[OK] tryinstall-concise: installation process works.
[OK] compile-concise: compiling the library throws no issues.
[OK] unittest-concise: '30' tests found and run.
[OK] codemetrics-concise: the cyclomatic complexity is excellent ('A').
```

Considering the old-fashioned syntax adopted by both `make` and `bash`, here a summary of its less intuitive aspects:

| Aspect | Description |
|---|---|
| `.PHONY` | All the targets that need to be called from another target need to be listed here. |
| `SHELL := /bin/bash` | By default, `make` uses `sh`, which doesn't support some functions such as string comparison. |
| `@` | By default, `make` logs all the commands included in the target. The `@` disables this behaviour. |
| `$$` | Necessary to escape `$`. |
| `$@` | Variable that stores the target name. |
| `if [[ ... ]]` | Double square brackets to enable pattern matching. |

## Known Issues - "Import nwshared could not be resolved Pylance (reportMissingImports)"

If while trying to import `nwshared` in `Visual Studio Code` the following warning appears:

```
Import nwshared could not be resolved Pylance (reportMissingImports)
```

please:

1. in your terminal application of choice, launch the Python interpreter:

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

4. open Visual Studio Code > <ins>File</ins> > <ins>Preferences</ins> > <ins>Settings</ins> and search for <ins>Python › Analysis: Extra Paths</ins>;

5. click on <ins>Add item</ins> and add the path above without the python file name: 

```
C:\Users\Rubèn\src\nwshared\src\
```

6. restart Visual Studio Code;
7. Done!

## Markdown Toolset

Suggested toolset to view and edit this Markdown file:

- [Visual Studio Code](https://code.visualstudio.com/)
- [Markdown Preview Enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced)
- [Markdown PDF](https://marketplace.visualstudio.com/items?itemName=yzane.markdown-pdf)