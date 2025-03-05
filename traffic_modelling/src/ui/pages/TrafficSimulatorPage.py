import tkinter as tk
import customtkinter as ctk
import pickle
import sys
import os

# add the src directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from PIL import Image

from objects.car import Car
from models.Junction import Junction, JunctionBuilder
from models.Vehicle import Vehicle
from simulation import Simulation, StatsCollector

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class TrafficSimulatorUI(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.configuration = {}

        # simulation settings
        self.simulation_started = False

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

        self.GAME_WIDTH = 800
        self.GAME_HEIGHT = 600
        self.cars_west = []
        self.cars_east = []
        self.cars_north = []
        self.cars_south = []
        self.car_spacing = 10  # pixels between cars
        self.current_green_direction = 'W'  # Which direction has green light (W, E, N, S)
        self.cars_per_green = 10  # How many cars can pass during one green light
        self.moving_cars = []


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
        tk_label = ctk.CTkLabel(
            parent,
            text="Traffic Junction #1",
            font=self.subheader_font,
            text_color=self.text_color
        )
        tk_label.grid(row=0, column=0, sticky="w", padx=10, pady=(5,0))

        # edit here later for junction simulator
        self.junction = ctk.CTkLabel(
            parent,
            text="",
            fg_color="#C2FFC2",
            text_color="#000000",
            font=self.normal_font
        )
        self.junction.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.colour = 0
        # self.show_simulation()

    def configure_simulation(self):
        conf = self.make_config()
        count = 0
        for _ in range(int(conf["Eastbound flow"]["East"])):
            self.cars_east.append(Car(x=200 - count * (118 + self.car_spacing), y=210, width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='E', destination='E'))
            count += 1
        for _ in range(int(conf["Eastbound flow"]["North"])):
            self.cars_east.append(Car(x=200 - count * (118 + self.car_spacing), y=210, width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='E', destination='N'))
            count += 1
        for _ in range(int(conf["Eastbound flow"]["South"])):
            self.cars_east.append(Car(x=200 - count * (118 + self.car_spacing), y=210, width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='E', destination='S'))
            count += 1
        
        count = 0
        for _ in range(int(conf["Westbound flow"]["South"])):
            self.cars_west.append(Car(x=600 + count * (118 + self.car_spacing), y=350, width=self.GAME_WIDTH, height=self.GAME_HEIGHT,direction='W', destination='S'))
            count += 1
        for _ in range(int(conf["Westbound flow"]["North"])):
            self.cars_west.append(Car(x=600 + count * (118 + self.car_spacing), y=350, width=self.GAME_WIDTH, height=self.GAME_HEIGHT,direction='W', destination='N'))
            count += 1
        for _ in range(int(conf["Westbound flow"]["West"])):
            self.cars_west.append(Car(x=600 + count * (118 + self.car_spacing), y=350, width=self.GAME_WIDTH, height=self.GAME_HEIGHT,direction='W', destination='W'))
            count += 1

        count = 0
        for _ in range(int(conf["Southbound flow"]["West"])):
            self.cars_south.append(Car(x=420, y=100 - count * (72 + self.car_spacing), width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='S', destination='W'))
            count += 1
        for _ in range(int(conf["Southbound flow"]["South"])):
            self.cars_south.append(Car(x=420, y=100 - count * (72 + self.car_spacing), width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='S', destination='S'))
            count += 1
        for _ in range(int(conf["Southbound flow"]["East"])):
            self.cars_south.append(Car(x=420, y=100 - count * (72 + self.car_spacing), width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='S', destination='E'))
            count += 1
          
        count = 0
        for _ in range(int(conf["Northbound flow"]["North"])):
            self.cars_north.append(Car(x=310, y=460 + count * (72 + self.car_spacing), width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='N', destination='N'))
            count += 1
        for _ in range(int(conf["Northbound flow"]["West"])):
            self.cars_north.append(Car(x=310, y=460 + count * (72 + self.car_spacing), width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='N', destination='W'))
            count += 1
        for _ in range(int(conf["Northbound flow"]["East"])):
            self.cars_north.append(Car(x=310, y=460 + count * (72 + self.car_spacing), width=self.GAME_WIDTH, height=self.GAME_HEIGHT, direction='N', destination='E'))
            count += 1

    def show_simulation(self):
        # Get frame dimensions for scaling
        frame_width = self.junction.winfo_width()
        frame_height = self.junction.winfo_height()
        
        # Create fixed-size surface
        pygame_screen = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))
        
        try:
            # Load and scale background image
            background = pygame.image.load("assets/junction.png")
            background = pygame.transform.scale(background, (self.GAME_WIDTH, self.GAME_HEIGHT))
            pygame_screen.blit(background, (0, 0))
            
            # Calculate line dimensions using fixed size
            line_thickness = 10
            extension_ratio_x = 0.17
            extension_ratio_y = 0.25
            center_x = self.GAME_WIDTH / 2
            center_y = self.GAME_HEIGHT / 2
            
            # Calculate line lengths
            line_length_x = self.GAME_WIDTH * extension_ratio_x
            line_length_y = self.GAME_HEIGHT * extension_ratio_y
            
            # Calculate start and end points for horizontal line
            h_start_x = center_x - line_length_x
            h_end_x = center_x + line_length_x
            h_y = center_y
            
            # Horizontal traffic dividers
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (0, h_y),
                (h_start_x, h_y),
                line_thickness
            )
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (h_end_x, h_y),
                (self.GAME_WIDTH, h_y),
                line_thickness
            )

            # Calculate start and end points for vertical traffic dividers
            v_start_y = center_y - line_length_y
            v_end_y = center_y + line_length_y
            v_x = center_x
            
            # Vertical traffic dividers
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (v_x, 0),
                (v_x, v_start_y),
                line_thickness
            )
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (v_x, v_end_y),
                (v_x, self.GAME_HEIGHT),
                line_thickness
            )
            
            # Stop lines for horizontal traffic dividers
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (h_start_x + line_thickness // 2, v_start_y + 0.02 * self.GAME_HEIGHT),
                (h_start_x + line_thickness // 2, v_end_y  - 0.02 * self.GAME_HEIGHT),
                line_thickness
            )
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (h_end_x, v_start_y + 0.02 * self.GAME_HEIGHT),
                (h_end_x, v_end_y - 0.02 * self.GAME_HEIGHT),
                line_thickness
            )
            # Stop lines for vertical traffic dividers
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (h_start_x + 0.035 * self.GAME_WIDTH, v_start_y),
                (h_end_x - 0.035 * self.GAME_WIDTH, v_start_y),
                line_thickness
            )
            pygame.draw.line(
                pygame_screen,
                (255, 255, 255),
                (h_start_x  + 0.035 * self.GAME_WIDTH, v_end_y),
                (h_end_x - 0.035 * self.GAME_WIDTH, v_end_y),
                line_thickness
            )

            for car in self.cars_west[:min(self.cars_per_green, len(self.cars_west))]:
                car.draw(pygame_screen)
            for car in self.cars_east[:min(self.cars_per_green, len(self.cars_east))]:
                car.draw(pygame_screen)
            for car in self.cars_north[:min(self.cars_per_green, len(self.cars_north))]:
                car.draw(pygame_screen)
            for car in self.cars_south[:min(self.cars_per_green, len(self.cars_south))]:
                car.draw(pygame_screen)
            
            if not self.moving_cars:
                print("No moving cars")
                print(self.current_green_direction)
                if self.current_green_direction == 'W':
                    num_cars = min(self.cars_per_green, len(self.cars_west))
                    for car in self.cars_west[:num_cars]:
                        self.moving_cars.append(car)
                        self.cars_west.remove(car)
                    for car in self.cars_west:
                        car.move(- ((num_cars - 1) * (118 + self.car_spacing)), 0)
                elif self.current_green_direction == 'E':
                    num_cars = min(self.cars_per_green, len(self.cars_east))
                    for car in self.cars_east[:num_cars]:
                        self.moving_cars.append(car)
                        self.cars_east.remove(car)
                    for car in self.cars_east:
                        car.move((num_cars - 1) * (118 + self.car_spacing), 0)
                elif self.current_green_direction == 'S':
                    num_cars = min(self.cars_per_green, len(self.cars_south))
                    for car in self.cars_south[:num_cars]:
                        self.moving_cars.append(car)
                        self.cars_south.remove(car)
                    for car in self.cars_south:
                        car.move(0, (num_cars - 1) * (72 + self.car_spacing))
                elif self.current_green_direction == 'N':
                    num_cars = min(self.cars_per_green, len(self.cars_north))
                    for car in self.cars_north[:num_cars]:
                        self.moving_cars.append(car)
                        self.cars_north.remove(car)
                    for car in self.cars_north:
                        car.move(0, -((num_cars - 1) * (72 + self.car_spacing)))
                for car in self.moving_cars:
                    print(car.direction, car.destination)
            else:
                for car in self.moving_cars:
                    car.go_destination()
                    car.draw(pygame_screen)
                    if car.out_of_bounds():
                        self.moving_cars.remove(car)

                direction_order = ['W', 'N', 'E', 'S']
                current_index = direction_order.index(self.current_green_direction)
                self.current_green_direction = direction_order[(current_index + 1) % 4]
        except Exception as e:
            print(e)
            # Fallback if image loading fails
            pygame_screen.fill((255, 255, 255))  # White background
        
        
        pygame_image = pygame.surfarray.array3d(pygame_screen)
        pygame_image = pygame_image.swapaxes(0, 1)
        pygame_image = ctk.CTkImage(Image.fromarray(pygame_image), size=(frame_width, frame_height))
        
        self.junction.configure(image=pygame_image)
        
        speed = int(20/float(self.sim_speed_var.get().split("x")[1]))
        
        if self.simulation_started:
            try:
                self.after(speed, self.show_simulation)
            except:      
                sys.exit()
    
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

        self.avg_lbl = ctk.CTkLabel(
            parent,
            text="Average Wait Time:\nNorthbound: XX sec\nEastbound: XX sec\nSouthbound: XX sec\nWestbound: XX sec",
            font=self.small_font,
            justify="left",
            text_color=self.text_color
        )
        self.avg_lbl.grid(row=1, column=0, sticky="nw", padx=10, pady=5)

        self.max_lbl = ctk.CTkLabel(
            parent,
            text="Maximum Wait Time:\nNorthbound: XX sec\nEastbound: XX sec\nSouthbound: XX sec\nWestbound: XX sec",
            font=self.small_font,
            justify="left",
            text_color=self.text_color
        )
        self.max_lbl.grid(row=1, column=1, sticky="nw", padx=10, pady=5)

        self.queue_lbl = ctk.CTkLabel(
            parent,
            text="Maximum Queue Length [cars]:\nNorthbound: XX\nEastbound: XX\nSouthbound: XX\nWestbound: XX",
            font=self.small_font,
            justify="left",
            text_color=self.text_color
        )
        self.queue_lbl.grid(row=1, column=2, sticky="nw", padx=10, pady=5)

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
        self.configure_simulation()
        self.simulation_started = True
        self.show_simulation()

        # create a junction instance with the configured traffic flows
        conf = self.make_config()
        junction = (JunctionBuilder()
                    .set_traffic(
                        north_traffic=(
                            int(conf["Northbound flow"]["North"]),
                            int(conf["Northbound flow"]["East"]),
                            int(conf["Northbound flow"]["West"])
                        ),
                        south_traffic=(
                            int(conf["Southbound flow"]["South"]),
                            int(conf["Southbound flow"]["East"]),
                            int(conf["Southbound flow"]["West"])
                        ),
                        east_traffic=(
                            int(conf["Eastbound flow"]["East"]),
                            int(conf["Eastbound flow"]["North"]),
                            int(conf["Eastbound flow"]["South"])
                        ),
                        west_traffic=(
                            int(conf["Westbound flow"]["West"]),
                            int(conf["Westbound flow"]["North"]),
                            int(conf["Westbound flow"]["South"])
                        )
                    )
                    .build())

        # run the simulation for a default duration (here, 3600sec which is 60min)
        self.sim = Simulation(junction, simulation_duration=3600)
        self.sim.runSimulation()

        # initialise StatsCollector
        self.stats = StatsCollector(self.sim)

    def stop_simulation(self):
        print("clicked Stop Simulation")
        self.simulation_started = False
        
        # calculate and display statistics when the simulation is stopped
        avg_wait = self.stats.calculateAverageWaitTime()
        max_wait = self.stats.calculateMaxWaitTimes()
        max_queues = self.stats.getMaxQueueLengths()

        # update the statistics in the data pane
        self.update_data_collected(avg_wait, max_wait, max_queues)

    def update_data_collected(self, avg_wait, max_wait, max_queues):
        avg_text = (
            f"Average Wait Time:\n"
            f"Northbound: {avg_wait['north']} sec\n"
            f"Eastbound: {avg_wait['east']} sec\n"
            f"Southbound: {avg_wait['south']} sec\n"
            f"Westbound: {avg_wait['west']} sec"
        )
        max_text = (
            f"Maximum Wait Time:\n"
            f"Northbound: {max_wait['north']} sec\n"
            f"Eastbound: {max_wait['east']} sec\n"
            f"Southbound: {max_wait['south']} sec\n"
            f"Westbound: {max_wait['west']} sec"
        )
        queue_text = (
            f"Maximum Queue Length [cars]:\n"
            f"Northbound: {max_queues['north']}\n"
            f"Eastbound: {max_queues['east']}\n"
            f"Southbound: {max_queues['south']}\n"
            f"Westbound: {max_queues['west']}"
        )

        self.avg_lbl.configure(text=avg_text)
        self.max_lbl.configure(text=max_text)
        self.queue_lbl.configure(text=queue_text)
    
    def make_config(self):
        config_file = {}
        for key in self.configuration:
            if isinstance(self.configuration[key], dict):
                config_file[key] = {}
                for subkey in self.configuration[key]:
                    config_file[key][subkey] = self.configuration[key][subkey].get()
            else:
                config_file[key] = self.configuration[key].get()
        return config_file

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