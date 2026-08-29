from scraper import db, scraper


def main():
    rows = scraper.scrape()
    conn = db.connect()
    db.init_db(conn)
    db.save_rows(conn, rows)
    print(f"Saved {len(rows)} articles")
    conn.close()


if __name__ == "__main__":
    main()