# Product Catalog – Development Setup

This project is a simple CRUD application with sales tracking:

- **Frontend**: Vue 3 + Vite + TailwindCSS  
- **Backend**: FastAPI  
- **Database**: PostgreSQL

---

## Requirements

- Docker & Docker Compose  
- Python 3.11+ (for the backend)  
- Node.js 18+ (for the frontend)  
- GNU Make

```bash
# For Debian-based distributions:

sudo apt update && sudo apt install -y \
    make \
    python3 \
    python3-pip \
    python3-venv \
    nodejs \
    npm

# Install docker engine: https://docs.docker.com/engine/install/ 

```

---

## Local Development (with Make)

Use the provided `Makefile` to streamline development tasks.

### 1. Start the database

```bash
make db
```

Starts the PostgreSQL database using Docker.  
Connection details:

- **Host**: `localhost`
- **Port**: `5432`
- **User**: `admin`
- **Password**: `admin`
- **Database**: `catalog`

---

### 2. Install dependencies

```bash
make install
```

This will:
- Set up a virtual environment and install backend dependencies.
- Install frontend packages with npm.

---

### 3. Run backend and frontend

Open two terminals:

**Terminal 1 – Backend**

```bash
make backend
```

Backend will run at [http://localhost:8000](http://localhost:8000)

**Terminal 2 – Frontend**

```bash
make frontend
```

Frontend will run at [http://localhost:5173](http://localhost:5173)

---

## Quick Test

1. Add products through the form.  
2. Sell units using the "Sell 1" button.  
3. Delete products using the "Delete" button.

---

## Stop or clean up

Stop the PostgreSQL container:

```bash
make stop
```

Stop and remove everything:

```bash
make clean
```

---

## Project Structure

```
.
├── backend/        # FastAPI app
├── frontend/       # Vue 3 + Tailwind
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## Notes

- Backend DB connection URL:
  ```
  postgresql://admin:admin@localhost:5432/catalog
  ```

- The frontend proxies `/api` to the backend (`localhost:8000`), configured in `vite.config.js`.