# Production Deployment, Nginx & Backup Strategy

## Context
Production deployment manual in `docs/DEPLOYMENT.md` covering VPS setup, Ubuntu 24.04 LTS, Nginx SSL reverse proxy, and automated PostgreSQL backups.

## Prompt for Antigravity

```markdown
Create `docs/DEPLOYMENT.md`:

```markdown
# 🚀 Production Deployment Guide

## 1. System Requirements
- OS: Ubuntu 22.04 / 24.04 LTS
- CPU: 2+ vCPUs
- RAM: 4GB+ (8GB recommended for production)
- Storage: 40GB SSD
- PostgreSQL 16
- Python 3.10+

## 2. Server Provisioning
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-dev libxml2-dev libxslt1-dev zlib1g-dev \
    libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev \
    libmysqlclient-dev libjpeg-dev libpq-dev libjpeg8-dev liblcms2-dev \
    libblas-dev libatlas-base-dev git postgresql postgresql-contrib nginx
```

## 3. Database Configuration
```bash
sudo -u postgres createuser -d -R -S odoo
sudo -u postgres psql -c "ALTER USER odoo WITH PASSWORD 'strong_production_db_password';"
```

## 4. Install & Launch Module
```bash
# Clone repository
git clone https://github.com/your-org/brightloop-subscription.git /opt/odoo/custom_addons

# Update Odoo instance
/opt/odoo/odoo-bin -c /etc/odoo/odoo.conf -i subscription_management --stop-after-init
```

## 5. Nginx Reverse Proxy with Let's Encrypt SSL
```nginx
upstream odoo {
    server 127.0.0.1:8069;
}
upstream odoochat {
    server 127.0.0.1:8072;
}

server {
    listen 80;
    server_name subscription.brightloop.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name subscription.brightloop.com;

    ssl_certificate /etc/letsencrypt/live/subscription.brightloop.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/subscription.brightloop.com/privkey.pem;

    client_max_body_size 100M;

    location / {
        proxy_pass http://odoo;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
    }

    location /websocket {
        proxy_pass http://odoochat;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## 6. Daily Automated PostgreSQL Backup Cron
```bash
# /etc/cron.daily/odoo_backup.sh
#!/bin/bash
BACKUP_DIR="/var/backups/odoo"
DATE=$(date +\%Y\%m\%d_\%H\%M\%S)
mkdir -p $BACKUP_DIR
pg_dump -U odoo -F c -b -v -f "$BACKUP_DIR/brightloop_$DATE.dump" odoo18_brightloop
find $BACKUP_DIR -type f -mtime +14 -name "*.dump" -delete
```
```
```

## Expected Output
- `docs/DEPLOYMENT.md`
