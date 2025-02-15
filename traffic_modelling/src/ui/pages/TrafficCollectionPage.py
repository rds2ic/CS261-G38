import tkinter as tk
import tkinter.messagebox
from typing import List
import customtkinter as ctk
from PIL import Image # pip install pillow

ctk.set_appearance_mode("Light") # can be system, light or dark
ctk.set_default_color_theme("blue") # can be blue, green or dark blue

class TrafficCollectionUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.controller = controller

        # font size and colours
        self.header_font = ctk.CTkFont(size=16, weight="bold")
        self.subheader_font = ctk.CTkFont(size=14, weight="bold")
        self.normal_font = ctk.CTkFont(size=13)
        self.small_font = ctk.CTkFont(size=11)
        self.text_color = "black"

        # Build the layout
        self._build_toolbar()
        self._build_junction_scroll_area()
        self._build_compare_button()
    
    # Helper function to make widgets a button
    def make_widget_button(self, widget, id):
        widget.bind("<Button-1>", lambda e: self.junction_pressed(id))
        widget.configure(cursor="hand2")

    def _build_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="#EEEEEE")
        toolbar.pack(side="top", fill="x", pady=(0, 10))

        # Configure grid for tool bar
        for col in range(6):
            toolbar.grid_columnconfigure(col, weight=0)
        toolbar.grid_columnconfigure(1, weight=1)
        toolbar.grid_columnconfigure(3, weight=1)
        toolbar.grid_columnconfigure(5, weight=1)

        # Title
        title = ctk.CTkLabel(
            toolbar,
            text="Traffic Collection",
            font=self.header_font,
            text_color=self.text_color
        )
        title.grid(row=0, column=0, padx=10, pady=5)

        # Priority Label
        priority_label = ctk.CTkLabel(
            toolbar,
            text="Output priority ratio\nfor calculating overall score:",
            font=self.normal_font,
            text_color=self.text_color
        )
        priority_label.grid(row=0, column=2, padx=10, pady=5)

        # Slider Frame
        slider_frame = ctk.CTkFrame(toolbar, fg_color="#EEEEEE")
        slider_frame.grid(row=0, column=3, sticky="ew", padx=10)

        left_label = ctk.CTkLabel(
            slider_frame,
            text="Prioritise Shorter\nWait Time",
            font=self.small_font,
            text_color="#0096FF"
        )
        left_label.pack(side="left", padx=(0, 10))

        self.slider_val = tk.IntVar(value=5)

        self.priority_slider = ctk.CTkSlider(
            slider_frame,
            from_=0,
            to=10,
            number_of_steps=10,
            variable=self.slider_val,
            width=400
        )
        self.priority_slider.set(5)
        self.priority_slider.pack(side="left", padx=10, pady=5)

        right_label = ctk.CTkLabel(
            slider_frame,
            text="Prioritise Shorter\nQueue Length",
            font=self.small_font,
            text_color="#FF0000"
        )
        right_label.pack(side="left", padx=(10, 0))

        # Priority Value
        self.priority_value = ctk.CTkLabel(
            toolbar,
            text="5:5",
            font=self.normal_font,
            text_color=self.text_color
        )
        self.priority_value.grid(row=0, column=4, padx=10, pady=5)

        self.priority_slider.configure(command=self._update_priority_value)

    def _build_junction_scroll_area(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(
            container,
            orientation="horizontal",
            fg_color="transparent"
        )
        self.scroll_frame.pack(fill="both", expand=True)

        self._add_junction_frame("Traffic Junction #1", "#FF0000", 1)
        self._add_junction_frame("Traffic Junction #2", "#FFD700", 2)
        self._add_junction_frame("Traffic Junction #3", "#00CC00", 3)
        self._add_junction_frame("Traffic Junction #4", "#0f5e21", 4)

    def _add_junction_frame(self, title, color, junction_id):
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="white", corner_radius=10, width=400)
        frame.pack(side="left", padx=10, fill="y")
        
        frame.grid_columnconfigure(0, weight=1)
        for row in range(6):
            frame.grid_rowconfigure(row, weight=0)
        
        # Spacing in between the title and image
        frame.grid_rowconfigure(1, weight=1)
        # Spacing in between the image and data
        frame.grid_rowconfigure(3, weight=1)

        # Makes widget maintain its size
        frame.grid_propagate(False)

        self.make_widget_button(frame, junction_id)

        # Title with colored background
        title_frame = ctk.CTkFrame(frame, fg_color=color, corner_radius=5)
        title_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=title,
            font=self.subheader_font,
            text_color="black"
        )
        title_label.pack(pady=5)
        self.make_widget_button(title_frame, junction_id)
        self.make_widget_button(title_label, junction_id)

        # Image section
        try:
            image = ctk.CTkImage(Image.open("test_junction.png"), size=(300, 300))
            image_label = ctk.CTkLabel(frame, image=image, text="")
            image_label.grid(row=2, column=0, pady=10)
            self.make_widget_button(image_label, junction_id)
        except:
            placeholder = ctk.CTkFrame(frame, width=200, height=200, fg_color="#CCCCCC")
            placeholder.grid(row=1, column=0, pady=10)
            self.make_widget_button(placeholder, junction_id)
            placeholder_text = ctk.CTkLabel(placeholder, text="Junction\nImage", text_color="black")
            placeholder_text.place(relx=0.5, rely=0.5, anchor="center")
            self.make_widget_button(placeholder_text, junction_id)
            placeholder.pack_propagate(False)

        # Frame for all the stats
        stats_frame = ctk.CTkFrame(frame, fg_color="white")
        stats_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
        self.make_widget_button(stats_frame, junction_id)
        
        for i in range(3):
            stats_frame.grid_columnconfigure(i, weight=1)

        self._add_stat_group(stats_frame, "Avg. Wait Time [s]", 0, junction_id)
        self._add_stat_group(stats_frame, "Max Wait Time [s]", 1, junction_id)
        self._add_stat_group(stats_frame, "Max Queue Len [cars]", 2, junction_id)

        # Overall score
        score_label = ctk.CTkLabel(
            frame,
            text="Overall Score: XX%",
            font=self.subheader_font,
            text_color=self.text_color
        )
        score_label.grid(row=5, column=0, pady=(5, 10))
        self.make_widget_button(score_label, junction_id)

    def _add_stat_group(self, parent, title, column, junction_id):
        group = ctk.CTkFrame(parent, fg_color="#F0F0F0")
        group.grid(row=0, column=column, sticky="nsew", padx=2)
        self.make_widget_button(group, junction_id)
        title_label = ctk.CTkLabel(
            group,
            text=title,
            font=self.normal_font,
            text_color=self.text_color
        )
        title_label.pack(anchor="center")
        self.make_widget_button(title_label, junction_id)
        for direction in ["N", "S", "E", "W"]:
            direction_label = ctk.CTkLabel(
                group,
                text=f"{direction}: XX",
                font=self.small_font,
                text_color=self.text_color
            )
            direction_label.pack(anchor="center")
            self.make_widget_button(direction_label, junction_id)

    def _build_compare_button(self):
        compare_btn = ctk.CTkButton(
            self,
            text="Compare Traffic Junctions",
            fg_color="#00CC00",
            text_color="white",
            width=200,
            command=self.compare_junctions
        )
        compare_btn.pack(side="bottom", pady=20)

    def _update_priority_value(self, value):
        left_value = int(value)
        right_value = 10 - left_value
        self.priority_value.configure(text=f"{left_value}:{right_value}")

    def compare_junctions(self):
        print("Comparing traffic junctions...")
    
    def junction_pressed(self, junctionid):
        self.controller.show_page("TrafficSimulatorUI")
        print(f"Clicked junction {junctionid}")

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
    page = TrafficCollectionUI(container, app)
    page.grid(row = 0, column = 0, sticky ="news")
    app.mainloop()