from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_gstplayer import SoundGstplayer
from kivy.core.window import Window
from mjpegviewer import MjpegViewer
from kivy.clock import Clock
import os


class MonitorElement(GridLayout):
    def __init__(self, name, fct_connect, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.cols = 3
        self.add_widget(Label(text=name))

        self.btn_connect = Button(text="Connect")
        self.btn_connect.size_hint_x = 0.4
        self.btn_connect.bind(on_release=fct_connect)
        self.add_widget(self.btn_connect)

        self.btn_delete = Button(text="Delete")
        self.btn_delete.size_hint_x = 0.2
        self.btn_delete.bind(on_release=self.delete)
        self.add_widget(self.btn_delete)

    def delete(self, instance):
        self.parent.remove_widget(self)


class ConnectPage(GridLayout):
    def __init__(self, bmon_app, **kwargs):
        super().__init__(**kwargs)
        self.bmon_app = bmon_app

        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(",")
                #prev_ip = d[0]
                for element in d:
                    self.ids["elements"].add_widget(MonitorElement(name=element, fct_connect=self.connect_button))

    def connect_button(self, instance):
        #with open("prev_details.txt", "w") as f:
        #    f.write(f"{ip}")

        info = f"Attempting to connect"
        self.bmon_app.info_page.update_info(info)
        self.bmon_app.screen_manager.current = "Info"
        Clock.schedule_once(self.connect, 1)

    def connect(self, _):
        """
        # Connect to Video and Audiostream
        if not socket_client.connect(ip, port, username, show_error):
            return
        """
        # Show Monitor page with options to show video stream
        self.bmon_app.create_monitor_page()
        self.bmon_app.screen_manager.current = "Monitor"

    def new_element(self):
        #self.ids["elements"].add_widget(MonitorElement(name="first"))
        s = 1


class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lbl_message = self.ids["lbl_message"]
        self.lbl_message.bind(width=self.update_text_width)

    def update_info(self, message):
        self.lbl_message.text = message

    def update_text_width(self, *_):
        self.lbl_message.text_size = (self.lbl_message.width * 0.9, None)


class MonitorPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.btn_video = self.ids["btn_video"]
        self.btn_audio = self.ids["btn_audio"]
        self.video_layout = self.ids["video_layout"]
        self.slider_volume = self.ids["slider_volume"]

        if os.path.isfile("prev_volume.txt"):
            with open("prev_volume.txt", "r") as f:
                self.volume = float(f.read())
                self.slider_volume.value = self.volume
        else:
            self.volume = self.slider_volume.value

    def switch_video(self):
        if self.btn_video.text == "Video: off":
            self.videoViewer = MjpegViewer(url="http://192.168.2.1:8090/")
            self.videoViewer.bind(height=self.update_video_size)
            self.video_layout.add_widget(self.videoViewer)
            self.videoViewer.start()
            self.btn_video.text = "Video: on"
        else:
            self.videoViewer.stop()
            self.video_layout.remove_widget(self.videoViewer)
            self.btn_video.text = "Video: off"

    def switch_audio(self):
        if self.btn_audio.text == "Audio: off":
            self.sound = SoundLoader.load("http://192.168.2.1:8000/raspi.mp3")
            self.sound.load()
            if self.sound:
                print("Sound found at %s" % self.sound.source)
                print("Sound is %.3f seconds" % self.sound.length)
                self.sound.volume = self.volume / 10.0
                self.sound.play()

            self.btn_audio.text = "Audio: on"
        else:
            self.sound.stop()
            self.sound.unload()
            self.btn_audio.text = "Audio: off"

    def update_video_size(self, *_):
        self.videoViewer.height = Window.size[1] * 0.9

    def change_volume(self, *_):
        self.volume = self.slider_volume.value

        with open("prev_volume.txt", "w") as f:
            f.write(f"{self.volume}")

        if self.btn_audio.text == "Audio: on":
            self.sound.volume = self.volume / 10.0