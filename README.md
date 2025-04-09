# Python Backend Starter Project

This is an example starter project for a Python API backend.

## Requirements to run

- python 3.12 #TODO
- docker (latest version) #TODO
- docker-compose (latest version) #TODO

### Run the server locally (for testing)

```shell
python wsgi.py
```

### Unit testing

```shell
python -m pytest tests/unit
```

### Linting

```shell
pip install black
python -m black .
python -m pylint --rcfile=setup.cfg src/*
python -m mypy .

```

## Production deployment

**Run App**

```
./deploy.sh
```

TODO: ADD METRICS ENDPOINT WITH PROMETHEUS