# Docker Deployment Guide

This guide explains how to run the Resume Ranker backend using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Build and run the application**:
   ```bash
   docker-compose up --build
   ```

2. **Run in background**:
   ```bash
   docker-compose up -d --build
   ```

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker directly

1. **Build the image**:
   ```bash
   cd backend
   docker build -t resume-ranker .
   ```

2. **Run the container**:
   ```bash
   docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads resume-ranker
   ```

## Dockerfile Features

The Dockerfile includes:

- **Python 3.10 slim base image** for optimal size
- **System dependencies** (gcc, g++) for compiling Python packages
- **Python requirements** installation from requirements.txt
- **spaCy model download** (en_core_web_sm) during build
- **Non-root user** for security
- **Health check** endpoint monitoring
- **Port 5000** exposure
- **Uploads directory** creation

## Environment Variables

You can customize the application using environment variables:

```bash
# In docker-compose.yml or docker run command
environment:
  - FLASK_ENV=production
  - SECRET_KEY=your-secret-key-here
  - DATABASE_URL=sqlite:///resume_ranker.db
```

## Volume Mounts

The application uses volume mounts for:

- **Uploads**: `./backend/uploads:/app/uploads` - Persistent file storage
- **Database**: `./backend/resume_ranker.db:/app/resume_ranker.db` - Persistent data

## Health Check

The container includes a health check that:

- Checks the `/health` endpoint every 30 seconds
- Times out after 10 seconds
- Retries 3 times before marking as unhealthy
- Waits 40 seconds before starting checks

## Building for Production

1. **Update the Dockerfile** for production settings:
   ```dockerfile
   ENV FLASK_ENV=production
   ENV SECRET_KEY=your-production-secret-key
   ```

2. **Build with production tag**:
   ```bash
   docker build -t resume-ranker:latest .
   ```

3. **Run with production settings**:
   ```bash
   docker run -d \
     -p 5000:5000 \
     -e FLASK_ENV=production \
     -e SECRET_KEY=your-production-secret \
     -v $(pwd)/uploads:/app/uploads \
     --name resume-ranker \
     resume-ranker:latest
   ```

## Troubleshooting

### Container won't start
- Check if port 5000 is already in use
- Verify the Dockerfile syntax
- Check container logs: `docker logs <container-name>`

### spaCy model issues
- The model is downloaded during build time
- If download fails, rebuild the image
- Check internet connectivity during build

### Permission issues
- The container runs as a non-root user
- Ensure volume mounts have correct permissions
- Check file ownership in the uploads directory

### Database issues
- The SQLite database is created automatically
- Ensure the database volume mount is writable
- Check database file permissions

## Development

For development with hot reloading:

```bash
# Mount source code as volume
docker run -p 5000:5000 \
  -v $(pwd):/app \
  -e FLASK_ENV=development \
  resume-ranker
```

## Monitoring

Check container status:
```bash
docker ps
docker logs resume-ranker
docker stats resume-ranker
```

## Security Notes

- The container runs as a non-root user
- Only port 5000 is exposed
- Uploads are stored in a separate volume
- Database is persistent and secure
- Health checks monitor application status

## Performance

- Uses Python 3.10 slim image for smaller size
- Dependencies are cached in separate layers
- spaCy model is downloaded during build
- Non-root user reduces security surface
