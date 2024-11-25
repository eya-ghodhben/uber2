# Use an official Python runtime as a base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the dependencies
RUN pip install -r requirements.txt

# Set the environment variable for MongoDB URI
ENV MONGO_URI="mongodb://mongo:27017/driverdb"

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

