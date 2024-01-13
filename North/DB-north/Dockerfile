
FROM postgres:latest

# Set environment variables
ENV POSTGRES_DB=north-back
ENV POSTGRES_USER=north-back
ENV POSTGRES_PASSWORD=123

# PostgreSQL listens on port 5002
ENV PGPORT=5012

# Copy the initialization script to the docker entrypoint directory
COPY ./init.sql /docker-entrypoint-initdb.d/

# Expose the PostgreSQL port
EXPOSE 5012

# Set the default command to run when starting the container
CMD ["postgres"]