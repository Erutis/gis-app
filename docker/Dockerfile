FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ../app .


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run db_setup.py when the container launches
CMD ["python", "db_setup.py"]
