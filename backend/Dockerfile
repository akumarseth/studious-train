# Use the official Python image from the Docker Hub
FROM python:3.12

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create virtual environments
RUN poetry config virtualenvs.create false

# Set the working directory in the container
WORKDIR /app/src

# Copy the Poetry configuration files
COPY ./pyproject.toml ./poetry.lock /app/src/

# Install the main dependencies using Poetry
RUN poetry install --only main

# Copy the rest of the application code
COPY . /app/src/

# Download and install the spaCy model
# RUN python -m spacy download en_core_web_sm

# RUN Ollama serve
# Expose the port the app runs on
EXPOSE 8000

# Create a non-root user and change ownership of the application directory
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

# Switch to the non-root user
USER appuser

# Specify the command to run the application
CMD ["/usr/local/bin/python", "-m", "src"]
