# import os
# import pickle
# import sys

# import pytest
# from unittest import mock
# from PIL import Image
# from models.Junction import Junction, JunctionBuilder
# from ui.pages.TrafficSimulatorPage import TrafficSimulatorUI

# import tkinter as tk
# import customtkinter as ctk

# @pytest.fixture
# def traffic_simulator_ui():
#     #mock the image loading to return a blank image instead of None
#     with mock.patch("PIL.Image.open", return_value=Image.new("RGB", (30, 30))):
#         app = ctk.CTk()
#         container = ctk.CTkFrame(app)  
#         container.pack(side="top", fill="both", expand=True) 
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#         ui = TrafficSimulatorUI(container, app)
#         yield ui
#         app.destroy()

# def test_save_junction_data(traffic_simulator_ui, tmp_path):
#     #temporary directory for testing
#     save_dir = tmp_path / "junctions"
#     save_dir.mkdir(parents=True, exist_ok=True)
    
#     #mock the configuration to save using tk.StringVar
#     mock_config = {
#         "Northbound flow": {"North": tk.StringVar(value="50"), "East": tk.StringVar(value="30"), "West": tk.StringVar(value="20")},
#         "Eastbound flow": {"East": tk.StringVar(value="40"), "North": tk.StringVar(value="25"), "South": tk.StringVar(value="35")},
#         "Southbound flow": {"South": tk.StringVar(value="30"), "East": tk.StringVar(value="45"), "West": tk.StringVar(value="25")},
#         "Westbound flow": {"West": tk.StringVar(value="20"), "North": tk.StringVar(value="30"), "South": tk.StringVar(value="50")},
#         "Special Vehicles": {}
#     }
#     traffic_simulator_ui.configuration = mock_config
    
#     #file path for saving
#     file_name = save_dir / "junction1.pkl"
    
#     #save the configuration
#     traffic_simulator_ui.save_parameters(str(file_name))
    
#     #verify the file is created
#     assert file_name.exists(), "File was not created."
    
#     #verify the contents of the saved file
#     with open(file_name, "rb") as f:
#         saved_data = pickle.load(f)
        
#         #convert StringVar to their string values for comparison
#         expected_data = {key: {subkey: var.get() for subkey, var in subdict.items()} 
#                          if isinstance(subdict, dict) else subdict 
#                          for key, subdict in mock_config.items()}
        
#         assert saved_data == expected_data, "Saved data does not match the configuration."
