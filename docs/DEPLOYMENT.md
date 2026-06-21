# CyberShield Deployment Guide

## AWS EC2 Deployment

### Step 1: Set Up EC2 Instance

```bash
# Launch Ubuntu 22.04 LTS instance
# Choose t2.medium or t3.medium (minimum)
# Configure security group:
#   - Allow HTTP (80)
#   - Allow HTTPS (443)
#   - Allow SSH (22)
```

### Step 2: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y

# Install MySQL
sudo apt install mysql-server -y

# Install Nginx
sudo apt install nginx -y

# Install Gunicorn
pip3 install gunicorn
```

### Step 3: Set Up Python Environment

```bash
cd /var/www
git clone <your-repository> CyberShield
cd CyberShield

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure MySQL

```bash
# Import database schema
mysql -u root -p < database/cybershield.sql

# Create database user
mysql -u root -p
```

```sql
CREATE USER 'cybershield_user'@'localhost' IDENTIFIED BY 'CyberShield2024!Secure';
GRANT ALL PRIVILEGES ON cybershield.* TO 'cybershield_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 5: Configure Gunicorn

Create `/etc/systemd/system/cybershield.service`:

```ini
[Unit]
Description=CyberShield Web Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/CyberShield
Environment="PATH=/var/www/CyberShield/venv/bin"
ExecStart=/var/www/CyberShield/venv/bin/gunicorn \
    --access-logfile /var/log/cybershield/access.log \
    --error-logfile /var/log/cybershield/error.log \
    --bind 127.0.0.1:5000 \
    --workers 4 \
    app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable cybershield
sudo systemctl start cybershield
```

### Step 6: Configure Nginx

Create `/etc/nginx/sites-available/cybershield`:

```nginx
upstream cybershield_server {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://cybershield_server;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/CyberShield/static;
        expires 30d;
    }

    location /certificates {
        alias /var/www/CyberShield/certificates;
        expires 30d;
    }

    location /reports {
        alias /var/www/CyberShield/reports;
        expires 30d;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/cybershield /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Configure SSL (HTTPS)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

---

## Production Checklist

- ✅ Enable HTTPS
- ✅ Set up database backups
- ✅ Configure monitoring (e.g., CloudWatch)
- ✅ Set up log rotation
- ✅ Configure CSRF for production
- ✅ Use environment variables for secrets
- ✅ Set up rate limiting
- ✅ Enable security headers

---

## Monitoring

```bash
# Check application status
sudo systemctl status cybershield

# View logs
sudo tail -f /var/log/cybershield/access.log
sudo tail -f /var/log/cybershield/error.log

# Check Nginx
sudo systemctl status nginx
```

---

For support: support@cybershield.platform