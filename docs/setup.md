# Setup

This project requires you to build a container, you can use the technology of your choice `docker` or `podman` the image is tested using both technologies.

!!! example "Why Python?" 

    The language of choice for the technical challenge was `python` specially because of my familiarity with the language. However I explore the use of `typescript` when beggining the technical challenge, but due to time constraints, I decided to implement the rest of the project in a language that didn't require compilation.

Building a container is out of the scope of this technical challenge, and one of the assumptions is that your computer, has any of the technologies mentioned 
before, `docker` or `buildah` to accomplish the preparation task.

## Cloning Repo

First step is to download the code from the repository

``` sh
git clone https://github.com/canimus/pvhtc

# move to directory
cd pvhtc
```

## Build Container
The only requirement for the build is to execute the following command
```sh
# Building the PVH technical challenge image
docker build --rm . -t pvhtcpy
```

!!! abstract "Container Details" 

    At this point, you can continue reading the details about the container image, or you can just jump to the execution of the test suite, in the next section.
    [Run](/run)


## Container File

The different sections of the container file are explained below:

### Base Image
``` Dockerfile hl_lines="2 3"
# python 3.8 installed
FROM python:3.8
```

For a production environment an `alpine` image is recommended as it will consume less space.
Also because it could be deployed faster.
In the case of the technical challenge, speed and operational readiness were not the considerations for the completion, and therefore I chose for an image that could get the job done quick, and without the need of additional setup from the operative system level.

### OCR Libs

For reading characters from images, I used the tesseract library. With its binging to python in the library `pytesseract`

``` Dockerfile
# Installing OS Libraries
RUN apt-get install -yqq unzip zstd tesseract-ocr libtesseract-dev
```

### Chrome Browser
As per the specification the only web browser under the scope is Chrome, hereby we setup the repositories to download the software binaries.
``` Dockerfile hl_lines="11"
# Google Repos
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Chrome
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Latest Versions
RUN apt-get -y update

# Browser Install
RUN apt-get install -y google-chrome-stable
```

### Chrome Driver

In order to enable the webdriver integration with the web browser, it is required to install the web driver libraries. Incorporated in the settings below.

``` Dockerfile hl_lines="5"
# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99
```

### Python Libs
The execution requires `selenium` as the main library to conduct the automation routines and additional libraries for the additional features covered by this automated test script.

``` Dockerfile
WORKDIR /usr/src
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
```

!!! example "requirements.txt" 

    ``` python
    selenium==3.141.0
    pytesseract==0.3.6
    Pillow==8.0.1
    numpy==1.19.4
    Faker==4.14.2
    fake-useragent==0.1.11
    pychalk==2.0.1
    mkdocs-material==6.1.5
    behave==1.2.6
    ```

### Runtime

The container uses a volume at the root of the file system, to pass scripts to be executed inside of the container in the path `/scripts`.
It is expected that when running the container a volume from the external host system, is mapped to this volume for execution.
The expected default script for running the suite is `main.py`.

``` Dockerfile hl_lines="4"
# Location of Automated Test Scripts
VOLUME /scripts

CMD ["python", "/scripts/main.py"]
```

Now we are ready to run the container and with it, the automated test script that covers the technical challenge.
Please go ahead to the __Run__ section by navigating in the footer of this page...