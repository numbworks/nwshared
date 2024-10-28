FROM python:3.12.5-bookworm

RUN pip install numpy==2.1.2
RUN pip install pyarrow==17.0.0
RUN pip install pandas==2.2.3
RUN pip install requests==2.32.3
RUN pip install matplotlib==3.9.2
RUN pip install coverage==7.6.4
RUN pip install parameterized==0.9.0
RUN pip install jinja2==3.1.4
RUN pip install 'git+https://github.com/numbworks/nwpackageversions.git@v1.2.0#egg=nwpackageversions&subdirectory=src'

RUN wget https://github.com/jgm/pandoc/releases/download/3.4/pandoc-3.4-1-amd64.deb \
    && dpkg -i pandoc-3.4-1-amd64.deb \
    && rm -f pandoc-3.4-1-amd64.deb