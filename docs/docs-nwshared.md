# nwshared
Contact: numbworks@gmail.com

## Revision History

| Date | Author | Description |
|---|---|---|
| 2024-05-19 | numbworks | Created. |
| 2024-08-13 | numbworks | Updated to v1.2.0. |

## Introduction

`nwshared` is a collection of shared components for Python modules.

## Getting Started

To inspect the functionalities of this Python module on Windows and Linux:

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
    - [Remote Development](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)
    - [Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

6. In order for Pylance to perform type checking, click on <ins>File</ins> > <ins>Preferences</ins> > <ins>Settings</ins> and set the `python.analysis.typeCheckingMode` setting to `basic`;
7. Click on <ins>File</ins> > <ins>Open folder</ins> > `nwshared`;
8. Click on <ins>View</ins> > <ins>Command Palette</ins> and type:

    ```
    > Dev Container: Reopen in Container
    ```

9. Wait some minutes for the container defined in the <ins>.devcointainer</ins> folder to be built;
10. Open the Python file (<ins>src/nwshared.py</ins>);
11. Done!

To try out if this Python module installs as a package as expected:

1. Open your terminal application of choice and type the following commands:

    ```
    docker run -it python:3.12.5-bullseye /bin/bash
    pip install -e 'git+https://github.com/numbworks/nwshared.git#egg=nwshared&subdirectory=src'
    pip show nwshared | grep "Version"
    exit
    ```

2. Remove the stopped container using the following commands:

    ```
    docker ps -a
    docker rm {container_id}
    ```

3. Done!


## Unit Tests

To run the unit tests in Visual Studio Code (while still connected to the Dev Container):

1.  click on the <ins>Testing</ins> icon on the sidebar, right-click on <ins>tests</ins> > <ins>Run Test</ins>;
2. select the Python interpreter inside the Dev Container (if asked);
3. Done! 

To calculate the unit test coverage in Visual Studio Code (while still connected to the Dev Container):

1. <ins>Terminal</ins> > <ins>New Terminal</ins>;
2. Run the following commands:

    ```
    cd tests
    coverage run -m unittest nwsharedtests.py
    coverage report
    ```

3. Done!

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