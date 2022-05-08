import tkinter
import tkinter.messagebox
import customtkinter
from libs.Crane import Crane
from libs.object import object

Model = Crane()
object.sim.startSimulation()

root_tk = tkinter.Tk()  # create the Tk window like you normally do
angle_slider = customtkinter.CTkSlider(master=root_tk,
                                 width=160,
                                 height=16,
                                 border_width=5.5,
                                 from_ = 0,
                                 to= 360,
                                 command=Model.XY.setPosition)

height_slider = customtkinter.CTkSlider(master=root_tk,
                                 width=160,
                                 height=16,
                                 border_width=5.5,
                                 from_ = 0,
                                 to= -0.25,
                                 command=Model.Z.setPosition)

tool_slider = customtkinter.CTkSlider(master=root_tk,
                                 width=160,
                                 height=16,
                                 border_width=5.5,
                                 from_ = 0,
                                 to= 0.25,
                                 command=Model.Tool.setPosition)

magnet_button = customtkinter.CTkButton(master=root_tk, 
                                corner_radius=10,
                                text= 'Magnet'
                                )

angle_slider.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
height_slider.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
tool_slider.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)
magnet_button.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)
root_tk.mainloop()