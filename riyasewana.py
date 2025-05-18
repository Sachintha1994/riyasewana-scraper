from scraper import scrape_model  # if your scraper is in scraper.py

model_config = {
    "url": "https://riyasewana.com/search/suzuki/wagon-r-fz",
    "title": "Suzuki Wagon R FZ - New Listings",
    "email_to": "thilina.sachintha17@gmail.com"
}

scrape_model(model_config, pages=1)
