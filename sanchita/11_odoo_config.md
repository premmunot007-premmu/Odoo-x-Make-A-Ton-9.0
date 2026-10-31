# Local Odoo 18 Configuration (odoo.conf)

## Context
A clean configuration file for running Odoo 18 in development mode with performance flags, log levels, and correct custom addons paths.

## Prompt for Antigravity

```markdown
Create `config/odoo.conf` in the project root:

```ini
[options]
; Database credentials
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
db_name = odoo18_brightloop

; Addons paths
addons_path = ../odoo/addons,./custom_addons

; Server settings
http_port = 8069
longpolling_port = 8072
workers = 0

; Development flags
dev_mode = reload,qweb,werkzeug,xml
limit_time_cpu = 600
limit_time_real = 1200
limit_memory_hard = 2684354560
limit_memory_soft = 2147483648

; Admin Master Password (change in production)
admin_passwd = admin_secret_key_2026

; Logging
log_level = info
log_handler = :INFO,odoo.addons.subscription_management:DEBUG
```
```

## Expected Output
- `config/odoo.conf`

## Verification
Launch Odoo using:
```bash
python odoo-bin -c config/odoo.conf
```
