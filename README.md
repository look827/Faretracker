# Flight Fare Fluctuation & Notification System

A full-stack fare monitor with FastAPI + SQLAlchemy/PostgreSQL, React/TypeScript, Recharts, a background scheduler, Telegram/email notification adapters, and a clearly labeled mock provider.

## Important data-source rule
The included provider is **mock data**. The app never presents it as live airline inventory. No website scraping is used. Replace `MockFlightDataProvider` with a provider adapter for a legitimate fare API before treating results as live fares.

## Local development
### Backend
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Open http://localhost:8000/docs.

### Frontend
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173.

The frontend defaults to `http://localhost:8000/api`; set `VITE_API_URL` if needed.

## PostgreSQL
Set `DATABASE_URL` to a SQLAlchemy PostgreSQL URL, for example:
`postgresql+psycopg://user:password@host:5432/flightmonitor`
and install a PostgreSQL driver such as `psycopg[binary]` in `backend/requirements.txt`.

## Docker
```bash
cp .env.example .env
# fill secrets if Telegram/email are desired
docker compose up --build
```
Frontend: http://localhost:5173
Backend API/docs: http://localhost:8000/docs

## Telegram
1. Create a bot with BotFather and obtain its token.
2. Send a message to the bot/chat and determine the chat ID.
3. Put `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`.
4. A triggered event is sent by the Telegram adapter.

The code records notification events and uses a unique event key to avoid duplicate delivery for the same monitor/event/price row.

## Email
Set SMTP host, port, username, password, and from address in `.env`. The reusable `EmailNotifier` adapter accepts a recipient address. Add a user notification-recipient field before exposing it in a multi-user production UI.

## Real fare API integration
Implement `FlightDataProvider` in `backend/app/providers/` and return `FlightQuote` objects. Keep the provider responsible only for retrieving/normalizing provider data. Do not scrape sites whose terms prohibit automated access. A real adapter should use provider credentials from environment variables and set `source` to a provider identifier, never `mock`.

Example interface:
```python
class RealProvider(FlightDataProvider):
    def search_flights(self, origin, destination, departure_date, return_date=None, airline=None, stops=None):
        # Call provider API, normalize results, return list[FlightQuote]
        ...
```
Then inject that provider into `check_monitor()` instead of `MockFlightDataProvider`.

## Monitoring algorithm
For each successful check:
1. Fetch normalized quotes.
2. Select the lowest returned fare for the monitor query.
3. Read the immediately previous stored price.
4. Persist a new immutable `flight_prices` row with timestamp and source.
5. Compute absolute and percentage change.
6. Compare against configurable thresholds.
7. Detect new low/high and target-price crossing.
8. Send enabled notifications and log each notification attempt.

API failure/no-result never creates a price of zero and never creates a price-change event. It returns `DATA_UNAVAILABLE`.

## History
`flight_prices` is append-only from the application perspective. The graph endpoint supports `24h`, `7d`, `30d`, `90d`, and `all`.

## Tests
```bash
cd backend
pytest -q
```
Tests cover percentage/change direction and API health; extend provider and notification integration tests before production deployment.

## Production hardening
- Add authentication/authorization before multi-user deployment.
- Add encrypted secret storage and TLS.
- Add rate limiting and provider-specific quota handling.
- Use a durable task queue such as Celery/Redis if monitoring volume grows.
- Add structured logging/metrics and alert delivery retry/backoff.
- Add migrations with Alembic rather than `create_all`.
- Add provider-specific fare identity so multiple flight options can be retained separately instead of only the cheapest quote per monitor.
