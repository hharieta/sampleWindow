import sys
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # create a box
        self.box1 = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)
        self.box2 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.box3 = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)

        # create a button
        self.button = Gtk.Button(label = "I'm a button")
        self.button.connect('clicked', self.hello)

        self.set_child(self.box1) # Horizontal box
        self.box1.append(self.box2) # Put vertical box into horizontal box
        self.box1.append(self.box3) # Other vertical box into horizontal box

        self.box2.append(self.button) # Put button in first vertical box added

        # check button
        self.check = Gtk.CheckButton(label = "Goodbye?")
        self.box2.append(self.check)

        # create swicth box
        self.switch_box = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)

        self.switch = Gtk.Switch()
        self.switch.set_active(True) # default state
        self.switch.connect("state-set", self.switch_switched) # trigger a function

        self.switch_box.append(self.switch)
        self.box2.append(self.switch_box)
        self.label = Gtk.Label(label = "Switch")
        self.switch_box.append(self.label)
        self.switch_box.set_spacing(5)

        # slider
        self.slider = Gtk.Scale()
        self.slider.set_digits(0) # decimal places to use
        self.slider.set_range(0, 10)
        self.slider.set_draw_value(True) # Show label with current value
        self.slider.set_value(5) # Current value position
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)

        # set header bar button
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        self.open_button = Gtk.Button(label = "Open")
        self.header.pack_start(self.open_button)
        self.open_button.set_icon_name("document-open-symbolic")


        # open file dialog
        self.open_dialog = Gtk.FileChooserNative.new(
            title = "Choose a file", parent = self, action = Gtk.FileChooserAction.OPEN)

        self.open_dialog.connect("response", self.open_response)
        self.open_button.connect("clicked", self.show_open_dialog)

        # filter for open dialog
        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/jpeg")
        f.add_mime_type("image/jpg")
        f.add_mime_type("image/png")
        self.open_dialog.add_filter(f)

        # Window parameters
        self.set_default_size(600, 250)
        self.set_title("MyAppd")

    def show_open_dialog(self, button):
        self.open_dialog.show()

    def open_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            filename = file.get_path()
            print(filename)

    def slider_changed(self, slider):
        print(int(slider.get_value()))

    def switch_switched(self, switch, state):
        print(f"The switch has been switched {'on' if state else 'off'}")

    def hello(self, button):
        print("Hello world, I'm a button")

        if self.check.get_active():
            print("Good-Bye wordl")
            self.close()


class MyApp(Adw.Application):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connect('activate', self.on_active)

    def on_active(self, app):
        self.win = MainWindow(application = app)
        self.win.present()


app = MyApp(application_id = "com.example.GtkApplication")
app.run(sys.argv)
