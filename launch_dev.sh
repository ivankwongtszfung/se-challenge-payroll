#!/bin/bash

mkdir -p db

tests() {
  export SQLALCHEMY_DATABASE_URL=sqlite:///
  pytest -vv
}

web_dev() {
  export SQLALCHEMY_DATABASE_URL=sqlite:///./db/sql.db
  alembic upgrade head
  uvicorn app.main:app --reload --reload-dir app
}



case $1 in

  tests)
    tests
    ;;
  web_dev)
    web_dev
    ;;
  *)
    echo """###############################
    we dont support $1
    run test with      tests
    run project with    web_dev
    """
    ;;
esac
