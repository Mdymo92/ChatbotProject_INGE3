# Use the official Python image as the base image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./chatbot /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Open future port that will be used
EXPOSE 5005

# Launch the payload
CMD ["rasa", "run","-m","models","--enable-api","--cors","\"*\"","--debug"]
