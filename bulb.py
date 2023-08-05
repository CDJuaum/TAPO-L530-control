import customtkinter as ctk
from CTkColorPicker import *
import colorsys
from PyP100 import PyL530

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def setBrightness(self, value):
        print(value)
        self.l530.setBrightness(value)

    def ask_color(self):
        pick_color = AskColor()
        hex = pick_color.get() 
        hex = hex.lstrip("#")
        rgb = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
        hsl = colorsys.rgb_to_hls(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
        self.hue = hsl[0] * 360
        self.saturation = hsl[2] * 100
        self.lightness = hsl[1] * 100
        print(self.hue, self.saturation, self.lightness)

    def select(self):
        check = int(self.radiobutton_var.get())
        if check == 1:
            self.l530.setColorTemp(self.scale.get())
        if check == 2:
            self.ask_color()
            self.l530.setColor(self.hue, self.saturation)

    def __init__(self):
        super().__init__()

        self.l530 = PyL530.L530("your device's IP", "your email", "your password") # your TAPO's credentials and bulb's IP
        self.l530.handshake()
        self.l530.login() 

        self.title("Bedroom Light")
        self.geometry("700x400")
        font1 = ctk.CTkFont(size=20)
        font2 = ctk.CTkFont(size=15)

        button_1 = ctk.CTkButton(self, text="Turn on", width=150, height=100, font=font1, command=lambda:self.l530.turnOn())
        button_1.place(anchor="center", x=250, y=100)
        button_2 = ctk.CTkButton(self, text="Turn off", width=150, height=100, font=font1, command=lambda:self.l530.turnOff())
        button_2.place(anchor="center", x=450, y=100)

        self.radiobutton_var = ctk.IntVar()

        radiobutton_1 = ctk.CTkRadioButton(self, variable=self.radiobutton_var, value=1, text="light")
        radiobutton_1.place(x=250, y=170)

        radiobutton_2 = ctk.CTkRadioButton(self, variable=self.radiobutton_var, value=2, text="color")
        radiobutton_2.place(x=400,y=170)

        button_3 = ctk.CTkButton(self, text="set color/temp", width=150, height=40, font=font2, command=lambda:self.select())
        button_3.place(anchor="center", x=350, y=230)

        self.scale = ctk.IntVar(value = 3750)
        self.bright = ctk.IntVar(value = 50)

        self.slider_1 = ctk.CTkSlider(self, from_=2500, to=5000, number_of_steps=1000, variable= self.scale, command=lambda value: print(value)) #replace w function, no print
        self.slider_1.place(anchor="center", x=350, y=275)
        self.brightness = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, variable= self.bright, command=self.setBrightness)
        self.brightness.place(anchor="center", x=350, y=315)
        
    

if __name__ == "__main__":
    app = App()
    app.mainloop()