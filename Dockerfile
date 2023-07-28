# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/

# Set work directory
WORKDIR /src

# Install dependencies
RUN pip install --upgrade --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --clear

# Copy project
COPY . /src/
