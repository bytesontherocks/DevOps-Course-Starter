FROM python:latest

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="${PATH}:/root/.local/share/pypoetry/venv/bin/"

COPY todo_app /todo_app
COPY pyproject.toml /pyproject.toml

RUN poetry install --no-root --no-interaction

ENTRYPOINT ["poetry", "run", "gunicorn", "todo_app.app:create_app()", "--bind", "0.0.0.0"]
#ENTRYPOINT ["bash"]