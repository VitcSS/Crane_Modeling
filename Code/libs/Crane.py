from libs.object import *
import tkinter
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Crane :
    def __init__(self,
                 XY : str = '/Spear_Joint', 
                 Z : str = '/Actuator_Joint', 
                 Tool : str = '/Tool_Joint', 
                 Actuator : str = '/Magnet', 
                 Distance : str = '/Distance'):
        self.XY = Revolute(XY,18)
        self.Z = Prismatic(Z,0.06)
        self.Tool = Prismatic(Tool,0.06)
        self.Actuator = Magnet(Actuator)
        self.Distance = Ray_Sensor(Distance)

