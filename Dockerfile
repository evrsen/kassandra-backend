FROM fnndsc/python-poetry

WORKDIR /backend
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

CMD ["poetry", "run", "python", "-m", "backend"]