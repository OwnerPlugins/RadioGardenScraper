import json
import requests
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://radio.garden/api/ara/content"
OUT = os.getcwd() + "/radio_garden.json"
BACKUP_OUT = os.getcwd() + "/radio_garden_backup.json"

S = requests.Session()
S.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://radio.garden/"
})

# ------------------------------------------------------------
# Clean text: remove control characters
# ------------------------------------------------------------
def clean_text(text):
    if not text:
        return text
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return cleaned

# ============================================================
# ISO_DATA: only country names
# ============================================================
ISO_DATA = {
    "AD": "Andorra",
    "AE": "United Arab Emirates",
    "AF": "Afghanistan",
    "AG": "Antigua and Barbuda",
    "AI": "Anguilla",
    "AL": "Albania",
    "AM": "Armenia",
    "AO": "Angola",
    "AR": "Argentina",
    "AS": "American Samoa",
    "AT": "Austria",
    "AU": "Australia",
    "AW": "Aruba",
    "AX": "Åland Islands",
    "AZ": "Azerbaijan",
    "BA": "Bosnia and Herzegovina",
    "BB": "Barbados",
    "BD": "Bangladesh",
    "BE": "Belgium",
    "BF": "Burkina Faso",
    "BG": "Bulgaria",
    "BH": "Bahrain",
    "BI": "Burundi",
    "BJ": "Benin",
    "BL": "Saint Barthélemy",
    "BM": "Bermuda",
    "BN": "Brunei",
    "BO": "Bolivia",
    "BQ": "Bonaire",
    "BR": "Brazil",
    "BS": "Bahamas",
    "BT": "Bhutan",
    "BV": "Bouvet Island",
    "BW": "Botswana",
    "BY": "Belarus",
    "BZ": "Belize",
    "CA": "Canada",
    "CC": "Cocos (Keeling) Islands",
    "CD": "DR Congo",
    "CF": "Central African Republic",
    "CG": "Congo",
    "CH": "Switzerland",
    "CI": "Ivory Coast",
    "CK": "Cook Islands",
    "CL": "Chile",
    "CM": "Cameroon",
    "CN": "China",
    "CO": "Colombia",
    "CR": "Costa Rica",
    "CU": "Cuba",
    "CV": "Cape Verde",
    "CW": "Curaçao",
    "CY": "Cyprus",
    "CZ": "Czechia",
    "DE": "Germany",
    "DJ": "Djibouti",
    "DK": "Denmark",
    "DM": "Dominica",
    "DO": "Dominican Republic",
    "DZ": "Algeria",
    "EC": "Ecuador",
    "EE": "Estonia",
    "EG": "Egypt",
    "EH": "Western Sahara",
    "ER": "Eritrea",
    "ES": "Spain",
    "ET": "Ethiopia",
    "FI": "Finland",
    "FJ": "Fiji",
    "FK": "Falkland Islands",
    "FM": "Micronesia",
    "FO": "Faroe Islands",
    "FR": "France",
    "GA": "Gabon",
    "GB": "United Kingdom",
    "GD": "Grenada",
    "GE": "Georgia",
    "GF": "French Guiana",
    "GG": "Guernsey",
    "GH": "Ghana",
    "GI": "Gibraltar",
    "GL": "Greenland",
    "GM": "Gambia",
    "GN": "Guinea",
    "GP": "Guadeloupe",
    "GQ": "Equatorial Guinea",
    "GR": "Greece",
    "GS": "South Georgia and the South Sandwich Islands",
    "GT": "Guatemala",
    "GU": "Guam",
    "GW": "Guinea-Bissau",
    "GY": "Guyana",
    "HK": "Hong Kong",
    "HN": "Honduras",
    "HR": "Croatia",
    "HT": "Haiti",
    "HU": "Hungary",
    "ID": "Indonesia",
    "IE": "Ireland",
    "IL": "Israel",
    "IM": "Isle of Man",
    "IN": "India",
    "IO": "British Indian Ocean Territory",
    "IQ": "Iraq",
    "IR": "Iran",
    "IS": "Iceland",
    "IT": "Italy",
    "JM": "Jamaica",
    "JO": "Jordan",
    "JP": "Japan",
    "KE": "Kenya",
    "KG": "Kyrgyzstan",
    "KH": "Cambodia",
    "KI": "Kiribati",
    "KM": "Comoros",
    "KN": "Saint Kitts and Nevis",
    "KP": "North Korea",
    "KR": "South Korea",
    "KW": "Kuwait",
    "KY": "Cayman Islands",
    "KZ": "Kazakhstan",
    "LA": "Laos",
    "LB": "Lebanon",
    "LC": "Saint Lucia",
    "LI": "Liechtenstein",
    "LK": "Sri Lanka",
    "LR": "Liberia",
    "LS": "Lesotho",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "LV": "Latvia",
    "LY": "Libya",
    "MA": "Morocco",
    "MC": "Monaco",
    "MD": "Moldova",
    "ME": "Montenegro",
    "MG": "Madagascar",
    "MH": "Marshall Islands",
    "MK": "North Macedonia",
    "ML": "Mali",
    "MM": "Myanmar",
    "MN": "Mongolia",
    "MO": "Macau",
    "MP": "Northern Mariana Islands",
    "MQ": "Martinique",
    "MR": "Mauritania",
    "MS": "Montserrat",
    "MT": "Malta",
    "MU": "Mauritius",
    "MV": "Maldives",
    "MW": "Malawi",
    "MX": "Mexico",
    "MY": "Malaysia",
    "MZ": "Mozambique",
    "NA": "Namibia",
    "NC": "New Caledonia",
    "NE": "Niger",
    "NF": "Norfolk Island",
    "NG": "Nigeria",
    "NI": "Nicaragua",
    "NL": "Netherlands",
    "NO": "Norway",
    "NP": "Nepal",
    "NR": "Nauru",
    "NU": "Niue",
    "NZ": "New Zealand",
    "OM": "Oman",
    "PA": "Panama",
    "PE": "Peru",
    "PF": "French Polynesia",
    "PG": "Papua New Guinea",
    "PH": "Philippines",
    "PK": "Pakistan",
    "PL": "Poland",
    "PM": "Saint Pierre and Miquelon",
    "PN": "Pitcairn Islands",
    "PR": "Puerto Rico",
    "PS": "Palestine",
    "PT": "Portugal",
    "PW": "Palau",
    "PY": "Paraguay",
    "QA": "Qatar",
    "RE": "Réunion",
    "RO": "Romania",
    "RS": "Serbia",
    "RU": "Russia",
    "RW": "Rwanda",
    "SA": "Saudi Arabia",
    "SB": "Solomon Islands",
    "SC": "Seychelles",
    "SD": "Sudan",
    "SE": "Sweden",
    "SG": "Singapore",
    "SH": "Saint Helena",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "SL": "Sierra Leone",
    "SM": "San Marino",
    "SN": "Senegal",
    "SO": "Somalia",
    "SR": "Suriname",
    "SS": "South Sudan",
    "ST": "São Tomé and Príncipe",
    "SV": "El Salvador",
    "SX": "Sint Maarten",
    "SY": "Syria",
    "SZ": "Eswatini",
    "TC": "Turks and Caicos Islands",
    "TD": "Chad",
    "TF": "French Southern Territories",
    "TG": "Togo",
    "TH": "Thailand",
    "TJ": "Tajikistan",
    "TK": "Tokelau",
    "TL": "East Timor",
    "TM": "Turkmenistan",
    "TN": "Tunisia",
    "TO": "Tonga",
    "TR": "Türkiye",
    "TT": "Trinidad and Tobago",
    "TV": "Tuvalu",
    "TW": "Taiwan",
    "TZ": "Tanzania",
    "UA": "Ukraine",
    "UG": "Uganda",
    "UK": "United Kingdom",
    "US": "United States",
    "UY": "Uruguay",
    "UZ": "Uzbekistan",
    "VA": "Vatican City",
    "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela",
    "VG": "British Virgin Islands",
    "VI": "U.S. Virgin Islands",
    "VN": "Vietnam",
    "VU": "Vanuatu",
    "WF": "Wallis and Futuna",
    "WS": "Samoa",
    "XC": "Northern Cyprus",
    "XK": "Kosovo",
    "XS": "Somaliland",
    "YE": "Yemen",
    "YT": "Mayotte",
    "ZA": "South Africa",
    "ZM": "Zambia",
    "ZW": "Zimbabwe"
}

# =========================
# Inverted map: country name -> iso code (lowercase)
# =========================
COUNTRY_MAP = {
    v.lower(): k.lower()
    for k, v in ISO_DATA.items()
}

# =========================
# Default language per country
# =========================
DEFAULT_LANGUAGES = {
    "it": "ita",
    "fr": "fra",
    "de": "deu",
    "es": "spa",
    "pt": "por",
    "nl": "nld",
    "en": "eng",
    "pl": "pol",
    "ru": "rus",
    "ja": "jpn",
    "zh": "zho",
    "ar": "ara",
    "hi": "hin",
    "bn": "ben",
    "ur": "urd",
    "pa": "pan",
    "ta": "tam",
    "te": "tel",
    "ml": "mal",
    "kn": "kan",
    "gu": "guj",
    "or": "ori",
    "mr": "mar",
    "si": "sin",
    "th": "tha",
    "vi": "vie",
    "ms": "msa",
    "id": "ind",
    "tl": "tgl",
    "tr": "tur",
    "el": "ell",
    "bg": "bul",
    "sr": "srp",
    "hr": "hrv",
    "cs": "ces",
    "sk": "slk",
    "hu": "hun",
    "ro": "ron",
    "uk": "ukr",
    "be": "bel",
    "lt": "lit",
    "lv": "lav",
    "et": "est",
    "fi": "fin",
    "sv": "swe",
    "no": "nor",
    "da": "dan",
    "is": "isl",
    "ga": "gle",
    "gd": "gla",
    "cy": "cym",
    "mt": "mlt",
    "sq": "sqi",
    "mk": "mkd",
    "sl": "slv",
    "bs": "bos",
    "ca": "cat",
    "eu": "eus",
    "gl": "glg",
    "oc": "oci",
    "an": "arg",
    "ast": "ast",
    "co": "cos",
    "ku": "kur",
    "fa": "fas",
    "ps": "pus",
    "prs": "prs",
    "tuk": "tuk",
    "uz": "uzb",
    "kk": "kaz",
    "ky": "kir",
    "tg": "tgk",
    "tk": "tuk",
    "mn": "mon",
    "ne": "nep",
    "km": "khm",
    "lo": "lao",
    "my": "mya",
    "dz": "dzo",
    "bo": "bod",
    "sa": "san",
    "kok": "kok",
    "mni": "mni",
    "raj": "raj",
    "bho": "bho",
    "mai": "mai",
    "mag": "mag",
}

def get_default_languages(country_code):
    lang = DEFAULT_LANGUAGES.get(country_code)
    if lang:
        return [lang]
    return ["eng"]

# =========================
# Utility functions
# =========================
def get_country_code(name):
    if not name:
        return None
    return COUNTRY_MAP.get(name.lower())

def get_json(url):
    try:
        r = S.get(url, timeout=10)
        if r.ok:
            return r.json()
    except:
        return None

def resolve_stream(cid):
    """Follow redirect to get the actual stream URL"""
    try:
        r = S.get(BASE + "/listen/" + cid + "/channel.mp3",
                  allow_redirects=False, timeout=8)
        if r.status_code in (301, 302, 307, 308):
            return r.headers.get("Location")
    except:
        pass
    return None

def process_place(place):
    page = get_json(BASE + "/page/" + place["id"])
    if not page:
        return []

    country_name = place.get("country")
    country_code = get_country_code(country_name)
    if not country_code:
        return []

    radios = []
    for block in page.get("data", {}).get("content", []):
        if block.get("itemsType") != "channel":
            continue
        for item in block.get("items", []):
            pg = item.get("page", {})
            url = pg.get("url", "")
            if not url.startswith("/listen/"):
                continue
            cid = url.rsplit("/", 1)[-1]

            # 1) Try to get the stream from the page (if it's a valid URL)
            stream = pg.get("stream")
            # If it's not a valid URL (no http), or None, resolve it
            if not stream or not stream.startswith(("http://", "https://")):
                stream = resolve_stream(cid)
            # If still None, keep whatever we had (but it might be incomplete)

            # Language
            lang_data = pg.get("languages") or pg.get("language")
            if isinstance(lang_data, str):
                languages = [lang_data] if lang_data else get_default_languages(country_code)
            elif isinstance(lang_data, list) and lang_data:
                languages = lang_data
            else:
                languages = get_default_languages(country_code)

            raw_name = pg.get("title")
            clean_name = clean_text(raw_name) if raw_name else None

            radios.append({
                "name": clean_name,
                "country": country_code,
                "languages": languages,
                "stream_urls": [stream] if stream else [],
                "nanoid": cid,
            })
    return radios

# ============================================================
# MAIN
# ============================================================
print("📥 loading places...")
pdata = get_json(BASE + "/places")
places = pdata["data"]["list"]
total_places = len(places)
print(f"Total places to process: {total_places}")

all_radios = []
seen = set()
processed = 0
total_radios_found = 0
last_backup_count = 0

PLACE_REPORT_INTERVAL = 50
RADIO_REPORT_INTERVAL = 500
BACKUP_INTERVAL = 1000

with ThreadPoolExecutor(max_workers=50) as ex:
    futures = [ex.submit(process_place, p) for p in places]

    for f in as_completed(futures):
        res = f.result()
        processed += 1
        new_radios = 0
        for r in res:
            if r["nanoid"] in seen:
                continue
            seen.add(r["nanoid"])
            all_radios.append(r)
            new_radios += 1
        total_radios_found += new_radios

        if processed % PLACE_REPORT_INTERVAL == 0 or processed == total_places:
            print(f"Progress: {processed}/{total_places} places, found {total_radios_found} radios so far")
        if total_radios_found % RADIO_REPORT_INTERVAL < new_radios:
            print(f"Radio count: {total_radios_found} (processed {processed}/{total_places} places)")

        # Backup every 1000 radios
        if total_radios_found - last_backup_count >= BACKUP_INTERVAL:
            print(f"💾 Backup: saving {len(all_radios)} radios to {BACKUP_OUT}")
            with open(BACKUP_OUT, "w", encoding="utf-8") as bf:
                json.dump(all_radios, bf, ensure_ascii=False, indent=2)
            last_backup_count = total_radios_found

# Final save
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(all_radios, f, ensure_ascii=False, indent=2)

print(f"\n✅ DONE! Total radios: {len(all_radios)} out of {total_places} places processed.")
print(f"Final file: {OUT}")
print(f"Backup file: {BACKUP_OUT}")