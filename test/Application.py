from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from networkx.algorithms.distance_measures import radius
from kivy.metrics import dp

# For Small Mobile Phones
Window.size = (360, 640)

# For Medium Sized Mobile Phones
# Window.size = (411, 731)

# For Large Sized Mobile Phones
# Window.size = (480, 854)

# For Tablets
# Window.size = (600, 960)

Window.clearcolor = (0, 0.12, 0.2, 1)

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.f_size = self.width * 0.025
        self.b_size = (None, None)
        self.p_both = (self.width * 0.03, self.width * 0.03)
        self.sp = None

        # self.make_responsive()

        self.top_bar = BoxLayout(orientation = 'horizontal', size_hint = (1, 0.15), padding = self.p_both, spacing = self.width * 0.02)

        heading = Label(
            text = "AI Powered Smart Vision",
            font_size = Window.width * 0.025,
            font_name = "fonts/LEMONMILK-Medium.otf",
            halign = 'left',
            valign = 'middle',
            color = (1, 1, 1, 1)
        )
        heading.bind(size = heading.setter('text_size'))

        logo = Image(
            source = "data/images/vr-glasses.png",
            size_hint = (0.2, 1)
        )

        # settings_button = Button(
        #     background_normal = "data/images/setting.png",
        #     background_down="data/images/setting.png",
        #     size_hint = (0.2, 0.4)
        # )

        self.top_bar.add_widget(heading)
        self.top_bar.add_widget(logo)
        # top_bar.add_widget(settings_button)

        self.start_button = Button(
            # background_normal = "data/images/start.png",
            # background_down = "data/images/stop.png",
            text = "Start",
            size_hint = (0.2, 0.15),
            font_name = "fonts/LEMONMILK-Bold.otf",
            pos_hint = {"center_x" : 0.5},
            background_normal = "",
            # background_color = (0.33, 0.35, 0.42, 1),
            background_color = (0, 0, 0, 0),
            color = (1, 1, 1, 1)
        )

        with self.start_button.canvas.before:
            self.start_button.bg_color = Color(0.33, 0.35, 0.42, 1)
            self.start_button.bg_rect = RoundedRectangle(pos = self.start_button.pos, size = self.start_button.size, radius = [dp(50)])

        self.start_button.bind(pos = self.update_start_btn, size = self.update_start_btn)

        # Update position/size when button resizes or moves

        # start_button.bind(on_press = MainLayout.on_button_press)
        # start_button.bind(on_release = MainLayout.on_button_release)

        self.add_widget(self.top_bar)
        self.add_widget(Widget())
        self.add_widget(self.start_button)
        self.add_widget(Widget())

    def update_start_btn(self, *args):
        self.start_button.bg_rect.pos = self.start_button.pos
        self.start_button.bg_rect.size = self.start_button.size


    @staticmethod
    def on_button_press(instance):
        print("Function is Called")
        instance.background_normal = "data/images/stop.png"

    @staticmethod
    def on_button_release(instance):
        print("Function is Called")
        instance.background_normal = "data/images/start.png"

    def make_responsive(self):

        width = Window.width

        if width <= 360:
            pass


class MyApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    Obj = MyApp()
    Obj.run()
