import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from bmonview import ConnectPage, InfoPage, MonitorPage
import sys
kivy.require("1.11.1")


class BmonApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        self.connect_page = ConnectPage(self)
        screen = Screen(name="Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        self.info_page = InfoPage()
        screen = Screen(name="Info")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def create_monitor_page(self):
        self.monitor_page = MonitorPage()
        screen = Screen(name="Monitor")
        screen.add_widget(self.monitor_page)
        self.screen_manager.add_widget(screen)


def show_error(message):
    bmon_app.info_page.update_info(message)
    bmon_app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 10)


if __name__ == "__main__":
    bmon_app = BmonApp()
    bmon_app.run()
