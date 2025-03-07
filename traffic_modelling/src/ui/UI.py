import tkinter as tk
import customtkinter as ctk

import sys
import os

# add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.TrafficSimulatorPage import TrafficSimulatorUI
from pages.TrafficCollectionPage import TrafficCollectionUI
from pages.DataAnalysisPage import DataAnalysisUI

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

PAGES = {"TrafficSimulatorUI": TrafficSimulatorUI, "TrafficCollectionUI": TrafficCollectionUI, "DataAnalysisUI": DataAnalysisUI}

class TrafficSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Traffic Junction Modelling")
        self.geometry("1300x800")
        self.minsize(900, 600)

        self.container = ctk.CTkFrame(self)  
        self.container.pack(side = "top", fill = "both", expand = True) 
  
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.pages = {}
        for key in PAGES:
            P = PAGES[key]
            page = P(self.container, self)
            self.pages[key] = page
            page.grid(row = 0, column = 0, sticky ="news")

        self.show_page("TrafficSimulatorUI")
    
    def show_page(self, page, params=None):
        try:
            self.pages[page].tkraise()
            if params:
                self.pages["TrafficSimulatorUI"].load_parameters(f"junctions/junction{params['id']}")
        except Exception as e:
            print("Error: ", e)

if __name__ == "__main__":
    app = TrafficSimulatorApp()
    app.mainloop()
