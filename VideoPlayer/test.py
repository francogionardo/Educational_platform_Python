from kivy.app import App
from kivy.uix.video import Video

class TestVideoApp(App):
    def build(self):
        video = Video(source='../Videos\GMT20240823-122814_Recording_1920x1080.mp4')
        video.state = 'play'
        video.options = {'eos': 'loop'}
        return video

if __name__ == '__main__':
    TestVideoApp().run()
