import rumps
import threading
import logging
from tracker import MusicTracker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)


class MusicPresenceApp(rumps.App):
    def __init__(self):
        super().__init__(
            name="MusicPresence",
            icon="icon.png",
            template=True,
            quit_button=None
        )

        self.tracker = MusicTracker(on_update=self.on_track_update)
        self.title = ""

        self.status_item = rumps.MenuItem("Not playing", callback=None)
        self.toggle_item = rumps.MenuItem("Pause", callback=self.toggle_rpc)
        self.quit_item = rumps.MenuItem("Quit", callback=self.quit_app)

        self.menu = [
            self.status_item,
            None,
            self.toggle_item,
            None,
            self.quit_item,
        ]

        self._paused = False

    def on_track_update(self, track_info):
        self._pending_update = track_info

    @rumps.timer(1)
    def check_update(self, _):
        if not hasattr(self, '_pending_update'):
            return
        data = self._pending_update
        if isinstance(data, dict):
            title = data.get("title", "")
            artist = data.get("artist", "")
            self.status_item.title = f"{title} — {artist}"
        elif data is None:
            self.status_item.title = "Not playing"

    def _update_ui(self, track_info):
        try:
            if track_info:
                title = track_info.get("title", "")
                artist = track_info.get("artist", "")
                self.status_item.title = f"{title} — {artist}"
            else:
                self.status_item.title = "Not playing"
        except Exception:
            pass

    def toggle_rpc(self, sender):
        self._paused = not self._paused
        if self._paused:
            self.toggle_item.title = "Resume"
            self.tracker.pause()
        else:
            self.toggle_item.title = "Pause"
            self.tracker.resume()

    def quit_app(self, sender):
        self.tracker.stop()
        rumps.quit_application()


if __name__ == "__main__":
    app = MusicPresenceApp()
    t = threading.Thread(target=app.tracker.run, daemon=True)
    t.start()
    app.run()
