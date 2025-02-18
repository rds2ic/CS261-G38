import tkinter as tk
import customtkinter as ctk
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

        container = ctk.CTkFrame(self)  
        container.pack(side = "top", fill = "both", expand = True) 
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.pages = {}
        for key in PAGES:
            P = PAGES[key]
            page = P(container, self)
            self.pages[key] = page
            page.grid(row = 0, column = 0, sticky ="news")

        self.show_page("TrafficSimulatorUI")
    
    def show_page(self, page):
        self.pages[page].tkraise()

if __name__ == "__main__":
    app = TrafficSimulatorApp()
    app.mainloop()
