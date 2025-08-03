import requests
import time
import telegram
from bs4 import BeautifulSoup

BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'
bot = telegram.Bot(token=BOT_TOKEN)
sent_links = set()

KEYWORDS = ["python", "dsa", "machine learning", "data structures"]

def send_message(msg):
    bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown')

def check_naukri_jobs():
    url = "https://www.naukri.com/internship-jobs?k=python%20internship&l=India"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all("article", class_="jobTuple")

    for job in jobs:
        title = job.find("a", class_="title").text.strip().lower()
        company = job.find("a", class_="subTitle").text.strip()
        link = job.find("a", class_="title")["href"]
        if link not in sent_links and any(k in title for k in KEYWORDS):
            message = f"🧠 {title.title()}\n🏢 {company}\n🔗 [Apply Now]({link})"
            send_message(message)
            sent_links.add(link)

def check_internshala_jobs():
    url = "https://internshala.com/internships"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    internships = soup.find_all("div", class_="individual_internship")

    for post in internships:
        title = post.find("div", class_="heading_4_5").get_text(strip=True).lower()
        company = post.find("a", class_="link_display_like_text").get_text(strip=True)
        link = "https://internshala.com" + post.find("a")["href"]
        if link not in sent_links and any(k in title for k in KEYWORDS):
            message = f"📘 {title.title()}\n🏢 {company}\n🔗 [Apply Now]({link})"
            send_message(message)
            sent_links.add(link)

def check_linkedin_jobs():
    query = "python OR machine learning OR DSA internship site:linkedin.com"
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    for result in soup.select('div.tF2Cxc'):
        title = result.select_one('h3').text.lower()
        link = result.select_one('a')['href']
        if link not in sent_links and any(k in title for k in KEYWORDS):
            message = f"🌐 {title.title()}\n🔗 [Apply Now]({link})"
            send_message(message)
            sent_links.add(link)

# Single run for scheduled job
check_naukri_jobs()
check_internshala_jobs()
check_linkedin_jobs()