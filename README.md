# bookings

Centralizirana multi-tenant SaaS platforma za hrvatska mala i srednja poduzeća.

## Moduli

- **Webshop** — katalog proizvoda, narudžbe, CorvusPay plaćanje, Fina eRačun fiskalizacija
- **Booking** — kalendar dostupnosti, rezervacije, depoziti
- **Loyalty** — markice / bodovi vezani uz kupnju ili rezervacije

## Arhitektura

```
bookings/
├── backend/       # FastAPI (Python 3.12)
├── frontend/      # Next.js 15 (TypeScript) — admin dashboard
├── widget/        # Embeddable JS widget (Vite + TypeScript)
├── kratos/        # Ory Kratos — identity & session management
├── oathkeeper/    # Ory Oathkeeper — API gateway & authz
└── docker-compose.yml
```

## Pokretanje lokalno

```bash
cp .env.example .env
# Uredite .env i postavite sigurne lozinke

docker compose up
```

| Servis       | URL                            |
|--------------|--------------------------------|
| Admin panel  | http://localhost:3000          |
| API docs     | http://localhost:8000/api/docs |
| Kratos UI    | http://localhost:4433          |
| Mailslurper  | http://localhost:4436          |
| Oathkeeper   | http://localhost:4455          |

## Backend (standalone)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Frontend (standalone)

```bash
cd frontend
npm install
npm run dev
```

## Widget

```bash
cd widget
npm install
npm run build   # generira dist/widget.iife.js
```

Ugradnja na stranicu tenanta:

```html
<div data-bookings data-tenant="moj-slug" data-module="webshop"></div>
<script src="https://cdn.bookings.hr/widget.iife.js" defer></script>
```

## Usklađenost

- **Fiskalizacija**: svako plaćanje poziva Fina eRačun API; JIR se ugrađuje u račun
- **Plaćanje**: CorvusPay sub-merchant model — svaki tenant ima vlastiti store ID
- **Valuta**: EUR (Hrvatska od 2023.)
