FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the source code
COPY . .

# Expose the port (default for Uvicorn)
EXPOSE 8000

# Start the app
CMD ["uvicorn", "playground:app", "--host", "0.0.0.0", "--port", "8000"]
