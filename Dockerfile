# 1. Use a lightweight Python base image
FROM python:3.9-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install system dependencies (FIX FOR YOUR ERROR)
# libgomp1 is required for LightGBM/XGBoost
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the app
COPY . .

# 7. Expose the port
EXPOSE 8000

# 8. Run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]