# Iranminex
## Backend

A Django-based web application built with Django REST Framework (DRF) featuring geospatial capabilities, containerized with Docker.

### Other Docs
The **ProjectDocs** directory contains all other project-related documents.

## 🚀 Features

- **Django REST Framework**: Robust API development
- **PostGIS**: Spatial database functionality with PostgreSQL 16 + PostGIS 3.5
- **Redis**: Caching and session management
- **Docker**: Containerized development and production environments
- **Hybrid Development Setup**: Python runs locally in development, fully containerized in production
- **Nginx**: Production-ready web server with SSL/TLS support
- **Geospatial Processing**: Advanced spatial operations and raster data handling

## 🛠 Tech Stack

- **Backend**: Python, Django, Django REST Framework
- **Database**: PostgreSQL 16 with PostGIS 3.5 extension (postgis/postgis:16-3.5-alpine)
- **Cache**: Redis 8.0.1 (Alpine)
- **Web Server**: Nginx (production only)
- **Containerization**: Docker & Docker Compose
- **Geospatial**: PostGIS for spatial operations, custom raster processing

## 📋 Prerequisites

### Development Environment
- Python 3.8+ (for local Django development)
- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)
- Git
- pip (Python package installer)

### Production Environment
- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)
- Git
- Sudo access (for directory creation and permissions)

## ⚠️ Important Setup Requirements

### Environment Configuration
**CRITICAL**: Before starting any environment, you must configure your environment variables:

```bash
cp .env-example .env
# Edit .env with your actual configuration values
```

**Never skip this step** - the application will not function without proper environment configuration.

### Production Directory Structure
The production environment requires specific host directories with proper permissions:

```bash
# These directories are required for production deployment
/var/iranminex/staticbck/    # Static files (CSS, JS, images)
/var/iranminex/mediabck/     # User-uploaded media files  
/var/iranminex/raster/       # Raster and geospatial processing files
```

## 🚀 Quick Start

### Development Environment

**Architecture**: Django runs locally, supporting services (PostgreSQL, Redis) run in Docker containers.

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd iranminex
   ```

2. **Set up environment variables**
   ```bash
   cp .env-example .env
   # Edit .env with your development configuration
   ```

3. **Start supporting services**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

4. **Set up Python environment**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   cd backend
   python manage.py migrate
   ```

6. **Create a superuser** (optional)
   ```bash
   python manage.py createsuperuser
   ```

7. **Start Django development server**
   ```bash
   python manage.py runserver
   ```

**Development URLs:**
- **Django API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin/
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Production Environment

**Architecture**: All services containerized, Nginx handles external traffic on ports 80/443.

1. **Create required directories and set permissions**
   ```bash
   sudo mkdir -p /var/iranminex/staticbck /var/iranminex/mediabck /var/iranminex/raster
   sudo chown -R 1000:1000 /var/iranminex
   ```

2. **Configure production environment**
   ```bash
   cp .env-example .env
   # Edit .env with production values (DEBUG=False, proper SECRET_KEY, etc.)
   ```

3. **Deploy to production**
   ```bash
   docker compose -f docker-compose.prod.yml up --build
   ```

4. **Run production setup commands**
   ```bash
   # Apply database migrations
   docker compose -f docker-compose.prod.yml exec web python manage.py migrate
   
   # Collect static files
   docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   
   # Create superuser (optional)
   docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

**Production URLs:**
- **Application**: http://your-domain (port 80) or https://your-domain (port 443)
- **Django Admin**: http://your-domain/admin/ or https://your-domain/admin/

## 🐳 Docker Services

### Development Services (`docker-compose.dev.yml`)

**Note**: Django web service runs locally during development.

### Production Services (`docker-compose.prod.yml`)


### Database Configuration

**Note**: The DATABASE utilizes a dedicated, separate server environment and is not deployed within the Docker Compose stack, primarily due to security and business requirements.



### Redis Configuration
```env
REDIS_PORT=6379
REDIS_URL=redis://localhost:6379/0
```

### Django Configuration
```env
# Development
SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Production
SECRET_KEY=your-strong-production-secret-key
DEBUG=0
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## 🗺 Geospatial Features

### PostGIS Capabilities
- **Spatial Data Types**: Point, LineString, Polygon, MultiPolygon
- **Spatial Operations**: Intersection, union, buffer, distance calculations
- **Coordinate Systems**: Support for multiple SRID transformations
- **Spatial Indexing**: Optimized queries with GiST indexes

### Raster Processing
The `/var/iranminex/raster/` directory handles:
- Satellite imagery processing
- Elevation models
- Geospatial raster analysis
- Custom raster operations

## 📚 API Documentation

**Development:**
- **API Root**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **API Schema**: http://localhost:8000/api/schema/
- **Swagger UI**: http://localhost:8000/api/docs/ (if configured)

**Production:**
- **API Root**: https://your-domain/api/
- **Django Admin**: https://your-domain/admin/

## 🛠 Development Workflow

### Environment Comparison

| Feature | Development | Production |
|---------|-------------|------------|
| **Django Runtime** | Local Python | Docker Container |
| **Code Reload** | Automatic | Manual rebuild required |
| **Database** | Docker container | Docker container |
| **Static Files** | Django dev server | Nginx |
| **Media Files** | Local filesystem | Volume mount |
| **SSL/TLS** | None | Nginx with certificates |
| **Ports** | Django (8000) | Nginx (80, 443) |
| **Debugging** | Full access | Container logs |

### Common Development Tasks

#### Local Development Commands
```bash
cd backend

# Django management
python manage.py makemigrations
python manage.py migrate
python manage.py shell
python manage.py test

# Custom commands
python manage.py collectstatic
python manage.py createsuperuser
```

#### Production Commands
```bash
# Django management in container
docker compose -f docker-compose.prod.yml exec web python manage.py makemigrations
docker compose -f docker-compose.prod.yml exec web python manage.py migrate
docker compose -f docker-compose.prod.yml exec web python manage.py shell

# Service management
docker compose -f docker-compose.prod.yml logs web
docker compose -f docker-compose.prod.yml restart web
```

### Database Operations

#### Development



#### Production


## 📦 Enhanced Project Structure


## ⚙️ Service Configuration Details

### PostgreSQL with PostGIS
- **Base Image**: postgis/postgis:16-3.5-alpine
- **Features**: PostGIS 3.5, spatial indexing, health checks
- **Extensions**: postgis, postgis_topology, fuzzystrmatch, postgis_tiger_geocoder
- **Persistence**: Named volume `pgdata`
- **Network**: Custom bridge network `iranminexnet`

### Redis Configuration
- **Image**: redis:8.0.1-alpine
- **Persistence**: AOF (Append Only File) enabled
- **Eviction Policy**: LRU (Least Recently Used)
- **Volume**: Named volume `redis_data`
- **Memory Management**: Optimized for caching and session storage

### Nginx (Production Only)
- **Purpose**: Reverse proxy, static file serving, SSL termination
- **Ports**: 80 (HTTP), 443 (HTTPS)
- **Features**: Gzip compression, security headers, rate limiting
- **Static Files**: Direct serving from volume mounts

## 🔒 Security & Best Practices

### Environment Security
- **Development**: Use local credentials, enable DEBUG mode
- **Production**: Strong passwords, disable DEBUG, use HTTPS
- **Secrets**: Never commit `.env` files, use strong `SECRET_KEY`

### Database Security
- **Connection**: Use connection pooling
- **Backup**: Regular automated backups
- **Access**: Restrict network access to database port

### File System Security
```bash
# Production directory permissions
sudo chown -R 1000:1000 /var/iranminex
sudo chmod -R 755 /var/iranminex
```

### Network Security
- **Development**: Services exposed only to localhost
- **Production**: Only Nginx ports (80, 443) exposed externally
- **Internal Communication**: Services communicate via Docker network


### Development Testing
```bash
cd backend
python manage.py test

# Specific app testing
python manage.py test accounts
python manage.py test contracts
python manage.py test layers

# Coverage report
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Production Testing
```bash
# Health checks
docker compose -f docker-compose.prod.yml exec web python manage.py check --deploy

# Test database connection
docker compose -f docker-compose.prod.yml exec web python manage.py dbshell
```

## 🚀 Deployment Strategies

## 📊 Monitoring & Logging

### Production Backup


## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Set up development environment
4. Make changes and test locally
5. Run tests: `python manage.py test`
6. Commit changes: `git commit -m 'Add amazing feature'`
7. Push to branch: `git push origin feature/amazing-feature`
8. Create Pull Request

### Code Standards
- Follow PEP 8 for Python code
- Use Django best practices
- Add tests for new functionality
- Update documentation for API changes
- Use meaningful commit messages

## 📞 Support & Contact

### Development Team
- **Jazi**: jazi1374@gmail.com
- **AminEbrahimi**: arcobject@gmail.com
- **Sherkat**: https://samanehnegar.com/

### Resources
- **Documentation**: Check `ProjectDocs/` directory
- **Issue Tracking**: Use GitHub issues for bug reports
- **Feature Requests**: Contact development team

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

**Production Checklist:**
- [ ] Environment variables configured in `.env`
- [ ] Production directories created with proper permissions
- [ ] SSL certificates configured (if using HTTPS)
- [ ] Database backups scheduled
- [ ] Monitoring systems in place
- [ ] Security headers configured in Nginx
- [ ] Log rotation configured
- [ ] Firewall rules applied

**Remember**: Always test deployments in a staging environment before production!