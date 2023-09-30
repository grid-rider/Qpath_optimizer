# @author Armin Ulrich 
# @brief Docker implementation for backend deployment. Copies current directory to image and sets up launch procedure. 

# Set base image (host OS)
FROM python:3

# Application listens on port 80
EXPOSE 80

# Set the working directory in the container
WORKDIR /app


COPY . . 
# Copy the dependencies file to the working directory
# COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy the content of the local src directory to the working directory
# COPY application.py .
# COPY graph.py .
# COPY map.py .
# COPY PathFinder.py .
# COPY data/ .

# Specify the command to run on container start
CMD [ "python", "application.py" ]

