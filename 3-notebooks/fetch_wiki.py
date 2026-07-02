import requests, time, re, json
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_URL = "https://en.wikipedia.org/w/api.php"
HEADERS = {"User-Agent": "CulturomicsEssayBot/1.0 (academic)"}
CACHE   = Path("corpus_cache.json")

# Создаём сессию с автоматическим retry на уровне TCP
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.headers.update(HEADERS)

ARTICLES = [

    # SCIENCE AND KNOWLEDGE
    "Albert_Einstein", "Charles_Darwin", "Photosynthesis", "DNA",
    "Black_hole", "Artificial_intelligence", "Climate_change",
    "COVID-19_pandemic", "Human_genome", "Wikipedia",

    # HISTORY AND POLITICS
    "World_War_II", "French_Revolution", "Cold_War",
    "September_11_attacks", "Arab_Spring", "Occupy_Wall_Street",
    "MeToo_movement", "Black_Lives_Matter", "WikiLeaks", "War_on_terror",

    # TECHNOLOGY: HARDWARE AND PLATFORMS
    "iPhone", "Android_(operating_system)", "iPod",
    "Tesla_(car_company)",          # исправлено: запятая убрана
    "SpaceX", "Google", "Amazon_(company)", "Microsoft",

    # SOCIAL MEDIA AND INTERNET
    "Facebook", "YouTube", "Twitter", "Instagram", "Reddit",
    "TikTok", "Snapchat", "MySpace", "Napster", "iTunes",
    "Netflix", "Spotify", "Zoom_(software)", "Remote_work",

    # AI AND EMERGING TECH
    "ChatGPT", "DALL-E", "Virtual_reality", "Augmented_reality",
    "Non-fungible_token", "Metaverse", "Podcast",

    # FILM AND TV
    "Harry_Potter", "The_Lord_of_the_Rings", "Shrek_(film)",
    "Avatar_(2009_film)", "Avengers_Endgame",  # исправлено: двоеточие убрано
    "Barbie_(film)", "Oppenheimer_(film)", "Frozen_(2013_film)",
    "Black_Panther_(film)", "Joker_(2019_film)", "Game_of_Thrones",
    "Breaking_Bad", "Stranger_Things", "Squid_Game",
    "Marvel_Cinematic_Universe",

    # GAMING
    "Minecraft", "Fortnite", "Pokémon_Go", "Among_Us",
    "Grand_Theft_Auto_V", "The_Last_of_Us", "League_of_Legends",
    "World_of_Warcraft", "Esports", "Roblox",

    # MEMES AND INTERNET CULTURE
    "Internet_meme", "Rickrolling", "Doge_(meme)", "Pepe_the_Frog",
    "Gangnam_Style", "Ice_Bucket_Challenge", "Harlem_Shake_(meme)",

    # MUSIC AND EVENTS  ← исправлено: реальные музыкальные статьи
    "K-pop", "BTS_(band)", "BLACKPINK",
    "Eurovision_Song_Contest",
    "Coachella_Valley_Music_and_Arts_Festival",
    "Studio_Ghibli", "Anime", "Manga", "Cosplay",

    # SPORT AND CULTURE
    "2024_Summer_Olympics", "Pride_parade",

]
YEARS = list(range(2004, 2025))

def clean(raw):
    t = re.sub(r'\[\[[a-z\-]{2,10}:[^\]]+\]\]', ' ', raw)
    t = re.sub(r'\{\{[^{}]*\}\}', ' ', t)
    t = re.sub(r'\[\[(?:File|Image|Category):[^\]]*\]\]', ' ', t, flags=re.I)
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def get_json(params, label):
    """Make API request with retry on empty/timeout."""
    for attempt in range(4):
        time.sleep(10 + attempt * 5)  # 10s, 15s, 20s, 25s
        try:
            r = session.get(API_URL, params=params, timeout=45)
            if len(r.text) < 50:
                print(f"    empty ({label}), retry {attempt+1}/4")
                continue
            return r.json()
        except requests.exceptions.Timeout:
            print(f"    timeout ({label}), retry {attempt+1}/4, waiting {30*(attempt+1)}s")
            time.sleep(30 * (attempt + 1))
        except Exception as e:
            print(f"    error ({label}): {e}, retry {attempt+1}/4")
            time.sleep(30 * (attempt + 1))
    print(f"    FAILED after 4 attempts: {label}")
    return None

def fetch(article, year):
    data = get_json({
        "action": "query", "titles": article, "prop": "revisions",
        "rvprop": "ids|timestamp", "rvlimit": 1, "rvdir": "newer",
        "rvstart": f"{year}-01-01T00:00:00Z",
        "rvend":   f"{year}-06-01T00:00:00Z",
        "format":  "json",
    }, f"step1 {article}/{year}")

    if not data:
        return ""
    pages = data.get("query", {}).get("pages", {})
    page  = list(pages.values())[0]
    if "missing" in page:
        return ""
    revs = page.get("revisions", [])
    if not revs:
        return ""
    rev_id = revs[0]["revid"]

    data2 = get_json({
        "action": "query", "revids": rev_id, "prop": "revisions",
        "rvprop": "content", "rvslots": "main", "format": "json",
    }, f"step2 {article}/{year}")

    if not data2:
        return ""
    try:
        raw = list(data2["query"]["pages"].values())[0]
        raw = raw["revisions"][0]["slots"]["main"]["*"]
        return clean(raw)
    except Exception as e:
        print(f"    parse error {article}/{year}: {e}")
        return ""

# Load cache
corpus = json.loads(CACHE.read_text()) if CACHE.exists() else {}
success = sum(1 for a in corpus for y in corpus.get(a,{}) if corpus[a].get(y))
total   = len(ARTICLES) * len(YEARS)
print(f"Cache: {success} entries. Target: {total}")

for article in ARTICLES:
    if article not in corpus:
        corpus[article] = {}
    art_ok = sum(1 for y in YEARS if corpus[article].get(str(y)))
    for year in YEARS:
        yk = str(year)
        if corpus[article].get(yk):
            continue
        print(f"Fetching {article}/{year}...")
        text = fetch(article, year)
        corpus[article][yk] = text
        if text:
            art_ok += 1
            print(f"  OK: {len(text)} chars")
        CACHE.write_text(json.dumps(corpus, ensure_ascii=False))
    print(f"[done] {article}: {art_ok}/{len(YEARS)} years")
    time.sleep(20)

non_empty = sum(1 for a in corpus for y in corpus[a] if corpus[a][y])
print(f"\nDONE. Non-empty: {non_empty}/{total}")
