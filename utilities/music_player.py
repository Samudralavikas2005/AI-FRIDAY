# utilities/music_player.py
import webbrowser
import music_library

class MusicPlayer:
    def __init__(self):
        self.music_library = music_library.music
    
    def play_playlist(self):
        link = self.music_library.get("playlist")
        if link:
            webbrowser.open(link)
            return "Playing your entire playlist."
        return "Playlist link not found."
    
    def play_song(self, song_name):
        if song_name in self.music_library:
            link = self.music_library[song_name]
            webbrowser.open(link)
            return f"Playing {song_name} from your playlist."
        return "Sorry, that song is not in your playlist."
    
    def extract_song_name(self, text):
        if text.startswith("play "):
            return text.replace("play", "", 1).strip()
        return None
