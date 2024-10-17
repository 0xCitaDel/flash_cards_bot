FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false 

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

# COPY . /app

CMD ["watchmedo", "auto-restart", "--recursive", "poetry", "run", "python3", "src/main.py"]
# CMD ["poetry", "run", "python3", "src/main.py"]
