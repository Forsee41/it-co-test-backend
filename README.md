# Backend

## Run locally

1. Make venv `python -m venv env`
1. Activate venv `source env/bin/activate`
1. Update pip `pip install --upgrade pip`
1. Install dependencies `pip install -r requirements.txt`
1. For dev, install dev dependencies `pip install -r requirements-dev.txt`
1. Set required environment variables. You can use `.env` file. List of required env vars is in `.env-example`
1. Run db containers `make up`
1. Run db migrations `alembic upgrade head`
1. Run app `python run.py`

## Run docker container

When building docker images on Windows, you need to change line ending format of `run.sh` to unix-compatible LF. No such problems on Linux.

1. Build image `docker build -t it-co-backend .`
1. Run image via docker cli `docker run -p 8000:8000 --env-file .env it-co-backend`. This assumes you have `.env` file with env vars.

## Run from docker-compose

1. Run `docker-compose -f docker-compose.yml up -d`

## Development

1. Run everything from 'Run locally' to set up your env and databases.
1. Set up pre-commit hooks `pre-commit install`
1. Check `Makefile` for a list of common scripts.
1. `make test` to run tests
1. `make prepare` fully run/updte dbs
1. `make psql` to connect to db via psql
1. `make check` to run lint checks and typechecks
