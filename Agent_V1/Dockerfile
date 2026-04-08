# Use a slim version of Python for a smaller image size
FROM python:3.11-slim

# Prevent Python from writing .pyc files and ensure logs are flush immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies if needed (e.g., for certain python libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Streamlit's default port is 8501
EXPOSE 8501

# Command to run the application
# Inside Agent_V1/Dockerfile
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0