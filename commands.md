# Commands

```bash
# Build images, start db, run the scraper once (db stays running in background)
docker compose up --build -d

# Check the scrape result and retry progress
docker compose logs app

# Open a psql console to inspect the stored articles
docker compose exec db psql -U scraper -d scraper

# Example queries in psql: show all articles, or sorted by date
SELECT * FROM articles;
SELECT id, title, published_at, categories FROM articles ORDER BY published_at DESC;

# Leave the psql console
exit

# Stop containers (data in the db volume is kept)
docker compose down

# Stop containers AND delete the database volume (all data lost)
docker compose down -v

# Stop containers and remove leftovers from older compose files
docker compose down --remove-orphans
```