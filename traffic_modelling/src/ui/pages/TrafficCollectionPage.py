import tkinter as tk
import tkinter.messagebox
from typing import List
import customtkinter as ctk

ctk.set_appearance_mode("Light") # can be system, light or dark
ctk.set_default_color_theme("blue") # can be blue, green or dark blue

class TrafficCollectionUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

