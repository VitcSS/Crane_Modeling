import tkinter
import tkinter.messagebox
import customtkinter
from libs.object import object
from libs.Crane import Crane
# from libs.Crane import Crane
# from libs.object import object

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class GUI(customtkinter.CTk):
    WIDTH = 350
    HEIGHT = 300
    def __init__(self):
        super().__init__()
        self.title("Crane GUI")
        self.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # Comunication Channel to CoppeliaSim
        self.Model = Crane()

        self.angle_slider = customtkinter.CTkSlider(master=self,
                                 width=160,
                                 height=16,
                                 border_width=5.5,
                                 from_ = -180,
                                 to= 180,
                                 command=self.angle_update)

        self.height_slider = customtkinter.CTkSlider(master=self,
                                        width=160,
                                        height=16,
                                        border_width=5.5,
                                        from_ = 0,
                                        to= -0.25,
                                        command=self.height_update)

        self.tool_slider = customtkinter.CTkSlider(master=self,
                                        width=160,
                                        height=16,
                                        border_width=5.5,
                                        from_ = 0,
                                        to= 0.25,
                                        command=self.tool_update)
        # Magnet :
        self.Magnet_B =customtkinter.CTkButton(master = self,
                                            text  = 'OFF',
                                            command = self.catching)
        #Title Labels :
        self.Angle_T = customtkinter.CTkLabel(master = self,
                                            text = "Angle")
        self.Height_T = customtkinter.CTkLabel(master = self,
                                            text = "Height")
        self.Tool_T = customtkinter.CTkLabel(master = self,
                                            text = "Tool")
        self.Magnet_T = customtkinter.CTkLabel(master = self,
                                            text = "Magnet")

        # Value Labels :
        self.Angle_V = customtkinter.CTkLabel(master = self,
                                            text = 0)
        self.Height_V = customtkinter.CTkLabel(master = self,
                                            text = 0)
        self.Tool_V = customtkinter.CTkLabel(master = self,
                                            text = 0)
        self.Dist = customtkinter.CTkLabel(master = self,
                                        text = "Distance : Unknown")
    


        # Position of inputs :
        self.angle_slider.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)
        self.height_slider.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
        self.tool_slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.Magnet_B.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
    
        # Title Label positions :
        self.Angle_T.place(relx=0.25, rely=0.3, anchor=tkinter.E)
        self.Height_T.place(relx=0.25, rely=0.4, anchor=tkinter.E)
        self.Tool_T.place(relx=0.25, rely=0.5, anchor=tkinter.E)
        self.Magnet_T.place(relx = 0.5, rely = 0.7, anchor=tkinter.CENTER)
        self.Dist.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        # Title Label positions :
        self.Angle_V.place(relx=0.75, rely=0.3, anchor=tkinter.W)
        self.Height_V.place(relx=0.75, rely=0.4, anchor=tkinter.W)
        self.Tool_V.place(relx=0.75, rely=0.5, anchor=tkinter.W)


    def angle_update(self, value):
        self.Model.XY.setPosition(value)
        value = str(value)
        self.Angle_V.configure(text = value)

        reading = self.Model.Distance.detect()
        if type(reading) == tuple:
            self.Dist.configure(text = 'Distance : '+str(reading[0]))
        else :
            self.Dist.configure(text = 'Distance : Unknown')
    
    def height_update(self, value):
        self.Model.Z.setPosition(value)
        value = str(value)
        self.Height_V.configure(text = value)

        reading = self.Model.Distance.detect()
        if type(reading) == tuple:
            self.Dist.configure(text = 'Distance : '+str(reading[0]))
        else :
            self.Dist.configure(text = 'Distance : Unknown')

    def tool_update(self, value):
        self.Model.Tool.setPosition(value)
        value = str(value)
        self.Tool_V.configure(text = value)

        reading = self.Model.Distance.detect()
        if type(reading) == tuple:
            self.Dist.configure(text = 'Distance : '+str(reading[0]))
        else :
            self.Dist.configure(text = 'Distance : Unknown')
    
    def catching(self):
        if self.Model.Actuator.has_something() == True:
            self.Model.Actuator.off()
            self.Magnet_B.configure(text = 'OFF')
        else :
            self.Model.Actuator.on()
            self.Magnet_B.configure(text = 'ON')
            if self.Model.Actuator.has_something() == False:
                self.Magnet_B.configure(text = 'OFF')


    def on_closing(self, event=0):
        object.sim.stopSimulation()
        self.destroy()
        exit(0)

    def start(self):
        object.sim.startSimulation()
        self.mainloop()
    
App = GUI()
GUI().start()