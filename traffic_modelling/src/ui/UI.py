import tkinter as tk
import tkinter.messagebox
from typing import List
import customtkinter as ctk

WIDTH = 1100
HEIGHT = 600
stickiness = "news"

ctk.set_appearance_mode("System") # can be system, light or dark
ctk.set_default_color_theme("blue") # can be blue, green or dark blue

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        FONTS = {
            "header": ctk.CTkFont(size=16, weight="bold"),
            "input": ctk.CTkFont(size=16)
        } # needs to be set up after root is initialised

        # Setting up window parameters
        self.title("Traffic Junction Modelling")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Frame for showing and controlloing main junction
        self.junction_frame = ctk.CTkFrame(self, fg_color="#FF00FF")
        self.junction_frame.grid(row=0, column=0, rowspan=3, sticky=stickiness)
        self.junction_frame.grid_columnconfigure(3, weight=1)
        
        # Frame for showing data collected from current run
        self.current_data_frame = ctk.CTkFrame(self, fg_color="#FF77FF")
        self.current_data_frame.grid(row=3, column=0, rowspan=1, sticky=stickiness)

        # Frame to collect primary input from user
        self.primary_input_frame = ctk.CTkScrollableFrame(self, label_text="Primary Input Parameters", fg_color="#FFFFFF")
        self.primary_input_frame.grid(row=0, column=1, rowspan=2, sticky=stickiness)
        self.primary_input_frame.grid_columnconfigure(1, weight=1)
        primary_labels = ["Northbound Traffic Flow", "a. Exiting North (vph)", "b. Exiting East (vph)", "c. Exiting West (vph)", "Eastbound Traffic Flow", "a. Exiting North (vph)", "b. Exiting East (vph)", "c. Exiting South (vph)",
                        "Southbound Traffic Flow", "a. Exiting East (vph)", "b. Exiting South (vph)", "c. Exiting West (vph)", "Westbound Traffic Flow", "a. Exiting North (vph)", "b. Exiting South (vph)", "c. Exiting West (vph)"]
        self.primary_input_labels: List[ctk.CTkLabel] = []
        self.primary_input_entries: List[ctk.CTkEntry] = []
        self.primary_input_values: List[tk.StringVar] = [tk.StringVar(value=0) for i in range(16)]
        for i in range(16):
            self.primary_input_labels.append(ctk.CTkLabel(self.primary_input_frame, text=primary_labels[i], font=FONTS["input"], text_color="#000000"))
            self.primary_input_labels[i].grid(row=i, column=0, pady=(0, 10))
            self.primary_input_entries.append(ctk.CTkEntry(self.primary_input_frame, placeholder_text="0", width=60, textvariable=self.primary_input_values[i]))
            self.primary_input_entries[i].grid(row=i, column=1)
        
        self.main_button_1 = ctk.CTkButton(master=self.primary_input_frame, fg_color="transparent", border_width=2, text_color="#000000", command=self.button)
        self.main_button_1.grid(row=16, column=0, columnspan=2)

        # Frame to collect configurable parameter input from user
        self.secondary_input_frame = ctk.CTkScrollableFrame(self, fg_color="#0000FF", label_text="Configurable Parameters")
        self.secondary_input_frame.grid(row=0, column=2, rowspan=2, sticky=stickiness)

        # Frame to show graph, as well as save and load parameter buttons
        self.data_graph_frame = ctk.CTkFrame(self,fg_color="#00FFFF")
        self.data_graph_frame.grid(row=2, column=1, rowspan=2, columnspan=2, sticky=stickiness)
    
    def button(self):
        for i in range(16):
            print(self.primary_input_values[i].get())

if __name__ == "__main__":
    app = App()
    app.mainloop()