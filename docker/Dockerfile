# Base image for Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the Flask app's port (used for the dashboard)
EXPOSE 5000

# Default command to run the main pipeline
CMD ["python", "main.py"]
