TRANSLATIONS = {
    "en": {
        "inquiry_title": "Inquiry Summary",
    },
    "th": {
        "inquiry_title": "สรุปคำถาม",
    }
}

CURRENT_LANG = "th"

def translate(key):
    return TRANSLATIONS.get(CURRENT_LANG, {}).get(key, key)