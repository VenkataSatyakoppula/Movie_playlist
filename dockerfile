# Use the official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

ARG DJANGO_KEY
ARG OMDB_API_KEY
ENV DJANGO_KEY=${DJANGO_KEY}
ENV OMDB_API_KEY=${OMDB_API_KEY}

# Run database migrations and collect static files
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
