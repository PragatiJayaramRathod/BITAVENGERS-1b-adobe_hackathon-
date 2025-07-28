# Use a lightweight Python base image for AMD64
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the processing script
COPY process_pdfs_round1b.py .

# Command to run the script
CMD ["python", "process_pdfs_round1b.py"]
