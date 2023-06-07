FROM ghcr.io/osgeo/gdal:alpine-normal-3.6.3

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update 
RUN apk add build-base python3-dev py3-pip libffi-dev openssl-dev geos-dev proj-dev proj-util py3-scikit-learn

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3.10", "app.py"]