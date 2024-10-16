# MediaController.py

import vlc

class MediaController:
    def __init__(self, video_path):
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        media = self.instance.media_new(video_path)
        self.media_player.set_media(media)

    def play(self):
        if not self.media_player.is_playing():
            self.media_player.play()

    def pause(self):
        if self.media_player.is_playing():
            self.media_player.pause()

    def toggle_play_pause(self):
        if self.media_player.is_playing():
            self.pause()
        else:
            self.play()

    def stop(self):
        self.media_player.stop()

    def set_hwnd(self, hwnd):
        self.media_player.set_hwnd(hwnd)
