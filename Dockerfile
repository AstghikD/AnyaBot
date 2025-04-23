# Use a lightweight official Python base image
FROM python:3.10.13-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all your bot code
COPY . .

# Command to run your bot
CMD ["python", "bot.py"]
