# Use the official Python image as a base
FROM python:3.10.0-slim as base

# Set environment variables to prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Create a non-root user for running the application
ARG USER_ID=10001
RUN useradd --no-create-home --shell /sbin/nologin --uid ${USER_ID} appuser

# Change ownership of the working directory to the non-root user
RUN chown appuser:appuser /app

# Install dependencies using a cache mount for pip cache and a bind mount for requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

# Switch to the non-root user
USER appuser

# Copy the application source code into the container
COPY . .

# Expose the port the application will run on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "app.py"]