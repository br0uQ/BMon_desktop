from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.audio import SoundLoader
from kivy.core.audio.audio_gstplayer import SoundGstplayer
from kivy.core.window import Window
from mjpegviewer import MjpegViewer
from kivy.clock import Clock
from kivy.uix.widget import Widget
import os


class ConnectPage(Widget):
    def __init__(self, bmon_app, **kwargs):
        super().__init__(**kwargs)
        self.bmon_app = bmon_app
        self.cols = 1

        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
        else:
            prev_ip = ""

        self.add_widget(Label(text="IP:"))

        self.txtin_ip = TextInput(text=prev_ip, multiline=False)
        self.add_widget(self.txtin_ip)

        self.btn_connect = Button(text="Connect")
        self.btn_connect.bind(on_press=self.connect_button)
        self.add_widget(Label())
        self.add_widget(self.btn_connect)

    def connect_button(self, instance):
        ip = self.txtin_ip.text

        with open("prev_details.txt", "w") as f:
            f.write(f"{ip}")

        info = f"Attempting to connect to {ip}"
        self.bmon_app.info_page.update_info(info)
        self.bmon_app.screen_manager.current = "Info"
        Clock.schedule_once(self.connect, 1)

    def connect(self, _):
        ip = self.txtin_ip.text

        """ 
        # Connect to Video and Audiostream
        if not socket_client.connect(ip, port, username, show_error):
            return
        """
        # Show Monitor page with options to show video stream
        self.bmon_app.create_monitor_page()
        self.bmon_app.screen_manager.current = "Monitor"


class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.lbl_message = Label(halign="center", valign="middle", font_size=30)
        self.lbl_message.bind(width=self.update_text_width)
        self.add_widget(self.lbl_message)

    def update_info(self, message):
        self.lbl_message.text = message

    def update_text_width(self, *_):
        self.lbl_message.text_size = (self.lbl_message.width * 0.9, None)


class MonitorPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        self.videoViewer = MjpegViewer(url="http://192.168.2.1:8090/", size_hint_y=None)
        self.videoViewer.bind(height=self.update_video_size)
        #videoViewer.start()
        videoLayout = AnchorLayout(anchor_x="center")
        videoLayout.add_widget(self.videoViewer)
        self.add_widget(videoLayout)
        buttons = GridLayout(height=Window.size[1]*0.1, size_hint_y=None)
        buttons.cols = 2
        self.btn_video = Button(text="Video: off")
        self.btn_video.bind(on_press=self.switch_video)
        buttons.add_widget(self.btn_video)

        self.btn_audio = Button(text="Audio: off")
        self.btn_audio.bind(on_press=self.switch_audio)
        buttons.add_widget(self.btn_audio)
        self.add_widget(buttons)
        #sound = SoundLoader.load("http://192.168.2.1:8000/raspi.mp3")
        #sound.load()
        #if sound:
        #    print("Sound found at %s" % sound.source)
        #    print("Sound is %.3f seconds" % sound.length)
        #    sound.play()

    def switch_video(self, _):
        if self.btn_video.text == "Video: off":
            self.videoViewer.start()
            self.btn_video.text = "Video: on"
        else:
            self.videoViewer.stop()
            self.btn_video.text = "Video: off"

    def switch_audio(self, _):
        if self.btn_audio.text == "Audio: off":

            self.btn_audio.text = "Audio: on"
        else:

            self.btn_audio.text = "Audio: off"

    def update_video_size(self, *_):
        self.videoViewer.height = Window.size[1] * 0.9