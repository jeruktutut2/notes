# MYSQL

## library
    pyenv versions
    pyenv local 3.9.18
    python --version
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install aiomysql
    deactivate

## unit test
    python -m unittest tests/unit_tests/test_mysql_service.py