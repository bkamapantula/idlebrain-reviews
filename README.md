# Idlebrain reviews

This is a repository for scripts to parse idlebrain.com reviews.

We explore the distribution of reviews across the years.

## Install dependencies

```bash
pip install -e .  # picks up packages from requirements.txt and installs
```

## Fetch links from archive page

[Idlebrain Archive page](http://www.idlebrain.com/movie/archive/index.html) lists movies.

### Step 1 - Create database

Create `reviews.db` file. Open it with SqliteBrowser and create `movies` table with the following schema:

```sql
CREATE TABLE `movies` ( `id` INTEGER, `name` TEXT, `url` TEXT, `release_date` TEXT, `rating` TEXT )
```

We fetch the archive list, save the links in a `sqlite` database named `reviews.db` (`movies` table). For this, run `parse_reviews()` in `parse.py`.

This updates `movies` table with movie entries.

## Fetch reviews for all movies

### Step 1 - Create data directory

Create `data` directory in the root directory.

### Step 2 - Scrape movie reviews

For this, run `fetch_data_from_IB()` in `parse.py`. This creates `movie_name.html` in `data/` directory.
