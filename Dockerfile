# ---- Base Node ----
FROM python:3.11 AS base
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

# Copy wait-for-it
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# ---- Copy Files/Build ----
FROM base AS build
WORKDIR /src
COPY . /src/

# ---- Release ----
FROM base AS release
# Copy built python / node src files from builder stage
COPY --from=build /src/ /src/
