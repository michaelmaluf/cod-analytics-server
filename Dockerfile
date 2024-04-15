# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Define environment variable
ENV FLASK_APP=app:create_app()

# Run gunicorn and bind it to 0.0.0.0:5001 with 2 worker processes
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:5001", "--workers", "2"]