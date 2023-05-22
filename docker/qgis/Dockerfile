FROM qgis/qgis:release-3_28

ENV QT_QPA_PLATFORM=offscreen

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3.10", "app.py"]