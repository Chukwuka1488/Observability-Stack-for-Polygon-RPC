# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV FLASK_APP=src.app

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "src.app:app"]