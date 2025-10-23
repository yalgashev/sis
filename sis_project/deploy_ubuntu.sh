#!/bin/bash

# Ubuntu Server Deployment Script for SIS Django Project
# Run this script as root or with sudo privileges

set -e  # Exit on any error

echo "🚀 Starting SIS Django Project Deployment on Ubuntu Server..."

# Update system packages
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y

# Install required packages
echo "🔧 Installing Docker and dependencies..."
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    software-properties-common \
    ufw \
    fail2ban

# Install Docker
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
fi

# Install Docker Compose (standalone)
if ! command -v docker-compose &> /dev/null; then
    echo "🔨 Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Start and enable Docker
systemctl start docker
systemctl enable docker

# Add current user to docker group (if not root)
if [ "$EUID" -ne 0 ]; then
    usermod -aG docker $USER
    echo "⚠️  Please log out and log back in for Docker group changes to take effect"
fi

# Configure firewall
echo "🔥 Configuring UFW firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8080/tcp  # Alternative HTTP
ufw --force enable

# Configure fail2ban for SSH protection
echo "🛡️  Configuring fail2ban..."
cat > /etc/fail2ban/jail.local << EOF
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
maxretry = 3
bantime = 1h
EOF

systemctl enable fail2ban
systemctl start fail2ban

# Create application directory
APP_DIR="/opt/sis"
echo "📁 Creating application directory: $APP_DIR"
mkdir -p $APP_DIR
cd $APP_DIR

# Create database initialization directory
mkdir -p database_init
mkdir -p logs
mkdir -p nginx/ssl

# Set proper permissions
chown -R www-data:www-data $APP_DIR
chmod -R 755 $APP_DIR

echo "✅ Server setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your SIS project files to: $APP_DIR"
echo "2. Copy your database dump to: $APP_DIR/database_init/"
echo "3. Update environment variables in docker-compose.yml"
echo "4. Generate SSL certificates (optional) in: $APP_DIR/nginx/ssl/"
echo "5. Run: docker-compose up -d"
echo ""
echo "🔗 Access your application at:"
echo "   HTTP: http://your-server-ip:80"
echo "   Alternative: http://your-server-ip:8080"
echo ""
echo "📊 Monitor with:"
echo "   docker-compose logs -f web"
echo "   docker-compose ps"
echo ""
echo "🔒 Security notes:"
echo "   - Change all default passwords in docker-compose.yml"
echo "   - Configure SSL certificates for HTTPS"
echo "   - Update ALLOWED_HOSTS in Django settings"
echo "   - Set a secure SECRET_KEY"