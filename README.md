# Real Python Scraper
Scrapes article cards from [realpython.com](https://realpython.com/) and saves them to a Postgres database.

## How it works
- Scrapes the homepage with `cloudscraper` + `beautifulsoup4`, with an RSS feed fallback
- Retries failed requests up to 5 times
- Stores articles (title, link, date, categories) in Postgres

## Quick start
```bash
docker compose up --build -d
docker compose logs app
```

## Development
```bash
docker compose exec db psql -U scraper -d scraper
```
See [commands.md](commands.md) for more.
