FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ../ .


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

# # Run db_setup.py when the container launches
# CMD ["alembic", "init", "alembic"]
