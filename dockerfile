# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install dependencies from setup.py
RUN pip install .

# Define the command to run your script (the entry point created in setup.py)
ENTRYPOINT ["my-air-monitor"]
