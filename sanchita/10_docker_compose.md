# Docker Compose Setup for Odoo 18 & PostgreSQL 16

## Context
Provide an instant one-command containerized development and demo environment with Odoo 18, PostgreSQL 16, persistent volumes, and live addon mounting.

## Prompt for Antigravity

```markdown
In the root of the project, create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    image: odoo:18.0
    container_name: brightloop_odoo18
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8069:8069"
      - "8072:8072"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - odoo-web-data:/var/lib/odoo
      - ./config:/etc/odoo
      - ./custom_addons:/mnt/extra-addons
    command: --dev=all -d brightloop_db -i subscription_management
    restart: unless-stopped

  db:
    image: postgres:16
    container_name: brightloop_postgres16
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
      - PGDATA=/var/lib/postgresql/data/pgdata
    volumes:
      - odoo-db-data:/var/lib/postgresql/data/pgdata
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U odoo"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  odoo-web-data:
  odoo-db-data:
```

Also create a simple `Makefile` with commands:
- `make up` (`docker compose up -d`)
- `make down` (`docker compose down`)
- `make logs` (`docker compose logs -f web`)
- `make restart` (`docker compose restart web`)
```

## Expected Output
- `docker-compose.yml`
- `Makefile`

## Verification
Run `docker compose up -d` (if Docker installed) and check `localhost:8069`.
