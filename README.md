# Product Catalog – AI-Powered Chat Integration

This project is a fullstack product catalog with CRUD operations, sales tracking, and a built-in AI assistant powered by RAG (Retrieval-Augmented Generation) to answer product-related queries.

- **Frontend**: Vue 3 + Vite + TailwindCSS  
- **Backend**: FastAPI + OpenAI API  
- **Database**: PostgreSQL  
- **AI**: Retrieval-Augmented Generation (RAG) using OpenAI and SQL-based product queries

---

## Requirements

- Docker & Docker Compose  
- Python 3.11+ (for the backend)  
- Node.js 18+ (for the frontend)  
- GNU Make
- OpenAI API Key

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

Create a `.env` file inside the `backend/` folder with the following content:

```env
# backend/.env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=catalog
DB_USER=admin
DB_PASSWORD=admin

OPENAI_API_KEY=sk-...
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

1. Add products using the form  
2. Use the chat (💬 button) to ask questions about the catalog  
3. Try:
   - “¿Hay productos frágiles?”
   - “¿Cuántos libros tenemos?”
   - “Muéstrame productos que cuesten menos de 20 €”

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
- Chat is powered by OpenAI GPT-4o via API (you need your key)