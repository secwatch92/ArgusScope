# --- Stage 1: Select the Base Image ---
# We use an official and slim Python image as the base.
FROM python:3.12-slim

# --- Stage 2: Environment Settings ---
# These environment variables help improve Python's performance in a Docker environment.
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from creating .pyc files
ENV PYTHONUNBUFFERED 1         # Sends logs directly to the Docker console, preventing buffering

# --- Stage 3: Install Dependencies ---
# Set the working directory inside the container.
WORKDIR /app

# First, copy only the requirements file.
# This makes optimal use of Docker's layer caching feature.
# If this file doesn't change, Docker won't re-run this step in subsequent builds, which speeds up the process.
COPY requirements.txt .

# Upgrade pip and then install the required libraries.
# --no-cache-dir reduces the image size.
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# --- Stage 4: Copy the Project Source Code ---
# Now that the dependencies are installed, copy all the project source code into the container.
# This code will be overlaid by the volume mount in development mode.
COPY . .

# --- Stage 5: Define Port and Execution Command ---
# Inform Docker which port our application will run on.
EXPOSE 8000

# The default command that runs when the container starts.
# This command starts the Uvicorn web server to run your API (built with FastAPI).
# It assumes that your main API file is located at argus_scope/api/server.py and the main variable is named 'app'.
# The --reload flag enables hot-reloading for development.
CMD ["uvicorn", "argus_scope.api.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]