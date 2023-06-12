FROM python:3.11-slim-buster as base

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/share/pypoetry/venv/bin/"

WORKDIR /web_app/
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-root --no-interaction --without dev

FROM base as prod
# In production we copy the todo_app to the container. In dev we worked in the mapped version from the host to see changes.
COPY todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "gunicorn", "--chdir=/web_app/todo_app", "app:create_app()", "--bind", "0.0.0.0"]

FROM base as dev 
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]

FROM base as test
COPY .env.test .
COPY todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "pytest"]
# CMD [ "bash" ]