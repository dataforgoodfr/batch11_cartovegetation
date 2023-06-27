FROM isciences/exactextract-build-env:latest

LABEL maintainer="dbaston@isciences.com"

COPY . /exactextract

RUN mkdir /cmake-build-release && \
    cd /cmake-build-release && \
    cmake -DCMAKE_BUILD_TYPE=Release /exactextract && \
    make && \
    ./catch_tests && \
    make install && \
    rm -rf /cmake-build-release

RUN apt-get update
RUN apt-get install -y python3 python3-pip

RUN pip3 install -r /exactextract/requirements.txt

WORKDIR /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["python3", "/app/app.py"]