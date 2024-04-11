# Use the official Python image as the base image
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

#Create a Virtual Environment
CMD ["python -m venv venv"]
CMD ["source venv/bin/activate"]

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory into the container
COPY . .

# Expose port 5000 (the default Flask port)
#EXPOSE 5000

# Set the entry point for the container
CMD ["python", "app.py"]

