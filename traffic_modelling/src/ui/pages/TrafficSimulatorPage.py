import tkinter as tk
import customtkinter as ctk
import pickle

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class TrafficSimulatorUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.configuration = {}

        self.controller = controller # Main tkinter page

        # font size and colours
        self.header_font = ctk.CTkFont(size=16, weight="bold")
        self.subheader_font = ctk.CTkFont(size=14, weight="bold")
        self.normal_font = ctk.CTkFont(size=13)
        self.small_font = ctk.CTkFont(size=11)
        self.text_color = "black"

        # PANEL SETTINGS

        # tool bar (top, fixed)
        self._build_top_toolbar()

        # main pane (everything other than tool bar, splits vertically where top: junction+params and bottom: data+graph)
        self.main_vpane = tk.PanedWindow(self, orient=tk.VERTICAL)
        self.main_vpane.pack(fill="both", expand=True)

        # top main pane (splits horizontally where left: junction and right: params)
        self.top_hpane = tk.PanedWindow(self.main_vpane, orient=tk.HORIZONTAL)

        # left top main pane (junction)
        self.junction_frame = ctk.CTkFrame(self.top_hpane, fg_color="#FFFFFF")
        self._build_junction_area(self.junction_frame)
        self.top_hpane.add(self.junction_frame, minsize=300, stretch="always")

        # right top main pane (params)
        self.params_frame = ctk.CTkFrame(self.top_hpane, fg_color="#F7F7F7")
        self._build_parameter_area(self.params_frame)
        self.top_hpane.add(self.params_frame, minsize=300, stretch="always")

        self.main_vpane.add(self.top_hpane, minsize=200, stretch="always")

        # top main pane (splits horizontally where left: data and right: graph)
        self.bottom_hpane = tk.PanedWindow(self.main_vpane, orient=tk.HORIZONTAL)

        # left bottom main pane (data)
        self.data_collected_frame = ctk.CTkFrame(self.bottom_hpane, fg_color="#EFEFEF")
        self._build_data_collected_area(self.data_collected_frame)
        self.bottom_hpane.add(self.data_collected_frame, minsize=200, stretch="always")

        # right bottom main pane (graph)
        self.graph_frame = ctk.CTkFrame(self.bottom_hpane, fg_color="#FFFFFF")
        self._build_graph_area(self.graph_frame)
        self.bottom_hpane.add(self.graph_frame, minsize=200, stretch="always")

        self.main_vpane.add(self.bottom_hpane, minsize=150, stretch="always")


    # TOOLBAR
    
    def _build_top_toolbar(self):
        toolbar = ctk.CTkFrame(self, fg_color="#EEEEEE")
        toolbar.pack(side="top", fill="x")

        # .grid to position inside the toolbar
        for col in range(8):
            toolbar.grid_columnconfigure(col, weight=0)
        toolbar.grid_columnconfigure(1, weight=1)
        toolbar.grid_columnconfigure(7, weight=1)

        back_button = ctk.CTkButton(
            toolbar, text="← Go to Traffic Collection",
            text_color= "white",
            command=self.go_to_traffic_collection
        )
        back_button.grid(row=0, column=0, padx=(10,10), pady=5, sticky="w")

        sim_label = ctk.CTkLabel(
            toolbar,
            text="Simulation",
            font=self.header_font,
            text_color=self.text_color
        )
        sim_label.grid(row=0, column=2, padx=5, pady=5)

        run_btn = ctk.CTkButton(
            toolbar,
            text="Run",
            fg_color="#00CC00",
            text_color="#FFFFFF",
            command=self.run_simulation
        )
        run_btn.grid(row=0, column=3, padx=5, pady=5)

        stop_btn = ctk.CTkButton(
            toolbar,
            text="Stop",
            fg_color="#CC0000",
            text_color="#FFFFFF",
            command=self.stop_simulation
        )
        stop_btn.grid(row=0, column=4, padx=5, pady=5)

        speed_label = ctk.CTkLabel(
            toolbar,
            text="Simulation speed:",
            font=self.normal_font,
            text_color=self.text_color
        )
        speed_label.grid(row=0, column=5, padx=(20,5), pady=5, sticky="e")

        self.sim_speed_var = tk.StringVar(value="x1")
        speed_om = ctk.CTkOptionMenu(
            toolbar,
            values=["x1", "x1.5", "x2"],
            variable=self.sim_speed_var,
            width=70
        )
        speed_om.grid(row=0, column=6, padx=(0,10), pady=5, sticky="w")


    # TOP LEFT MAIN PANE (JUNCTION)

    def _build_junction_area(self, parent):
        parent.grid_rowconfigure(1, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # edit here later for changing traffic junction name
        tj_label = ctk.CTkLabel(
            parent,
            text="Traffic Junction #1",
            font=self.subheader_font,
            text_color=self.text_color
        )
        tj_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))

        # edit here later for junction simulator
        junction_placeholder = ctk.CTkLabel(
            parent,
            text="[Traffic Junction Graphic Placeholder]",
            fg_color="#C2FFC2",
            text_color="#000000",
            font=self.normal_font
        )
        junction_placeholder.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    
    # TOP RIGHT MAIN PANE (PARAMS)

    def _build_parameter_area(self, parent):
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=0)
        parent.grid_columnconfigure(0, weight=1)

        # sub-frame to place primary and configurable params frames side-by-side
        param_top = ctk.CTkFrame(parent, fg_color="#DDDDDD")
        param_top.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        param_top.grid_columnconfigure(0, weight=1)
        param_top.grid_columnconfigure(1, weight=1)
        param_top.grid_rowconfigure(0, weight=1)

        # primary frame
        self.primary_frame = ctk.CTkScrollableFrame(param_top, fg_color="#FFFFFF")
        self.primary_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self._build_primary_parameters(self.primary_frame)

        # configurable frame
        self.config_frame = ctk.CTkScrollableFrame(param_top, fg_color="#FFFFFF")
        self.config_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self._build_configurable_parameters(self.config_frame)

        # bottom row for save/load param button
        buttons_frame = ctk.CTkFrame(parent, fg_color="#F7F7F7")
        buttons_frame.grid(row=1, column=0, pady=5)
        self._build_param_buttons(buttons_frame)

    def _build_primary_parameters(self, parent):
        title_label = ctk.CTkLabel(
            parent,
            text="Primary Input Parameters",
            font=self.subheader_font,
            text_color=self.text_color
        )
        title_label.pack(pady=(5,5))

        self._build_one_direction_parameter(parent, "Northbound", ["North", "East", "West"])
        self._build_one_direction_parameter(parent, "Eastbound", ["East", "North", "South"])
        self._build_one_direction_parameter(parent, "Southbound", ["South", "East", "West"])
        self._build_one_direction_parameter(parent, "Westbound", ["West", "North", "South"])

    def _build_one_direction_parameter(self, parent, dir_label, sub_exits):
        self.configuration[f"{dir_label} flow"] = {}
        container = ctk.CTkFrame(parent, fg_color="#FAFAFA", corner_radius=5)
        container.pack(padx=5, pady=(5,10), fill="x")

        total_label_var = tk.StringVar(value=f"{dir_label} Traffic Flow: 0 vph")
        total_label = ctk.CTkLabel(container, textvariable=total_label_var, font=self.normal_font, text_color=self.text_color)
        total_label.pack(anchor="w", padx=10, pady=(5,2))

        flows = []
        for i, exit_dir in enumerate(sub_exits, start=1):
            flow_var = tk.StringVar(value="50")
            self.configuration[f"{dir_label} flow"][exit_dir] = flow_var
            rowf = ctk.CTkFrame(container, fg_color="#FAFAFA")
            rowf.pack(anchor="w", padx=25, pady=2, fill="x")

            sub_label = ctk.CTkLabel(rowf, text=f"{chr(96 + i)}. Exiting {exit_dir} (vph):", anchor="w", text_color=self.text_color)
            sub_label.grid(row=0, column=0, sticky="w")

            entry = ctk.CTkEntry(rowf, width=60, textvariable=flow_var, fg_color="white", text_color="black")
            entry.grid(row=0, column=1, padx=(5,0))

            flow_var.trace_add("write", lambda *_: self._update_sum(container, total_label_var))
            flows.append(flow_var)

        container.flows = flows
        container.total_label_var = total_label_var
        self._update_sum(container, total_label_var)

    def _update_sum(self, container, total_label_var):
        total = 0
        for var in container.flows:
            try:
                total += float(var.get())
            except ValueError:
                pass
        prefix = total_label_var.get().split(":")[0]
        total_label_var.set(f"{prefix}: {int(total)} vph")

    def _build_configurable_parameters(self, parent):
        title_label = ctk.CTkLabel(parent, text="Configurable Parameters", font=self.subheader_font, text_color=self.text_color)
        title_label.pack(pady=(5, 5))

        # lane configs
        lane_frame = ctk.CTkFrame(parent, fg_color="#F0F0F0", corner_radius=5)
        lane_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(lane_frame, text="Lane Configurations", font=self.subheader_font, text_color=self.text_color).pack(anchor="w", padx=10, pady=(5, 2))

        self._build_config_row(lane_frame, "Number of Lanes", ["1", "2", "3", "4", "5"])
        self._build_config_row(lane_frame, "Left Turn Lane", ["Yes", "No"])

        # bus/cycle (part of lane configs)
        sub_lane_frame = ctk.CTkFrame(lane_frame, fg_color="#EAEAEA", corner_radius=5)
        sub_lane_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(sub_lane_frame, text="Bus/Cycle Lane and Traffic Flow Settings", font=self.normal_font, text_color=self.text_color).pack(anchor="w", padx=10, pady=(5, 2))

        self._build_config_row(sub_lane_frame, "Bus/Cycle Lane", ["Yes", "No"])
        self._build_config_row(sub_lane_frame, "Vehicle Type", ["Bus", "Bicycle"])

        flow_frame = ctk.CTkFrame(sub_lane_frame, fg_color="#E0E0E0", corner_radius=5)
        flow_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(flow_frame, text="Buses/Bicycles per hour (arrival direction → dest. direction)", font=self.normal_font, text_color=self.text_color).pack(anchor="w", padx=10, pady=(5, 2))

        directions = [
            "N → W", "N → S", "N → E",
            "E → N", "E → W", "E → S",
            "S → E", "S → N", "S → W",
            "W → S", "W → E", "W → N"
        ]
        self.configuration["Special Vehicles"] = {}
        for direction in directions:
            self._build_config_entry(flow_frame, f"{direction}")

        # pedestrian configs
        ped_frame = ctk.CTkFrame(parent, fg_color="#F0F0F0", corner_radius=5)
        ped_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(ped_frame, text="Pedestrian Settings", font=self.subheader_font, text_color=self.text_color).pack(anchor="w", padx=10, pady=(5, 2))

        for direction in ["North", "East", "South", "West"]:
            ped_sub_frame = ctk.CTkFrame(ped_frame, fg_color="#EAEAEA", corner_radius=5)
            ped_sub_frame.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(ped_sub_frame, text=f"{direction} Pedestrian Crossing", font=self.normal_font, text_color=self.text_color).pack(anchor="w", padx=10, pady=(5, 2))

            self._build_config_row(ped_sub_frame, f"Pedestrian Crossing {direction}", ["Yes", "No"])
            self._build_config_entry(ped_sub_frame, f"Duration {direction} [sec]")
            self._build_config_entry(ped_sub_frame, f"Requests {direction} per hour")

        # prioritised traffic configs
        priority_frame = ctk.CTkFrame(parent, fg_color="#F0F0F0", corner_radius=5)
        priority_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(priority_frame, text="Traffic Flow Prioritisation", font=self.subheader_font, text_color=self.text_color).pack(anchor="w", padx=10, pady=(5, 2))

        for d in ["North", "East", "South", "West"]:
            self._build_config_row(priority_frame, f"Priority {d}", ["0", "1", "2", "3", "4"])

    def _build_config_row(self, parent, label, options):
        row = ctk.CTkFrame(parent, fg_color="#FAFAFA")
        row.pack(fill="x", padx=5, pady=2)

        lbl = ctk.CTkLabel(row, text=f"{label}:", text_color=self.text_color)
        lbl.grid(row=0, column=0, padx=5, sticky="w")

        var = tk.StringVar(value=options[0])
        opt_menu = ctk.CTkOptionMenu(row, values=options, variable=var)
        opt_menu.grid(row=0, column=1, padx=5, sticky="w")

    def _build_config_entry(self, parent, label):
        row = ctk.CTkFrame(parent, fg_color="#FAFAFA")
        row.pack(fill="x", padx=5, pady=2)

        lbl = ctk.CTkLabel(row, text=f"{label}:", text_color=self.text_color)
        lbl.grid(row=0, column=0, padx=5, sticky="w")

        var = tk.StringVar(value="")
        self.configuration["Special Vehicles"][label] = var
        entry = ctk.CTkEntry(row, width=60, fg_color="white", text_color="black", textvariable=var)
        entry.grid(row=0, column=1, padx=5, sticky="w")

    def _build_config_row(self, parent, label, options):
        row = ctk.CTkFrame(parent, fg_color="#FAFAFA")
        row.pack(fill="x", padx=5, pady=2)

        lbl = ctk.CTkLabel(row, text=f"{label}:", text_color=self.text_color)
        lbl.grid(row=0, column=0, padx=5, sticky="w")

        var = tk.StringVar(value=options[0])
        self.configuration[label] = var
        opt_menu = ctk.CTkOptionMenu(
            row,
            values=options,
            variable=var,
            fg_color="#D3D3D3",
            button_color="#A9A9A9",
            button_hover_color="#808080",
            text_color="black"
        )
        opt_menu.grid(row=0, column=1, padx=5, sticky="w")

    def _build_config_entry(self, parent, label):
        row = ctk.CTkFrame(parent, fg_color="#FAFAFA")
        row.pack(fill="x", padx=5, pady=2)

        lbl = ctk.CTkLabel(row, text=f"{label}:", text_color=self.text_color)
        lbl.grid(row=0, column=0, padx=5, sticky="w")
        
        var = tk.StringVar(value="")
        self.configuration["Special Vehicles"][label] = var

        entry = ctk.CTkEntry(row, width=60, fg_color="white", text_color="black", textvariable=var)
        entry.grid(row=0, column=1, padx=5, sticky="w")

    def _build_param_buttons(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        frame = ctk.CTkFrame(parent, fg_color="#F7F7F7")
        frame.grid(row=0, column=0)

        save_btn = ctk.CTkButton(
            frame,
            text="Save Parameter Settings",
            fg_color="#2E7D32",
            text_color="#FFFFFF",
            command=self.save_parameters
        )
        save_btn.grid(row=0, column=0, padx=10, pady=5)

        load_btn = ctk.CTkButton(
            frame,
            text="Load Parameter Settings",
            fg_color="#1565C0",
            text_color="#FFFFFF",
            command=self.load_parameters
        )
        load_btn.grid(row=0, column=1, padx=10, pady=5)


    #  bottom left main pane (data)

    def _build_data_collected_area(self, parent):
        parent.grid_columnconfigure((0,1,2), weight=1)
        parent.grid_rowconfigure(0, weight=0)

        data_label = ctk.CTkLabel(
            parent,
            text="Data Collected",
            font=self.subheader_font,
            text_color=self.text_color
        )
        data_label.grid(row=0, column=0, columnspan=3, pady=(5,5))

        avg_lbl = ctk.CTkLabel(
            parent,
            text="Average Wait Time:\nNorthbound: XX sec\nEastbound: XX sec\nSouthbound: XX sec\nWestbound: XX sec",
            font=self.small_font,
            justify="left",
            text_color=self.text_color
        )
        avg_lbl.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

        max_lbl = ctk.CTkLabel(
            parent,
            text="Maximum Wait Time:\nNorthbound: XX sec\nEastbound: XX sec\nSouthbound: XX sec\nWestbound: XX sec",
            font=self.small_font,
            justify="left",
            text_color=self.text_color
        )
        max_lbl.grid(row=1, column=1, sticky="nw", padx=10, pady=5)

        queue_lbl = ctk.CTkLabel(
            parent,
            text="Maximum Queue Length [cars]:\nNorthbound: XX\nEastbound: XX\nSouthbound: XX\nWestbound: XX",
            font=self.small_font,
            justify="left",
            text_color=self.text_color
        )
        queue_lbl.grid(row=1, column=2, sticky="nw", padx=10, pady=5)


    #  bottom right main pane (graph)

    def _build_graph_area(self, parent):
        parent.grid_rowconfigure(0, weight=0)  # title
        parent.grid_rowconfigure(1, weight=1)  # main area
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=0)

        title_lbl = ctk.CTkLabel(
            parent,
            text="Real-time Data Plotting Graph",
            font=self.subheader_font,
            text_color=self.text_color
        )
        title_lbl.grid(row=0, column=0, columnspan=2, pady=(5,5))

        main_frame = ctk.CTkFrame(parent, fg_color="#DDDDDD")
        main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_rowconfigure(1, weight=1)

        # graph y-axis selector
        graph_sel_frame = ctk.CTkFrame(main_frame, fg_color="#EEEEEE")
        graph_sel_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        graph_sel_frame.grid_columnconfigure(0, weight=0)
        graph_sel_frame.grid_columnconfigure(1, weight=0)
        graph_sel_frame.grid_columnconfigure(2, weight=1)

        self.graph_param_var = tk.StringVar(value="Average Wait Time [s]")
        param_menu = ctk.CTkOptionMenu(
            graph_sel_frame,
            values=["Average Wait Time [s]", "Maximum Wait Time [s]", "Max Queue Length [cars]"],
            variable=self.graph_param_var,
            width=180
        )
        param_menu.grid(row=0, column=0, padx=(10,10), pady=5, sticky="w")

        self.graph_dir_var = tk.StringVar(value="North")
        dir_menu = ctk.CTkOptionMenu(
            graph_sel_frame,
            values=["North","East","South","West"],
            variable=self.graph_dir_var,
            width=80
        )
        dir_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # edit this later for displaying the graph
        graph_placeholder = ctk.CTkLabel(
            main_frame,
            text="[Graph Placeholder]",
            font=self.normal_font,
            text_color="#000000",
            fg_color="#FFFFFF",
            corner_radius=5
        )
        graph_placeholder.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        # save data and traffic button
        save_btn = ctk.CTkButton(
            main_frame,
            text="Save Traffic Junction and Collected Data",
            fg_color="#4CAF50",
            text_color="#FFFFFF",
            command=self.save_junction_data
        )
        save_btn.grid(row=1, column=1, sticky="n", padx=10, pady=5)


    #  button print messages (for debug)

    def go_to_traffic_collection(self):
        self.controller.show_page("TrafficCollectionUI")
        print("clicked Go to Traffic Collection")

    def run_simulation(self):
        print("clicked Run Simulation")

    def stop_simulation(self):
        print("clicked Stop Simulation")

    def save_parameters(self):
        print("clicked Save Parameter Settings")
        config_file = {}
        for key in self.configuration:
            if isinstance(self.configuration[key], dict):
                config_file[key] = {}
                for subkey in self.configuration[key]:
                    config_file[key][subkey] = self.configuration[key][subkey].get()
                    # print(f"{key} - {subkey}: {self.configuration[key][subkey].get()}")
            else:
                config_file[key] = self.configuration[key].get()
                # print(f"{key}: {self.configuration[key].get()}")
        print(config_file)
        with (open("config_file.pkl", "wb")) as f:
            pickle.dump(config_file, f)

    def load_parameters(self):
        print("clicked Load Parameter Settings")
        with (open("config_file.pkl", "rb")) as f:
            config_file = pickle.load(f)
            # print(self.configuration)
            for key in self.configuration:
                if isinstance(self.configuration[key], dict):
                    for subkey in self.configuration[key]:
                        self.configuration[key][subkey].set(config_file[key][subkey])
                else:
                    self.configuration[key].set(config_file[key])

    def save_junction_data(self):
        print("clicked Save Traffic Junction and Collected Data")

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Traffic Junction Modelling")
    app.geometry("1300x800")
    app.minsize(900, 600)

    container = ctk.CTkFrame(app)  
    container.pack(side = "top", fill = "both", expand = True) 

    container.grid_rowconfigure(0, weight = 1)
    container.grid_columnconfigure(0, weight = 1)
    page = TrafficSimulatorUI(container, app)
    page.grid(row = 0, column = 0, sticky ="news")
    app.mainloop()