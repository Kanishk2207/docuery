# Use the official Python image as a base image
FROM python:3.9-slim

RUN apt-get update && apt-get install libpq-dev build-essential -y
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/app/external/gcp/credentials.json"
# Set environment variables for Google Cloud Storage

# Copy Google Cloud credentials if needed
# (Alternatively, mount the credentials as a volume during deployment)

# Run the FastAPI app with Uvicorn
CMD ["python3", "main.py"]
