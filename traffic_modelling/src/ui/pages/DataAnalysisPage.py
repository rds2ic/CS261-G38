import tkinter as tk
import customtkinter as ctk
import matplotlib.pyplot as plt #pip3 install matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# text size of labels on graphs
plt.rcParams.update({
    'font.size': 4,          # normal text size
    'axes.titlesize': 5,    # title size
    'axes.labelsize': 4,     # axis label size
    'xtick.labelsize': 3.5,    # x-axis tick label size
    'ytick.labelsize': 3.5,    # y-axis tick label size
    'legend.fontsize': 4     # legend font size
})

class DataAnalysisUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        # font styles
        self.header_font = ctk.CTkFont(size=16, weight="bold")
        self.subheader_font = ctk.CTkFont(size=14, weight="bold")
        self.normal_font = ctk.CTkFont(size=13)
        self.small_font = ctk.CTkFont(size=11)
        self.text_color = "black"

        # create toolbar
        self._build_top_toolbar()

        # create graph container
        self._build_graph_section()


    # TOOLBAR

    def _build_top_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="#EEEEEE")
        toolbar.pack(side="top", fill="x")

        for col in range(8):
            toolbar.grid_columnconfigure(col, weight=0)
        toolbar.grid_columnconfigure(1, weight=1)
        toolbar.grid_columnconfigure(7, weight=1)

        back_button = ctk.CTkButton(
            toolbar, text="← Back to Traffic Collection",
            text_color="white",
            command=self.back_to_traffic_collection
        )
        back_button.grid(row=0, column=0, padx=(10, 10), pady=5, sticky="w")


    # MAIN GRAPH PANE

    def _build_graph_section(self):
        container = ctk.CTkFrame(self, fg_color="#FFFFFF")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # title of the page
        title_label = ctk.CTkLabel(container, text="Data Analysis", font=self.header_font, text_color=self.text_color)
        title_label.pack(pady=5)

        # frame to place the graphs
        graph_frame = ctk.CTkFrame(container, fg_color="#FFFFFF")
        graph_frame.pack(fill="both", expand=True)

        self._create_graphs(graph_frame)

    def _create_graphs(self, parent):
        criteria_labels = [
            ("Average Wait Time", "Avg. Wait Time [s]"),
            ("Maximum Wait Time", "Max Wait Time [s]"),
            ("Maximum Queue Length", "Max Queue Length [cars]")
        ]
        directions = ["North", "East", "South", "West"]

        # different colours for each junction #
        junctions = np.array([1, 2, 3, 4, 5, 6])
        colors = ["#FF0000", "#FFD700", "#00CC00", "#b5e2ff", "#A020F0", "#FFC0CB"]

        # subplots
        fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(12, 8))
        fig.subplots_adjust(hspace=0.5, wspace=0.3)

        # spacing between graphs
        fig.subplots_adjust(hspace=0.9, wspace=0.8)

        for row, (criteria, ylabel) in enumerate(criteria_labels):
            for col, direction in enumerate(directions):
                ax = axes[row, col]

                # the current data is random, so pls edit here later to display the actual data collected from the simulation
                data = np.random.randint(10, 50, size=len(junctions))

                ax.bar(junctions, data, color=colors)
                ax.set_title(f"{criteria}\n{direction}")
                ax.set_xticks(junctions)
                ax.set_xlabel("Junction #")
                ax.set_ylabel(ylabel) 

        # embed matplotlib figures in tkinter
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        canvas.draw()


    # buttons (for page transfer)

    def back_to_traffic_collection(self):
        self.controller.show_page("TrafficCollectionUI")
        print("Clicked Back to Traffic Collection")


if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Traffic Junction Modelling")
    app.geometry("1300x800")
    app.minsize(900, 600)

    container = ctk.CTkFrame(app)  
    container.pack(side="top", fill="both", expand=True)

    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    page = DataAnalysisUI(container, app)
    page.grid(row=0, column=0, sticky="news")

    app.mainloop()
