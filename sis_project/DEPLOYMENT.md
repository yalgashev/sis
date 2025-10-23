# SIS Django Project - Ubuntu Server Deployment

This guide will help you deploy the SIS (Student Information System) Django project on Ubuntu Server using Docker containers.

## 📋 Prerequisites

- Ubuntu Server 20.04 LTS or newer
- Root or sudo access
- Internet connection
- At least 2GB RAM and 10GB disk space

## 🚀 Quick Deployment

### 1. Run the Automated Setup Script

```bash
# Download and run the setup script
sudo bash deploy_ubuntu.sh
```

This script will:
- Install Docker and Docker Compose
- Configure firewall (UFW)
- Set up fail2ban for SSH protection
- Create application directories
- Configure security settings

### 2. Upload Project Files

Copy all project files to `/opt/sis/`:

```bash
# Create the directory structure
sudo mkdir -p /opt/sis
cd /opt/sis

# Copy your project files here
# You can use scp, rsync, or git clone
```

### 3. Prepare Database (if you have existing data)

If you have an existing database, export it and place the SQL dump in the initialization directory:

```bash
# Place your database dump here
sudo cp your_database_dump.sql /opt/sis/database_init/01-init.sql
```

### 4. Configure Environment Variables

Edit the `docker-compose.yml` file and update these critical settings:

```yaml
environment:
  - DEBUG=0  # Always 0 for production
  - ALLOWED_HOSTS=your-domain.com,your-server-ip  # Your actual domain/IP
  - SECRET_KEY=your-very-secure-secret-key-here    # Generate a new one
```

### 5. Deploy the Application

```bash
cd /opt/sis
sudo docker-compose up -d
```

### 6. Verify Deployment

```bash
# Check if all services are running
sudo docker-compose ps

# Check logs
sudo docker-compose logs -f web

# Test the application
curl http://localhost
```

## 🌐 Access Your Application

- **Main Application**: `http://your-server-ip`
- **Alternative Port**: `http://your-server-ip:8080`
- **Admin Panel**: `http://your-server-ip/admin/`

## 🔒 Security Configuration

### SSL/HTTPS Setup (Recommended)

1. Obtain SSL certificates (Let's Encrypt recommended):
```bash
sudo apt install certbot
sudo certbot certonly --standalone -d your-domain.com
```

2. Copy certificates to nginx directory:
```bash
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem /opt/sis/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem /opt/sis/nginx/ssl/key.pem
```

3. Uncomment HTTPS server block in `nginx/nginx.conf`

4. Restart services:
```bash
sudo docker-compose restart nginx
```

### Change Default Passwords

**Important**: Update these passwords in `docker-compose.yml`:

```yaml
# PostgreSQL password
POSTGRES_PASSWORD: sis_secure_password_2024

# Redis password
command: redis-server --appendonly yes --requirepass redis_password_2024

# Django secret key
SECRET_KEY: your-very-secure-secret-key-here
```

## 📊 Monitoring and Maintenance

### View Logs
```bash
# All services
sudo docker-compose logs -f

# Specific service
sudo docker-compose logs -f web
sudo docker-compose logs -f db
```

### Backup Database
```bash
# Create backup
sudo docker-compose exec db pg_dump -U postgres -d sis > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Update Application
```bash
cd /opt/sis
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
```

### Restart Services
```bash
# Restart all services
sudo docker-compose restart

# Restart specific service
sudo docker-compose restart web
```

## 🛠 Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
sudo netstat -tulpn | grep :80
sudo systemctl stop apache2  # If Apache is running
sudo systemctl disable apache2
```

2. **Permission errors**:
```bash
sudo chown -R www-data:www-data /opt/sis
sudo chmod -R 755 /opt/sis
```

3. **Database connection errors**:
```bash
sudo docker-compose logs db
sudo docker-compose exec db psql -U postgres -d sis -c "SELECT 1;"
```

4. **Static files not loading**:
```bash
sudo docker-compose exec web python manage.py collectstatic --noinput
sudo docker-compose restart nginx
```

## 🔧 Configuration Files

- `docker-compose.yml`: Main orchestration file
- `Dockerfile`: Django application container
- `nginx/nginx.conf`: Web server configuration
- `requirements.txt`: Python dependencies
- `.dockerignore`: Docker build exclusions

## 📈 Performance Optimization

### For Production Use:

1. **Increase worker processes** in Dockerfile:
```dockerfile
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "sis_project.wsgi:application"]
```

2. **Enable Redis caching** in Django settings:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
```

3. **Configure database pooling** and **connection limits**

## 📞 Support

For issues with the SIS application:
1. Check the logs: `sudo docker-compose logs -f web`
2. Verify database connectivity: `sudo docker-compose exec db psql -U postgres -d sis`
3. Ensure all services are healthy: `sudo docker-compose ps`

## 🔄 Backup Strategy

Implement regular backups:
```bash
#!/bin/bash
# Add to crontab: 0 2 * * * /opt/sis/backup.sh

BACKUP_DIR="/opt/sis/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
docker-compose exec -T db pg_dump -U postgres -d sis > "$BACKUP_DIR/sis_db_$DATE.sql"

# Backup media files
tar -czf "$BACKUP_DIR/sis_media_$DATE.tar.gz" -C /opt/sis media/

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

---

**🎉 Your SIS Django application is now deployed and ready for production use!**