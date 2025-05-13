# Product Catalog App

This project includes a simple product catalog with sales tracking, built with:

- **Frontend**: Vue 3 + TailwindCSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL

## Prerequisites

- Docker & Docker Compose

## Launching the Project

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. Start all services:
   ```bash
   docker-compose up --build
   ```

3. Open the frontend in your browser:
   ```
   http://localhost:5173
   ```

## Development Notes

- The backend uses PostgreSQL as its database.
- The frontend communicates with the backend via REST API internally through the Docker network.
- Product data is stored in the database, and sales are tracked by creating separate sale entries.

## Database Connection Details

- **Host**: `db`
- **Port**: `5432`
- **Database**: `catalog`
- **User**: `admin`
- **Password**: `admin`

---

ℹ️ You can stop the project with:
```bash
docker-compose down
```
