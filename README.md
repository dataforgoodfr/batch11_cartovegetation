# batch11_cartovegetation
### Requirements

- Docker must be installed
- Until data gathering is implemented, it is necessary to have a data folder containing a geoTIFF file representing a region the size of a town (for test purpose, full automatisation is not yet implemented since it recquires an IGN web service for data import that is scheduled to be launch in beta version mid-july)

### Install

- Clone the current repository :
```shell
git clone https://github.com/dataforgoodfr/batch11_cartovegetation.git
```

- Current branch for data processing is accessed using:
```shell
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


