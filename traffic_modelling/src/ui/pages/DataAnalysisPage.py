import tkinter as tk
import customtkinter as ctk
import pickle

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class DataAnalysisUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        # font size and colours
        self.header_font = ctk.CTkFont(size=16, weight="bold")
        self.subheader_font = ctk.CTkFont(size=14, weight="bold")
        self.normal_font = ctk.CTkFont(size=13)
        self.small_font = ctk.CTkFont(size=11)
        self.text_color = "black"

# For testing purposes
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Traffic Junction Modelling")
    app.geometry("1300x800")
    app.minsize(900, 600)

    container = ctk.CTkFrame(app)  
    container.pack(side = "top", fill = "both", expand = True) 

    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)
    page = DataAnalysisUI(container, app)
    page.grid(row = 0, column = 0, sticky ="news")
    app.mainloop()