# STEP 1 - Base Image
FROM python:3.12-slim

# STEP 2 - Install uv
RUN pip install --no-cache-dir uv

# STEP 3 - Set the working directory
WORKDIR /app

# STEP 4 - Copy the dependency file 
COPY pyproject.toml uv.lock ./

# STEP 5 - Install dependencies
RUN uv pip install --system --no-deps

# STEP 6 - Copy the application code
COPY . .

# STEP 7 - Expose the port the app runs on
CMD ["python", "-m", "src"]