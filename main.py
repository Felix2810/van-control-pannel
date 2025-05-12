import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.graphics import Color, Line

# Set fixed window size
Window.size = (1024, 600)

# Main screen
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        background = Image(source='logo.png', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        layout.add_widget(background)

        num_buttons = len(config["labels"])
        left_count = num_buttons // 2
        right_count = num_buttons - left_count
        spacing = 1 / (max(left_count, right_count) + 1)

        for i, (label, icon) in enumerate(zip(config["labels"], config["icons"])):
            button = IconLabelButton(icon, label)
            y_pos = 1 - ((i // 2 + 1) * spacing)
            if i % 2 == 0:
                button.pos_hint = {'x': 0.1, 'top': y_pos}
            else:
                button.pos_hint = {'right': 0.9, 'top': y_pos}
            layout.add_widget(button)

        # Settings button at bottom center
        settings_btn = IconButton(pos_hint={'center_x': 0.5, 'y': 0.02})
        settings_btn.bind(on_release=self.goto_settings)
        layout.add_widget(settings_btn)

        self.add_widget(layout)

    def goto_settings(self, *args):
        self.manager.current = 'settings'

# Default config (used instead of config.json)
config = {
    "labels": ["Lights", "Exterior Lights", "Water Pump", "Fridge", "Heater", "Fan", "Inverter", "USB Ports"],
    "icons": [
        "Icons/light.png",
        "Icons/outside_lights.png",
        "Icons/Water_Pump.png",
        "Icons/fridge.png",
        "Icons/Heater.png",
        "Icons/fan.png",
        "Icons/Inverter.png",
        "Icons/USB.png"
    ]
}

# Custom toggle button with icon, label and border color change
class IconLabelButton(ButtonBehavior, BoxLayout):
    def __init__(self, icon_path, label_text, **kwargs):
        super().__init__(orientation='vertical', size_hint=(None, None), size=(200, 120), spacing=5, **kwargs)
        
        self.is_on = False  # Custom state to toggle border

        self.icon = Image(source=icon_path, size_hint=(1, 0.7))
        self.label = Label(
            text=label_text,
            size_hint=(1, 0.3),
            color=(71/255, 157/255, 177/255, 1),
            font_size=30
        )

        self.add_widget(self.icon)
        self.add_widget(self.label)

        with self.canvas.before:
            self.border_color = Color(80/255,116/255,140/255,1)  # Smalt Blue
            self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=2)

        self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        self.border.rectangle = (self.x, self.y, self.width, self.height)

    def on_press(self):
        self.is_on = not self.is_on  # Toggle state
        if self.is_on:
            self.border_color.rgba = (0, 1, 0, 0.3)  # Green border when ON
        else:
            self.border_color.rgba = (80/255,116/255,140/255,1)  # Smalt Blue border when OFF

# Clickable settings button
class IconButton(ButtonBehavior, BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='horizontal', spacing=10, size_hint=(None, None), size=(180, 50), **kwargs)
        self.icon = Image(source='Icons/cogs.png', size_hint=(None, None), size=(40, 40))
        self.label = Label(
            text="Settings",
            color=(71/255, 157/255, 177/255, 1),
            font_size=20,
            halign='left',
            valign='middle'
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.icon)
        self.add_widget(self.label)



# Placeholder settings screen
class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text="Settings Screen - Under Construction", font_size=24))
        back_btn = Button(text="Back", size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5})
        back_btn.bind(on_release=self.go_back)
        layout.add_widget(back_btn)
        self.add_widget(layout)

    def go_back(self, *args):
        self.manager.current = 'main'

# App entry
class VanControlPanelApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    VanControlPanelApp().run()
