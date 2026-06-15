import subprocess
from typing import Optional


def run_applescript(script: str) -> str:
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    return result.stdout.strip()


def get_now_playing() -> Optional[dict]:
    script = """
    tell application "Music"
        if player state is playing then
            set t to current track
            set pos to player position
            return (name of t) & "|||" & (artist of t) & "|||" & (album of t) & "|||" & (duration of t) & "|||" & pos
        else
            return "NOT_PLAYING"
        end if
    end tell
    """
    output = run_applescript(script)

    if not output or output == "NOT_PLAYING":
        return None

    parts = output.split("|||")
    if len(parts) < 5:
        return None

    try:
        # Fix locale decimal separator (comma vs dot)
        duration_str = parts[3].strip().replace(",", ".")
        position_str = parts[4].strip().replace(",", ".")
        return {
            "title": parts[0].strip(),
            "artist": parts[1].strip(),
            "album": parts[2].strip(),
            "duration": float(duration_str),
            "position": float(position_str),
        }
    except (ValueError, IndexError):
        return None


def is_music_running() -> bool:
    script = 'tell application "System Events" to (name of processes) contains "Music"'
    result = run_applescript(script).lower()
    return result in ("true", "1")
