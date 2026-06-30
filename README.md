<h1 align="center">🎵 Radio Garden Scraper</h1>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Enigma2](https://img.shields.io/badge/Enigma2-Plugin-ff6600.svg)](https://www.enigma2.net)
[![Python](https://img.shields.io/badge/Python-3.x%2B-blue.svg)](https://www.python.org)

<br>

[![Visitors](https://komarev.com/ghpvc/?username=Belfagor2005&label=Repository%20Views&color=blueviolet)](https://github.com/Belfagor2005)

[![Donate](https://img.shields.io/badge/_-Donate-red.svg?logo=githubsponsors&labelColor=555555&style=for-the-badge)](https://ko-fi.com/lululla)
[![Donate](https://img.shields.io/badge/_-Donate-green.svg?logo=githubsponsors&labelColor=555555&style=for-the-badge)](https://paypal.me/belfagor2005)

</div>

<div align="center">

A high‑performance Python scraper for **Radio Garden** that extracts worldwide radio streams, metadata, and language information with parallel processing and automatic backup.

<br>

<img src="https://play-lh.googleusercontent.com/TuMoS5RrGwz6xmyyYkA56eXukRHNNd2JgldA0wpzVFxiQDAAf9NLuKkTacl29_ltEbr4YvshNOauntxGlrvb=w240-h480-rw" alt="Icon image" width="200">

</div>
---

## 🚀 Features

- **Multi‑threaded scraping** – processes up to 50 countries in parallel for speed.
- **Stream resolution** – follows HTTP redirects to obtain actual stream URLs.
- **Smart language fallback** – uses default languages per country (e.g., `"ita"` for Italy) when metadata is missing.
- **Clean names** – removes control characters from station names.
- **Automatic backup** – saves progress every 1,000 radios to `radio_garden_backup.json`.
- **JSON output** – well‑formatted, UTF‑8 encoded, with no ASCII escape sequences.
- **Country ISO codes** – output uses lowercase two‑letter codes (e.g., `"it"`, `"fr"`).

---

## 📦 Requirements

- Python 3.6+
- `requests` library

Install dependencies:
```bash
pip install requests
```

---

## 📥 Installation

Clone the repository and run the script:
```bash
git clone https://github.com/OwnerPlugins/RadioGardenScraper.git
cd RadioGardenScraper
python3 radiogarden_scraper.py
```

---

## 🛠 How It Works

1. **Fetches the list of all countries** from Radio Garden’s API.
2. **For each country**, it retrieves the page containing all available radio channels.
3. **For each channel**, it:
   - Extracts the station name, country code, and NanoID.
   - Resolves the stream URL by following the redirect (if not already present).
   - Determines the language(s): uses API metadata if available, otherwise falls back to a country‑specific default.
   - Cleans the station name from unwanted control characters.
4. **Saves progress** every 1,000 radios to a backup file.
5. **Outputs** the complete list to `radio_garden.json`.

---

## 📁 Output Format

The generated JSON file contains an array of objects with the following structure:

```json
[
  {
    "name": "Radio Megamix 80",
    "country": "it",
    "languages": ["ita"],
    "stream_urls": ["https://centova.ipstream.it/proxy/megamix80/stream"],
    "nanoid": "EclBWv2P7j1F8F"
  },
  {
    "name": "WIQH 88.3 FM Carlisle High School",
    "country": "us",
    "languages": ["eng"],
    "stream_urls": ["http://96.31.83.86:8074/"],
    "nanoid": "RttrR4CN"
  }
]
```

| Field        | Description                                 |
|--------------|---------------------------------------------|
| `name`       | Station name (cleaned from control chars)   |
| `country`    | ISO 3166‑1 alpha‑2 code (lowercase)         |
| `languages`  | Array of ISO 639‑3 language codes           |
| `stream_urls`| Array of one or more stream URLs            |
| `nanoid`     | Unique identifier for the channel           |

---

## ⚙️ Configuration

You can adjust the following constants at the top of the script:

| Constant               | Default | Description |
|------------------------|---------|-------------|
| `max_workers`          | 50      | Number of concurrent threads. |
| `PLACE_REPORT_INTERVAL`| 50      | Progress report every N countries. |
| `RADIO_REPORT_INTERVAL`| 500     | Radio count report every N stations. |
| `BACKUP_INTERVAL`      | 1000    | Backup every N radios. |

---

## 📌 Notes

- The script respects Radio Garden’s rate limits by using reasonable timeouts and parallelisation.
- **No video/audio content is stored** – only metadata and stream URLs.
- The backup file (`radio_garden_backup.json`) can be used to resume from a partial run (manual merge required).

---

## ⚖️ Legal Disclaimer

**The project author is not responsible for how this software is used by others.**  
The author assumes no responsibility for any misuse. It is not intended to be used for accessing or distributing copyrighted materials without authorization. Users are solely responsible for determining the legality of their actions.

**Warning:**  
This repository has no control over the streams, links, or the legality of the content provided by the different hosts (including all mirror sites). It is the end user's responsibility to ensure the legal use of these streams, and we strongly recommend verifying that the content complies with all applicable laws, including copyright laws and regulations of your country's jurisdiction before use.

No video files are stored in this repository. To remove content from the web, contact the hosting provider (not GitHub or repository maintainers).

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

