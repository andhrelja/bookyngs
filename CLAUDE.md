# CLAUDE.md

## Project

Croatian SMB SaaS platform — multi-tenant, three independently licensable modules:
**webshop**, **booking**, **loyalty**. Tenants are Croatian small businesses (wineries,
accommodation, rental/service). All payments and receipts must comply with Croatian
fiscal law (Fina eRačun) and use CorvusPay for card payments.

## Monorepo layout

```
backend/    FastAPI + SQLAlchemy async (Python 3.12)
frontend/   Next.js 15 App Router + Tailwind (TypeScript)
widget/     Vite IIFE embeddable widget (TypeScript)
kratos/     Ory Kratos identity config
oathkeeper/ Ory Oathkeeper API gateway config
```

## Development commands

### Full stack
```bash
cp .env.example .env   # fill POSTGRES_PASSWORD and SECRET_KEY
docker compose up
```

| Service     | URL                            |
|-------------|--------------------------------|
| Admin panel | http://localhost:3000          |
| API docs    | http://localhost:8000/api/docs |
| Kratos      | http://localhost:4433          |
| Mailslurper | http://localhost:4436          |
| Oathkeeper  | http://localhost:4455          |

### Backend (standalone)
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

After changing models, always generate and apply a migration:
```bash
alembic revision --autogenerate -m "describe what changed"
alembic upgrade head
```

### Frontend (standalone)
```bash
cd frontend
npm install
npm run dev
```

### Widget
```bash
cd widget
npm install
npm run build   # outputs dist/widget.iife.js
npm run dev     # watch mode
```

## Architecture

### Auth flow
1. User authenticates via Ory Kratos (browser session cookie `ory_kratos_session`)
2. Oathkeeper validates the cookie by calling `http://kratos:4433/sessions/whoami`
3. Oathkeeper injects `X-Kratos-Authenticated-Identity-Id: <kratos-identity-uuid>` into backend requests
4. `backend/app/dependencies/auth.py:get_session()` reads that header
5. `backend/app/dependencies/tenant.py:get_current_tenant()` resolves the `Tenant` row via `owner_kratos_id`

In local development without Oathkeeper, `get_session()` falls back to calling Kratos directly with the cookie.

### Multi-tenancy
Every data row is scoped to a `tenant_id`. All queries in routers **must** include `tenant_id == tenant.id` in their WHERE clause. Never query across tenants.

Module access is enforced by dependency functions:
- `require_webshop` — use on all `/api/webshop/` routes
- `require_booking` — use on all `/api/booking/` routes
- `require_loyalty` — use on all `/api/loyalty/` routes

These return 403 with a Croatian error message if the tenant's flag is off.

### Adding a new API route
1. Add the SQLAlchemy model to `backend/app/models/<module>.py` and register it in `backend/app/models/__init__.py`
2. Add Pydantic schemas (Read/Create/Update) to `backend/app/schemas/<module>.py`
3. Add route to `backend/app/routers/<module>.py` using the appropriate `require_<module>` dependency
4. Generate a migration: `alembic revision --autogenerate -m "..."` then `alembic upgrade head`

### Adding a frontend page
- All dashboard pages live under `frontend/src/app/(dashboard)/`
- Use `frontend/src/lib/api.ts` for all API calls — `api.get<T>()`, `api.post<T>()`, `api.patch<T>()`, `api.delete()`
- Error messages surfaced to users must be in Croatian

## Code conventions

### Backend (Python)
- Python 3.12 — use built-in `list[T]`, `dict[K,V]`, `X | None` (no `typing` imports needed)
- SQLAlchemy ORM with `Mapped` / `mapped_column` — no legacy `Column()` style
- All DB queries are async: `await db.execute(select(...))`, `await db.commit()`
- Use `result.scalar_one_or_none()` for single-row fetches; handle `None` with a 404 immediately
- Soft-delete pattern: set `is_active = False`, never `db.delete()`
- All user-facing error `detail` strings are in Croatian
- All monetary values use `Decimal` (never `float`)
- VAT default is 25% (Croatian standard). Always store `vat_rate` alongside the price at the time of sale — never recalculate from the current product rate

### Frontend (TypeScript)
- Next.js 15 App Router — Server Components by default; add `"use client"` only when needed (event handlers, hooks, `usePathname`)
- All user-visible text defaults to Croatian; English only in the widget when `data-locale="en"`
- Tailwind for all styling — no CSS modules, no inline style objects in components
- Use `clsx` for conditional class names
- Fetch data with `src/lib/api.ts` — never call `fetch()` directly in components

### Widget (TypeScript)
- Zero runtime dependencies — plain TypeScript compiled to a single IIFE
- Each module (`webshop`, `booking`, `loyalty`) is a separate file under `widget/src/modules/` and is dynamically imported at mount time to keep initial bundle tiny
- Inline styles only (no external CSS) so the widget renders correctly on any host page
- Never use `document.cookie` — the widget runs on the tenant's domain, not the platform's

## Compliance — do not bypass

### Fina eRačun (fiscalization)
- `backend/app/services/fiscalization.py` is currently a stub
- Before going live, replace with a real SOAP implementation using the tenant's `.p12` certificate
- Every `Order` and `Reservation` that receives payment **must** be fiscalized; store `jir` and `zki` on the row
- Test endpoint: `https://cistest.apis-it.hr:8449/FiskalizacijaServiceTest`
- Production endpoint: `https://cis.porezna-uprava.hr:8449/FiskalizacijaService`
- Reference: Zakon o fiskalizaciji u prometu gotovinom (NN 133/12, 115/16, 106/18)

### CorvusPay
- `backend/app/services/corvuspay.py` is currently a stub
- Each tenant operates under their own CorvusPay merchant account (sub-merchant model)
- `corvus_store_id` and `corvus_secret_key` are stored per-tenant on the `Tenant` model
- Always verify the callback signature before marking an order as paid

### Currency
- Croatia adopted EUR on 1 January 2023 — all amounts are in EUR
- No HRK anywhere in the codebase

## Tenant provisioning
Tenants are created manually by the operator (no self-serve registration). The flow:
1. User registers via Kratos — this creates a Kratos identity with a UUID
2. Operator creates a `Tenant` row in the DB with `owner_kratos_id = <kratos-uuid>` and sets the module flags
3. The tenant's admin dashboard immediately reflects only the licensed modules

There is no operator-facing UI yet — provisioning is done directly in the DB or via a future `/api/admin/` route.

## What this project is not
- Not a website builder
- Not an ERP or inventory system
- Not a marketplace
- Not an accounting system (it issues fiscal receipts and exports data; it does not do bookkeeping)
