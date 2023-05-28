
# batch11_cartovegetation
### Requirements

- Docker and Docker compose must be installed [Docker (Docker compose included)](https://www.docker.com/products/docker-desktop/)
- Until data gathering is implemented, it is required to have a data folder in your system containing the unzipped data from IGN BD ORTHO IRC of the 'departement' that contain the processed city. *For test purpose, full automatisation is not yet implemented since it recquires an IGN web service for data import that is scheduled to be launch in beta version mid-july*

### Install

- Clone the current repository :
```shell
git clone https://github.com/dataforgoodfr/batch11_cartovegetation.git
```

- Current branch for data processing is accessed using:
```shell
git fetch --all
git switch project-init
```

- Rename the file `.env.sample` to `.env` and update its variables using your configuration.

- `.otb.env` contains variables that can also be tweaked.

### Build Images
```shell
docker compose build
```

### Run

To start all services and run the whole processing chain:
```shell
docker compose --env-file .env up
```

To stops containers and removes them:
```shell
docker compose down
```

To run specific service defined in *docker-compose.yaml*:
```shell
docker compose run --rm --env .env <service_name>
```

### Glossary

| id | Definition |
|--|--|
| ext | Extraction of area |
| seg | Segmentation |
| hte | Haralick texture extraction |
| bnd | Reordering band |
| rdi | Radiometric indices |
| zst | Zonal Statistics |