# import os
# import time
# import pymongo
# from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# # ✅ Secure MongoDB Connection (Use GitHub Secrets)
# MONGO_URI = os.getenv("MONGO_URI")  # Get MongoDB URI from environment variable
# DB_NAME = "GameStats"
# COLLECTION_NAME = "steam_charts"

# try:
#     client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=60000)
#     db = client[DB_NAME]
#     collection = db[COLLECTION_NAME]
#     print("✅ Connected to MongoDB Atlas!")
# except pymongo.errors.ServerSelectionTimeoutError:
#     print("❌ Failed to connect to MongoDB. Ensure MongoDB URI is correct.")

# # ✅ SteamCharts Base URL
# BASE_URL = "https://steamcharts.com/top"

# # ✅ Selenium Setup
# def init_driver():
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# def scrape_page(driver, page_number):
#     url = f"{BASE_URL}/p.{page_number}"
#     driver.get(url)
    
#     try:
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "table.common-table tbody tr"))
#         )
#         games = driver.find_elements(By.CSS_SELECTOR, "table.common-table tbody tr")
        
#         for game in games:
#             cols = game.find_elements(By.TAG_NAME, "td")
#             if len(cols) >= 5:  # Ensure there are enough columns
#                 rank = cols[0].text.strip()
#                 name = cols[1].text.strip()
#                 current_players = cols[2].text.strip()
#                 hours_played = cols[4].text.strip()  # Corrected index for "Hours Played"
                
#                 print(f"Extracted: {name} | Rank: {rank} | Current: {current_players} | Hours: {hours_played}")
                
#                 game_data = {
#                     "rank": rank,
#                     "name": name,
#                     "current_players": current_players,
#                     "hours_played": hours_played if hours_played else "N/A",
#                     "date": datetime.now().strftime("%Y-%m-%d"),
#                     "timestamp": time.time()
#                 }
#                 collection.update_one(
#                     {"name": name, "date": game_data["date"]},
#                     {"$set": game_data},
#                     upsert=True
#                 )
#                 print(f"✅ Updated: {name}")
#     except Exception as e:
#         print("❌ Error scraping data:", e)

# def scrape_website():
#     driver = init_driver()
#     for page in range(1, 3):  # Scraping pages 1 and 2
#         print(f"📄 Scraping page {page}...")
#         scrape_page(driver, page)
    
#     driver.quit()

# def monitor_system():
#     while True:
#         print("🔄 Running Scraper...")
#         scrape_website()
#         time.sleep(300)  # Runs every 5 minutes

# if __name__ == "__main__":
#     monitor_system()
