# CyberShield Installation Guide

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- Node.js 16+ (optional, for development)
- pip (Python package manager)

## Step 1: Install Python Dependencies

```bash
cd CyberShield
pip install -r requirements.txt
```

## Step 2: Set Up MySQL Database

```bash
# Start MySQL service
sudo systemctl start mysql

# Create database and import schema
mysql -u root -p < database/cybershield.sql
```

## Step 3: Configure Environment Variables

Create a `.env` file:

```bash
MYSQL_USER=cybershield_user
MYSQL_PASSWORD=CyberShield2024!Secure
MYSQL_HOST=localhost
MYSQL_DATABASE=cybershield
SECRET_KEY=Your-Secret-Key-Here
```

## Step 4: Run the Application

```bash
# Development mode
python app.py

# Production mode (using Gunicorn)
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

## Step 5: Access the Application

Open your browser and navigate to:


## Default Accounts

- **Admin**: username: `admin`, password: `admin123`
- **Student**: Create a new account via registration

---

## Troubleshooting

### Database Connection Error
```bash
# Check MySQL is running
sudo systemctl status mysql

# Verify database exists
mysql -u root -p -e "SHOW DATABASES;"
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

For more information, see [DEPLOYMENT.md](DEPLOYMENT.md)


