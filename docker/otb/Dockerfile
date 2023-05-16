FROM orfeotoolbox/otb:8.1.1

# install pip
RUN apt update
RUN apt install -y python3-pip

# Install pip requirements
COPY requirements.txt .
RUN python3.8 -m pip install -r requirements.txt

WORKDIR /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3.8", "app.py"]