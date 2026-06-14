import requests
import re
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

LRCLIB_BASE = "https://lrclib.net/api"

# Cache manual yang tidak simpan hasil None
_lyrics_cache = {}


def _clean_title(title: str) -> str:
    cleaned = re.sub(r'\s*\(([^)]+)\)', r' - \1', title).strip()
    return cleaned


def fetch_lyrics(title: str, artist: str, album: str = "", duration: float = 0) -> Optional[List[dict]]:
    cache_key = f"{title}||{artist}"
    if cache_key in _lyrics_cache:
        return _lyrics_cache[cache_key]

    result = _fetch_lyrics_raw(title, artist, album, duration)

    # Hanya cache kalau ada hasilnya
    if result is not None:
        _lyrics_cache[cache_key] = result

    return result


def _fetch_lyrics_raw(title: str, artist: str, album: str = "", duration: float = 0) -> Optional[List[dict]]:
    clean_title = _clean_title(title)
    params = {"track_name": clean_title, "artist_name": artist}

    try:
        resp = requests.get(f"{LRCLIB_BASE}/get", params=params, timeout=10)
        logger.info(f"_fetch_lyrics_raw: status={resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            logger.info(f"_fetch_lyrics_raw: hasSynced={bool(data.get('syncedLyrics'))}, hasPlain={bool(data.get('plainLyrics'))}, code={data.get('code')}")
            if data.get("syncedLyrics"):
                return parse_lrc(data["syncedLyrics"])
            elif data.get("plainLyrics"):
                return parse_plain(data["plainLyrics"])
        return _fallback_search(clean_title, artist)
    except Exception as e:
        logger.info(f"_fetch_lyrics_raw exception: {e}")
        return None


def _fallback_search(title: str, artist: str) -> Optional[List[dict]]:
    try:
        resp = requests.get(
            f"{LRCLIB_BASE}/search",
            params={"q": f"{title} {artist}"},
            timeout=10
        )
        if resp.status_code == 200:
            for item in resp.json():
                if item.get("syncedLyrics"):
                    return parse_lrc(item["syncedLyrics"])
                elif item.get("plainLyrics"):
                    return parse_plain(item["plainLyrics"])
    except requests.RequestException:
        pass
    return None


def parse_lrc(lrc_text: str) -> Optional[List[dict]]:
    lines = []
    pattern = re.compile(r"\[(\d{2}):(\d{2})\.(\d{2,3})\](.*)")
    for line in lrc_text.splitlines():
        match = pattern.match(line.strip())
        if match:
            t = int(match.group(1)) * 60 + int(match.group(2)) + int(match.group(3)) / 100
            lines.append({"time": t, "text": match.group(4).strip()})
    return lines or None


def parse_plain(plain_text: str) -> List[dict]:
    lines = [l.strip() for l in plain_text.splitlines() if l.strip()]
    return [{"time": i * 5.0, "text": line} for i, line in enumerate(lines)]


def get_current_line(lyrics: List[dict], position: float) -> str:
    current = ""
    for entry in lyrics:
        if entry["time"] <= position:
            current = entry["text"]
        else:
            break
    return current or "♪"