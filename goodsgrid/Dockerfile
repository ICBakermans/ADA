# Using python 3.8.3 slim image as the base image
FROM python:3.8.3-slim
# Defining working directory and copy the requirements file. We will run the commands inside this new directory
WORKDIR /usr/src/myapp
# Copy requirements_pod.txt  to the working directory
COPY requirements_pod.txt .
# Install required python packages
RUN pip install --no-cache-dir -r requirements_pod.txt
# Copy all files in training-db local host directory to /usr/src/myapp in Docker container
COPY . .
# Expose the port that our app runs in
EXPOSE 5000
# Enviroment Variables
ENV DB_URL  sqlite:///goodsgrid.db
# Run our App
CMD ["python3","app.py"]