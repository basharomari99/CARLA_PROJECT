#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

# Allows controlling a vehicle with a keyboard. For a simpler and more
# documented example, please take a look at tutorial.py.

"""
Welcome to CARLA manual control.

Use ARROWS or WASD keys for control.

    W            : throttle
    S            : brake
    A/D          : steer left/right
    Q            : toggle reverse
    Space        : hand-brake
    P            : toggle autopilot
    M            : toggle manual transmission
    ,/.          : gear up/down
    CTRL + W     : toggle constant velocity mode at 60 km/h

    L            : toggle next light type
    SHIFT + L    : toggle high beam
    Z/X          : toggle right/left blinker
    I            : toggle interior light

    TAB          : change sensor position
    ` or N       : next sensor
    [1-9]        : change to sensor [1-9]
    G            : toggle radar visualization
    C            : change weather (Shift+C reverse)
    Backspace    : change vehicle

    O            : open/close all doors of vehicle
    T            : toggle vehicle's telemetry

    V            : Select next map layer (Shift+V reverse)
    B            : Load current selected map layer (Shift+B to unload)

    R            : toggle recording images to disk

    CTRL + R     : toggle recording of simulation (replacing any previous)
    CTRL + P     : start replaying last recorded simulation
    CTRL + +     : increments the start time of the replay by 1 second (+SHIFT = 10 seconds)
    CTRL + -     : decrements the start time of the replay by 1 second (+SHIFT = 10 seconds)

    F1           : toggle HUD
    H/?          : toggle help
    ESC          : quit
"""

from __future__ import print_function
import time

# ==============================================================================
# -- find carla module ---------------------------------------------------------
# ==============================================================================
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
# To import a basic agent
import sys

if sys.version_info >= (3, 0):

    from configparser import ConfigParser

else:

    from ConfigParser import RawConfigParser as ConfigParser

import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


# ==============================================================================
# -- imports -------------------------------------------------------------------
# ==============================================================================

import threading
import carla
import random
############################DEBGUS##################
PRINT_SPAWN_POINTS = False
#vehicle.bh.crossbike,"vehicle.chevrolet.impala
####################################################

################METADATA #############
LESSON_ID = 1
traffic_manager = None
SPAWN_POINT_PLAYER_INDEX_DICT = {0: 128, 1:85, 2:240}#85
BEYOND_CAR_INDEX_DICT = {0: 18,1:18}
PLAYER_BLUEPRINT_ID = "vehicle.audi.tt"
BAREL_BLUIPRIT_ID = "static.prop.barrel"
BEYOND_CAR_BLUEPRINT_ID = "vehicle.chevrolet.impala"
BEYOND_CAR_BLUEPRINT_ID_DICT = {0:"vehicle.chevrolet.impala",1:"vehicle.bh.crossbike",2:"vehicle.mercedes.coupe_2020"}
to_destroy_spawn_list = {}
auto_piloted_y_list = {}
auto_piloted_x_list = {}
ran_autopilot_x,ran_autopilot_y = False,False
telemetry = {"speed": [], "locations": [],"collisions": []}
max_speed = 0
sum_speed = 0
samples_num = 0
CARS_Z_POSITION = 0.5999999642372131
start_flag = False
##################################
DEBUG_EN = True
from carla import ColorConverter as cc

import argparse
import collections
import datetime
import logging
import math
import random
import re
import weakref

try:
    import pygame
    from pygame.locals import KMOD_CTRL
    from pygame.locals import KMOD_SHIFT
    from pygame.locals import K_0
    from pygame.locals import K_9
    from pygame.locals import K_BACKQUOTE
    from pygame.locals import K_BACKSPACE
    from pygame.locals import K_COMMA
    from pygame.locals import K_DOWN
    from pygame.locals import K_ESCAPE
    from pygame.locals import K_F1
    from pygame.locals import K_LEFT
    from pygame.locals import K_PERIOD
    from pygame.locals import K_RIGHT
    from pygame.locals import K_SLASH
    from pygame.locals import K_SPACE
    from pygame.locals import K_TAB
    from pygame.locals import K_UP
    from pygame.locals import K_a
    from pygame.locals import K_b
    from pygame.locals import K_c
    from pygame.locals import K_d
    from pygame.locals import K_f
    from pygame.locals import K_g
    from pygame.locals import K_h
    from pygame.locals import K_i
    from pygame.locals import K_l
    from pygame.locals import K_m
    from pygame.locals import K_n
    from pygame.locals import K_o
    from pygame.locals import K_p
    from pygame.locals import K_q
    from pygame.locals import K_r
    from pygame.locals import K_s
    from pygame.locals import K_t
    from pygame.locals import K_v
    from pygame.locals import K_w
    from pygame.locals import K_x
    from pygame.locals import K_z
    from pygame.locals import K_MINUS
    from pygame.locals import K_EQUALS
except ImportError:
    raise RuntimeError('cannot import pygame, make sure pygame package is installed')

try:
    import numpy as np
except ImportError:
    raise RuntimeError('cannot import numpy, make sure numpy package is installed')

#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////// OUR FUNCS /////////////////////////////////////////////////////////////////

def show_telemetry_old():
    # Example telemetry data (can be modified)

    if not start_flag:
        return

    collisions_num = 0
    frames_1 = []
    collisions = []
    for el in telemetry["collisions"]:
        collisions_num += 1
        frames_1.append(el['frame'])
        collisions.append(collisions_num)

    frames_2 = []
    speeds = []
    for el in telemetry["speed"]:
        frames_2.append(el["frame"])
        speeds.append(el['curr_speed'])

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Telemetry Data Visualization")

    # Create a figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))


    # Plot the first graph
    axs[0].plot(frames_1, collisions, marker='o', linestyle='-', color='b')
    axs[0].set_title('#Collisions Graph', fontsize=12)
    axs[0].set_xlabel('Frame', fontsize=10)
    axs[0].set_ylabel('#Collisions', fontsize=10)
    axs[0].grid(True)

    # Plot the second graph
    axs[1].plot(frames_2, speeds, marker='x', linestyle='-', color='r')
    axs[1].set_title('Speed over Time', fontsize=12)
    axs[1].set_xlabel('Frame', fontsize=10)
    axs[1].set_ylabel('Speed (km/h)', fontsize=10)
    axs[1].grid(True)

    # Create a table below the plots (sample data)
    table_data = [["MAX Speed",f"{max_speed : .3f}km/h"],["AVG Speed",f"{(sum_speed / samples_num) if samples_num > 0 else 0 : .3f}km/h"]]
    for key in telemetry:
        if not isinstance(telemetry[key], list):
            table_data.append([key, telemetry[key]])

    # Add the table (adjust its position)
    table = plt.table(cellText=table_data,
                      colLabels=['Metric', 'Value'],
                      cellLoc='center',
                      loc='bottom',
                      colColours=['#f0f0f0'] * 2,
                      bbox=[0.2, -0.3, 0.6, 0.2])

    # Adjust the layout
    plt.tight_layout()

    # Embed the plot into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)  # Embed the figure in the Tkinter window
    canvas.draw()

    # Place the canvas in the Tkinter window
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



    # Start the Tkinter main loop (this opens the pop-up window)
    root.mainloop()


class RecordingHandler():
    def __init__(self):
        self.worked = False
        self.stop_delay = None
        self.should_stop = False

    def restart(self):
        self.worked = False
        self.stop_delay = None
        self.should_stop = False

    def start_recording(self,client,world):
        if world.recording_enabled is False and self.worked == False:
            self.worked = True
            print("grepdbg recording started !!!!!!!!!!")
            print("grepdbg recording started !!!!!!!!!!")
            print("grepdbg recording started !!!!!!!!!!")
            client.start_recorder("manual_recording.rec")
            world.recording_enabled = True

    def stop_recording(self,client,world):
        delay = 3 if LESSON_ID == 0 else 7
        if self.worked and world.recording_enabled:
            if self.stop_delay is None:
                self.stop_delay = time.time()
                return
            elif time.time() - self.stop_delay < delay:
                return
            else:
                print("grepdbg recording stopped !!!!!!!!!!")
                print("grepdbg recording stopped !!!!!!!!!!")
                print("grepdbg recording stopped !!!!!!!!!!")
                client.stop_recorder()
                world.recording_enabled = False

    def handle_recording(self,client,world):
        velocity = world.player.get_velocity()
        speed = velocity.length()

        if LESSON_ID == 0:
            if world.player.get_transform().location.x <= -1:
                self.start_recording(client, world)
            if world.player.get_transform().location.x <= -50.0 or self.should_stop:
                self.should_stop = True
                self.stop_recording(client, world)
        if LESSON_ID == 1:
            abs_locXspeed = abs(world.player.get_transform().location.x + 89 ) * speed

            if abs_locXspeed > 500 or world.player.get_transform().location.x > 10:
                self.start_recording(client,world)

            if world.player.get_transform().location.x >= 33.5 or self.should_stop:
                self.should_stop = True
                self.stop_recording(client,world)

        if LESSON_ID == 2:
            if world.player.get_transform().location.y > -75.0:
                self.start_recording(client, world)
            if world.player.get_transform().location.y >= 30:
                self.stop_recording(client,world)


def destroy_auto_piloted_cars():

    global auto_piloted_y_list,auto_piloted_x_list,ran_autopilot_x,ran_autopilot_y
    for el in auto_piloted_y_list:
        print(f"DESTROYING  {el} autopilot off")
        auto_piloted_y_list[el].destroy()

    for el in auto_piloted_x_list:
        print(f"DESTROYING  {el} autopilot off")
        auto_piloted_x_list[el].destroy()

    auto_piloted_y_list = {}
    auto_piloted_x_list = {}

def disable_auto_pilot_cars():
    global auto_piloted_y_list,auto_piloted_x_list,ran_autopilot_x,ran_autopilot_y
    if ran_autopilot_y:
        for el in auto_piloted_y_list:
            print(f"setting {el} autopilot off")
            auto_piloted_y_list[el].set_autopilot(False)

    if ran_autopilot_x:
        for el in auto_piloted_x_list:
            print(f"setting {el} autopilot off")
            auto_piloted_x_list[el].set_autopilot(False)

    ran_autopilot_x, ran_autopilot_y = False, False

def show_telemetry(world,client):

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Telemetry Data Visualization")

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    def clear_canvas():
        """Clears the canvas_frame before displaying new content."""
        for widget in canvas_frame.winfo_children():
            widget.destroy()

    # Create the button click functions
    def show_collisions():
        clear_canvas()
        fig, ax = plt.subplots(figsize=(8, 6))
        collisions_num = 0
        frames_1 = []
        collisions = []
        for el in telemetry["collisions"]:
            collisions_num += 1
            frames_1.append(el['frame'])
            collisions.append(collisions_num)
        ax.plot(frames_1, collisions, marker='o', linestyle='-', color='b')
        ax.set_title('#Collisions Graph')
        ax.set_xlabel('Frame')
        ax.set_ylabel('#Collisions')
        ax.grid(True)
        show_plot(fig)

    def show_speed():
        clear_canvas()
        fig, ax = plt.subplots(figsize=(8, 6))
        frames_2 = []
        speeds = []
        for el in telemetry["speed"]:
            frames_2.append(el["frame"])
            speeds.append(el['curr_speed'])
        ax.plot(frames_2, speeds, marker='x', linestyle='-', color='r')
        ax.set_title('Speed over Time')
        ax.set_xlabel('Frame')
        ax.set_ylabel('Speed (km/h)')
        ax.grid(True)
        show_plot(fig)


    def show_table():
        clear_canvas()
        fig, ax = plt.subplots(figsize=(8, 6))
        table_data = [["MAX Speed", f"{max_speed : .3f}km/h"],
                      ["AVG Speed", f"{(sum_speed / samples_num) if samples_num > 0 else 0 : .3f}km/h"]]

        for key in telemetry:
            if not isinstance(telemetry[key], list):
                table_data.append([key, telemetry[key]])

        ax.axis('tight')
        ax.axis('off')

        # Create the table
        table = ax.table(cellText=table_data, colLabels=['Metric', 'Value'], cellLoc='center', loc='center')

        # Adjust font size of table cells
        for (i, j), cell in table.get_celld().items():
            cell.set_fontsize(10)  # Set the font size for each cell
            cell.set_text_props(fontsize=10)  # Ensure text inside cells gets the correct font size

        # Adjust font size of column labels (headers)
        for label in table.get_celld().values():
            if label.get_text() is not None:  # Ensure we are modifying labels
                label.set_fontsize(10)  # Change font size for the column headers

        # You can also adjust table auto font size behavior
        table.auto_set_font_size(False)  # Disable auto font size
        table.set_fontsize(10)  # Set desired font size for table content and headers

        show_plot(fig)

    # Function to display the plot in the window
    def show_plot(fig):
        clear_canvas()
        # Clear the current plot and create a new canvas for each plot
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def start_replaying():
        clear_canvas()
        if recording_handler.worked is False:
            return
        print("grepdbg Replaying !!!!!!!!!!")
        # stop recorder
        client.stop_recorder()
        world.recording_enabled = False
        # work around to fix camera at start of replaying
        current_index = world.camera_manager.index
        world.destroy_sensors()

        world.hud.notification("Replaying Driving lesson !")
        # replayer
        client.replay_file("manual_recording.rec", world.recording_start, 0, 0)
        world.camera_manager.set_sensor(current_index)

    def show_description():
        clear_canvas()
        if LESSON_ID == 0:
            description_label = tk.Label(canvas_frame, text=(
            "✴ Lesson 1: Maintaining a Safe Following Distance\n\n"
            "✴ What was tested?\n"
            "✦ In this lesson, you encountered a car driving ahead of you.At one point, it suddenly performed an emergency brake.\n\n"
            "✴ What could have happened?\n"
            "✦ If you maintained a safe following distance, you would have had enough time to react and brake smoothly, avoiding a collision.This would have ensured a safe and controlled driving experience.\n"
            "✦ If you followed too closely, there was a risk of not stopping in time, which could have resulted in a collision with the vehicle ahead.\n"
            "\n✴ Key takeaway:\n"
            "✦ To ensure safety, always keep a safe distance from the vehicle in front.The three-second rule helps maintain proper spacing, and in poor weather or high-speed situations, an even greater distance is recommended.\n"
            ), font=("Arial", 12), wraplength=700, justify="left")
            description_label.pack(pady=20, padx=20)

        if LESSON_ID == 1:
            description_label = tk.Label(canvas_frame, text=(
            "✴ Lesson 2: Driving Safely in Poor Weather Conditions\n\n"
            "✴ What was tested?\n"
            "✦ You were driving in rainy and foggy weather conditions when a cyclist unexpectedly emerged from a blind spot onto the street.\n\n"
            "✴ What could have happened?\n"
            "✦ If you were driving cautiously, maintaining a controlled speed, and staying attentive, you would have had enough time to react and safely slow down or stop, avoiding any dangerous situation.\n"
            "✦ If you were driving too fast or not fully focused on potential hazards, you might not have been able to react in time, increasing the risk of a collision.\n"
            "\n✴ Key takeaway:\n"
            "✦ In poor weather conditions, visibility is reduced, and unexpected obstacles may appear suddenly. Driving at a safe speed, staying alert, and anticipating possible hazards from blind spots can significantly reduce risks and ensure a safer driving experience.\n"
            ), font=("Arial", 12), wraplength=700, justify="left")
            description_label.pack(pady=20, padx=20)

        if LESSON_ID == 2:
            description_label = tk.Label(canvas_frame, text=(
            "✴ Lesson 3: Navigating Roundabouts Properly\n\n"
            "✴ What was tested?\n"
            "✦ You entered a two-lane roundabout while driving in the left lane, while another car in the right lane was also navigating the roundabout.\n\n"
            "✴ What could have happened?\n"
            "✦ If you checked your surroundings and anticipated other drivers' movements, you would have been able to adjust your position accordingly and navigate the roundabout smoothly.\n"
            "✦ If you proceeded without being fully aware of the vehicle in the right lane, there was a risk of a collision if the other car is turning left .\n"
            "\n✴ Key takeaway:\n"
            "✦ When navigating roundabouts, stay aware of surrounding vehicles, anticipate lane changes, and adjust your speed accordingly. Checking blind spots and understanding right-of-way rules help ensure a safe passage through intersections.\n"
            ), font=("Arial", 12), wraplength=700, justify="left")
            description_label.pack(pady=20, padx=20)




    disable_auto_pilot_cars()

    # Create the buttons
    button1 = tk.Button(button_frame, text="Collisions Graph", command=show_collisions)
    button1.pack(side=tk.LEFT, padx=10, pady=10)

    button2 = tk.Button(button_frame, text="Speed Graph", command=show_speed)
    button2.pack(side=tk.LEFT, padx=10, pady=10)

    button3 = tk.Button(button_frame, text="Table", command=show_table)
    button3.pack(side=tk.LEFT, padx=10, pady=10)

    button4 = tk.Button(button_frame, text="Lesson Description", command=show_description)
    button4.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a frame for displaying the plot or table
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    start_replaying_b = tk.Button(button_frame, text="start Replaying", command=start_replaying)
    start_replaying_b.pack(side=tk.LEFT, padx=10, pady=10)




    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    # Start the Tkinter main loop
    root.mainloop()
def update_Speed_info(speed):
    global max_speed, sum_speed, samples_num
    if samples_num == 0 and speed == 0:
        return
    samples_num += 1
    sum_speed += speed
    if speed > max_speed:
        max_speed = speed

def reset_telemetry():
    global telemetry,max_speed,samples_num,sum_speed
    telemetry = {"speed": [], "locations": [], "collisions": []}
    max_speed = 0
    sum_speed = 0
    samples_num = 0


def dist(L1,L2):
    return math.sqrt((L1[0] - L2[0])**2 + (L1[1] - L2[1])**2)
def spawn_barrier(world, location, rotation=(0, 0, 0),barrier_type='static.prop.streetbarrier'):
    blueprint_library = world.get_blueprint_library()
    barrier_bp = blueprint_library.find(barrier_type)  # Adjust the blueprint name as needed

    transform = carla.Transform(
        carla.Location(x=location[0], y=location[1], z=location[2]),
        carla.Rotation(pitch=rotation[0], yaw=rotation[1], roll=rotation[2])
    )
    barrier = world.spawn_actor(barrier_bp, transform)

    return barrier


def spawn_static_car(world, location, rotation = (0.0,180.0,0.0),cars_filter=None):
    """
    Spawn a static car at a specified location with a specified orientation in CARLA.

    :param client: The CARLA client object.
    :param location: A tuple (x, y, z) specifying the car's location.
    :param orientation: String specifying the car's orientation ('horizontal' or 'vertical').
    # Default horizontal orientation (yaw = 0 degrees, pitch = 0 degrees, roll = 0 degrees)
    # Example vertical orientation (yaw = 90 degrees, pitch = 90 degrees, roll = 0 degrees)
    """
    blueprint_library = world.get_blueprint_library()
    cars_filter = 'vehicle.*' if cars_filter is None else cars_filter
    vehicle_bp = random.choice(blueprint_library.filter(cars_filter))  # Choose a vehicle blueprint

    # Create the location and rotation objects
    location = carla.Location(x=location[0], y=location[1], z=location[2])
    rotation = carla.Rotation(pitch=rotation[0], yaw=rotation[1], roll=rotation[2])
    spawn_point = carla.Transform(location, rotation)

    # Spawn the vehicle
    try:
        vehicle = world.spawn_actor(vehicle_bp, spawn_point)
        if DEBUG_EN:
            print(f"Spawned car at {location} with {rotation} orientation")
        return vehicle
    except Exception as e:
        print(f"Failed to spawn car: {e}")
    
def set_up_lesson_static_environmen(world):
    if LESSON_ID == 0:
        barrier1 = spawn_barrier(world, (10.0, 131.21006774902344, 0.0), (0, 90, 0))
        barrier2 = spawn_barrier(world, (10.0, 129.21006774902344, 0.0), (0, 90, 0))
        barrier3 = spawn_barrier(world, (-31.0, 129.21006774902344, 0.0), (0, 90, 0))
        barrier4 = spawn_barrier(world, (-31.0, 130.810067749023444, 0.0), (0, 90, 0))
        to_destroy_spawn_list["barrier1"] = barrier1
        to_destroy_spawn_list["barrier2"] = barrier2
        to_destroy_spawn_list["barrier3"] = barrier3
        to_destroy_spawn_list["barrier4"] = barrier4
        loops = 5
        x_pos = 2.6
        allocated_static_cars = []
        for i in range(loops):
            static_car = None
            j = 10
            while static_car is None and j > 0:
                static_car = spawn_static_car(world, (x_pos, 130.21006774902344, CARS_Z_POSITION))
                if static_car is not None:
                    allocated_static_cars.append(static_car)
                    #calculating created car length
                    bounding_box = static_car.bounding_box
                    car_length = bounding_box.extent.x * 2
                    x_pos = (x_pos - car_length - 3)
                j -= 1
            if x_pos <= -25.9:
                break
        for i in range(len(allocated_static_cars)):
            to_destroy_spawn_list[f"static_car_{i + 1}/{len(allocated_static_cars)}"] = allocated_static_cars[i]

        constructions_car = spawn_static_car(world=world,location=(-59.7, 126.71006774902344, CARS_Z_POSITION),rotation=(0,200,0),cars_filter="vehicle.carlamotors.european_hgv")
        to_destroy_spawn_list[f"construction_car"] = constructions_car
        ambulance = spawn_static_car(world=world,location=(-52.5, 124.9, CARS_Z_POSITION),rotation=(0,270,0),cars_filter="vehicle.ford.ambulance")
        to_destroy_spawn_list[f"ambulance"] = ambulance

        b_loops = 3
        for i in range(b_loops):
            barrier = spawn_barrier(world, (-39.50 - i * 2, 124.2, 0.0), (0, 0, 0))
            to_destroy_spawn_list[f"turn_barrier{i + 1}/{b_loops}"] = barrier

        t_loops = 5
        x_pos = -35.0
        for i in range(t_loops):
            cone = spawn_barrier(world, (x_pos, 130.21006774902344, 0.0), (0, 90, 0),'static.prop.trafficcone01')
            x_pos = x_pos - 4
            to_destroy_spawn_list[f"cone{i + 1}/{t_loops}"] = cone
        c_loops = 2
        for i in range(c_loops):
            wsign = spawn_barrier(world, (x_pos,130.21006774902344, 0.0), (0, 270, 0), 'static.prop.warningconstruction')
            x_pos = x_pos - 4
            to_destroy_spawn_list[f"wsign{i + 1}/{c_loops}"] = wsign
        d_loops = 4

        for i in range(d_loops):
            dirt = spawn_barrier(world, (x_pos, 128.21006774902344 - (i % 2)*2, 0.0), (0, 270, 0), 'static.prop.dirtdebris01')
            x_pos = x_pos - (1- i % 2) * 4
            to_destroy_spawn_list[f"cdirt{i + 1}/{d_loops}"] = dirt
    elif LESSON_ID == 1:
        ambulance = spawn_static_car(world=world,location=(26.2, 31, CARS_Z_POSITION),rotation=(0,0,0),cars_filter="vehicle.ford.ambulance")
        to_destroy_spawn_list[f"ambulance"] = ambulance
        vendingmachine1 = spawn_barrier(world, (26.2, 35,0.0), (0, 270, 0),'static.prop.vendingmachine')
        vendingmachine2 = spawn_barrier(world, (26.2, 38,0.0), (0, 270, 0),'static.prop.vendingmachine')
        to_destroy_spawn_list[f"vendingmachine1"] = vendingmachine1
        to_destroy_spawn_list[f"vendingmachine2"] = vendingmachine2

        barrier1 = spawn_barrier(world, (-48.0, 38.6, 0.0), (0, 0, 0))
        barrier2 = spawn_barrier(world, (-52.0, 38.6, 0.0), (0, 0, 0))
        barrier3 = spawn_barrier(world, (25.8, 28.2, 0.0), (0, 90, 0))
        to_destroy_spawn_list["barrier1"] = barrier1
        to_destroy_spawn_list["barrier2"] = barrier2
        to_destroy_spawn_list["barrier3"] = barrier3
        for i in range(5):
            to_destroy_spawn_list[f"barrier_for_{i}"] = spawn_barrier(world, (-53.0 + i * 5, 20.8, 0.0), (0, 0, 0))
    elif LESSON_ID == 2:
        pass

def set_up_auto_piloted_cars(world):
    global auto_piloted_y_list,to_destroy_spawn_list,auto_piloted_x_list,ran_autopilot_x,ran_autopilot_y

    if not LESSON_ID == 2:
        return

    loops = 7
    y_pos = -110
    x_pos = -4.7
    allocated_auto_pilot_cars = []
    for i in range(loops):
        autopiloted_car = None
        j = 10
        while autopiloted_car is None and j > 0:
            autopiloted_car = spawn_static_car(world, (x_pos, y_pos, CARS_Z_POSITION),(0, 90, 0))
            if autopiloted_car is not None:
                allocated_auto_pilot_cars.append(autopiloted_car)
                # calculating created car length
                bounding_box = autopiloted_car.bounding_box
                car_length = bounding_box.extent.x * 2
                y_pos = (y_pos + car_length + 3)
                x_pos -= 0.2
            j -= 1
        if y_pos >= -50:
            break
    for i in range(len(allocated_auto_pilot_cars)):
        auto_piloted_y_list[f"auto_pilot_y_{i + 1}/{len(allocated_auto_pilot_cars)}"] = allocated_auto_pilot_cars[i]

    loops = 5
    x_pos = -65.3
    allocated_static_cars = []
    for i in range(loops):
        static_car = None
        j = 10
        while static_car is None and j > 0:
            static_car = spawn_static_car(world, (x_pos, 0.6, CARS_Z_POSITION),(0,0,0))
            if static_car is not None:
                allocated_static_cars.append(static_car)
                # calculating created car length
                bounding_box = static_car.bounding_box
                car_length = bounding_box.extent.x * 2
                x_pos = (x_pos + car_length + 2)
            j -= 1
        if x_pos >= -38:
            break
    for i in range(len(allocated_static_cars)):
        auto_piloted_x_list[f"auto_piloted_x_{i + 1}/{len(allocated_static_cars)}"] = allocated_static_cars[i]

def set_up_lesson_weather(world):
    if LESSON_ID == 0 or LESSON_ID == 2:
        #morning_weather
        weather = carla.WeatherParameters(
            cloudiness=20.0,  # Light clouds
            precipitation=0.0,  # No rain
            precipitation_deposits=0.0,  # Dry roads
            wind_intensity=10.0,  # Light breeze
            sun_altitude_angle=15.0,  # Morning sun, not directly overhead
            fog_density=10.0,  # Very light fog for a fresh morning feel
            fog_distance=100.0,  # High visibility
            wetness=0.0  # Dry environment
        )
    elif LESSON_ID == 1:
        #rainy_dark_weather
        weather = carla.WeatherParameters(
            cloudiness=100.0,  # Full cloud coverage
            precipitation=80.0,  # Heavy rain
            precipitation_deposits=80.0,  # Very wet roads
            wind_intensity=50.0,  # Moderate wind
            sun_altitude_angle=-20.0,  # Low sun (below the horizon for darkness)
            fog_density=30.0,  # Moderate fog
            fog_distance=10.0,  # Short visibility due to fog
            wetness=80.0  # Very wet environment
        )

    world.set_weather(weather)

def set_up_lights(vehicle,current_lights=None,is_palyer_car=True):
    current_lights = carla.VehicleLightState.NONE if current_lights is None else current_lights
    if LESSON_ID == 0:
        pass
    elif LESSON_ID == 1:
        lights = current_lights | carla.VehicleLightState.Position | carla.VehicleLightState.LowBeam
        vehicle.set_light_state(carla.VehicleLightState(lights))

def set_brake_light_state(vehicle, brake_light_on):
    # Retrieve the current light state
    current_light_state = vehicle.get_light_state()

    # Determine the new light state based on the brake_light_on flag
    if brake_light_on:
        # Turn on the brake lights
        new_light_state = current_light_state | carla.VehicleLightState.Brake
    else:
        # Turn off the brake lights
        new_light_state = current_light_state & ~carla.VehicleLightState.Brake

    # Apply the new light state to the vehicle
    vehicle.set_light_state(carla.VehicleLightState(new_light_state))


def set_speed(vehicle, target_speed):
    control = carla.VehicleControl()
    velocity = vehicle.get_velocity()
    current_speed = (velocity.x**2 + velocity.y**2 + velocity.z**2)**0.5

    # Basic control logic to adjust throttle and brake
    if current_speed < target_speed:
        control.throttle = min((target_speed - current_speed) / target_speed, 1.0)
        control.brake = 0.0
        set_brake_light_state(vehicle,brake_light_on=False)
    else:
        control.throttle = 0.0
        if target_speed > 0:
            control.brake = min((current_speed - target_speed) / target_speed, 1.0)
            set_brake_light_state(vehicle,brake_light_on=True)
        else:
            # If target_speed is zero, apply full braking or handle as needed
            control.brake = 1.0
            set_brake_light_state(vehicle,brake_light_on=True)


    vehicle.apply_control(control)

def init_spawn_active_car(name,world,blueprint,spawn_point):
    car = world.try_spawn_actor(blueprint, spawn_point)
    to_destroy_spawn_list[name] = car
    return car

def get_beyond_car_spawn_point(spawn_points):
    if LESSON_ID == 0:
        return spawn_points[BEYOND_CAR_INDEX_DICT[LESSON_ID]]
    elif LESSON_ID == 1:
        # Create the location and rotation objects
        location = carla.Location(x=30.1, y=40, z=CARS_Z_POSITION)
        rotation = carla.Rotation(pitch=0, yaw=-90, roll=0)
        return carla.Transform(location, rotation)

    elif LESSON_ID == 2:#todo fixme
        # Create the location and rotation objects
        location = carla.Location(x=-4.8, y=-118, z=CARS_Z_POSITION)
        rotation = carla.Rotation(pitch=0, yaw=90, roll=0)
        return carla.Transform(location, rotation)

#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////
#/////////////////////////////////////////////////////////////////

# ==============================================================================
# -- Global functions ----------------------------------------------------------
# ==============================================================================


def find_weather_presets():
    rgx = re.compile('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)')
    name = lambda x: ' '.join(m.group(0) for m in rgx.finditer(x))
    presets = [x for x in dir(carla.WeatherParameters) if re.match('[A-Z].+', x)]
    return [(getattr(carla.WeatherParameters, x), name(x)) for x in presets]


def get_actor_display_name(actor, truncate=250):
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return (name[:truncate - 1] + u'\u2026') if len(name) > truncate else name

def get_actor_blueprints(world, filter, generation):
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2, 3]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []




# ==============================================================================
# -- World ---------------------------------------------------------------------
# ==============================================================================


class World(object):
    def __init__(self, carla_world, hud, args):
        self.world = carla_world
        self.sync = args.sync
        self.actor_role_name = args.rolename
        try:
            self.map = self.world.get_map()
        except RuntimeError as error:
            print('RuntimeError: {}'.format(error))
            print('  The server could not send the OpenDRIVE (.xodr) file:')
            print('  Make sure it exists, has the same name of your town, and is correct.')
            sys.exit(1)
        self.hud = hud
        self.player = None
        self.beyond_car = None
        self.collision_sensor = None
        self.lane_invasion_sensor = None
        self.gnss_sensor = None
        self.imu_sensor = None
        self.radar_sensor = None
        self.camera_manager = None
        self._weather_presets = find_weather_presets()
        self._weather_index = 0
        self._actor_filter = args.filter
        self._actor_generation = args.generation
        self._gamma = args.gamma
        self.restart()
        self.world.on_tick(hud.on_world_tick)
        self.recording_enabled = False
        self.recording_start = 0
        self.constant_velocity_enabled = False
        self.show_vehicle_telemetry = False
        self.doors_are_open = False
        self.current_map_layer = 0
        self.map_layer_names = [
            carla.MapLayer.NONE,
            carla.MapLayer.Buildings,
            carla.MapLayer.Decals,
            carla.MapLayer.Foliage,
            carla.MapLayer.Ground,
            carla.MapLayer.ParkedVehicles,
            carla.MapLayer.Particles,
            carla.MapLayer.Props,
            carla.MapLayer.StreetLights,
            carla.MapLayer.Walls,
            carla.MapLayer.All
        ]

    def restart(self):
        # self.player_max_speed = 1.589
        # self.player_max_speed_fast = 3.713
        self.player_max_speed = 0.7
        self.player_max_speed_fast = 1.8

        # Keep same camera config if the camera manager exists.
        cam_index = self.camera_manager.index if self.camera_manager is not None else 0
        cam_pos_index = self.camera_manager.transform_index if self.camera_manager is not None else 0
        blueprint_list = get_actor_blueprints(self.world, self._actor_filter, self._actor_generation)
        if not blueprint_list:
            raise ValueError("Couldn't find any blueprints with the specified filters")
        blueprint = random.choice(blueprint_list)
        beyond_car_blueprint = get_actor_blueprints(self.world,BEYOND_CAR_BLUEPRINT_ID_DICT[LESSON_ID], self._actor_generation)[0]
        # blueprint = random.choice(blueprint_list)
        blueprint.set_attribute('role_name', self.actor_role_name)
        if blueprint.has_attribute('terramechanics'):
            blueprint.set_attribute('terramechanics', 'true')
        if blueprint.has_attribute('color'):
            color = random.choice(blueprint.get_attribute('color').recommended_values)
            blueprint.set_attribute('color', color)
        if blueprint.has_attribute('driver_id'):
            driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
            blueprint.set_attribute('driver_id', driver_id)
        if blueprint.has_attribute('is_invincible'):
            blueprint.set_attribute('is_invincible', 'true')
        # set the max speed
        if blueprint.has_attribute('speed'):
            self.player_max_speed = float(blueprint.get_attribute('speed').recommended_values[1])
            self.player_max_speed_fast = float(blueprint.get_attribute('speed').recommended_values[2])

        if not self.map.get_spawn_points():
            print('There are no spawn points available in your map/town.')
            print('Please add some Vehicle Spawn Point to your UE4 scene.')
            sys.exit(1)
        spawn_points = self.map.get_spawn_points()
        if PRINT_SPAWN_POINTS:
            print("spawn_points",[f"x={spawn_points[idx].location.x},y={spawn_points[idx].location.y},idx={idx}" for idx in range(len(spawn_points))])
        # Spawn the player.
        if self.player is not None:
            spawn_point = self.player.get_transform()
            spawn_point.location.z += 2.0
            spawn_point.rotation.roll = 0.0
            spawn_point.rotation.pitch = 0.0
            self.destroy()
            #set up environment
            self.player = init_spawn_active_car("Player_car",self.world, blueprint, spawn_points[SPAWN_POINT_PLAYER_INDEX_DICT[LESSON_ID]])
            self.beyond_car = init_spawn_active_car("Beyond_car",self.world, beyond_car_blueprint, get_beyond_car_spawn_point(spawn_points))

            # set up lesson env
            set_up_lesson_static_environmen(world=self.world)
            set_up_auto_piloted_cars(world=self.world)
            set_up_lesson_weather(self.world)
            set_up_lights(self.player)

            self.show_vehicle_telemetry = False
            self.modify_vehicle_physics(self.player)
        while self.player is None:
            print("LOOPING !!")
            spawn_point = random.choice(spawn_points) if spawn_points else carla.Transform()
            #set up environment
            self.player = init_spawn_active_car("Player_car",self.world, blueprint, spawn_points[SPAWN_POINT_PLAYER_INDEX_DICT[LESSON_ID]])
            self.beyond_car = init_spawn_active_car("Beyond_car",self.world, beyond_car_blueprint,get_beyond_car_spawn_point(spawn_points))

            #set up lesson env
            set_up_lesson_static_environmen(world=self.world)
            set_up_auto_piloted_cars(world=self.world)
            set_up_lesson_weather(self.world)
            set_up_lights(self.player)

            self.show_vehicle_telemetry = False
            self.modify_vehicle_physics(self.player)


        # Set up the sensors.
        self.collision_sensor = CollisionSensor(self.player, self.hud)
        self.lane_invasion_sensor = LaneInvasionSensor(self.player, self.hud)
        self.gnss_sensor = GnssSensor(self.player)
        self.imu_sensor = IMUSensor(self.player)
        self.camera_manager = CameraManager(self.player, self.hud, self._gamma)
        self.camera_manager.transform_index = cam_pos_index
        self.camera_manager.set_sensor(cam_index, notify=False)
        actor_type = get_actor_display_name(self.player)
        self.hud.notification(actor_type)

        if self.sync:
            self.world.tick()
        else:
            self.world.wait_for_tick()

    def next_weather(self, reverse=False):
        global telemetry
        self._weather_index += -1 if reverse else 1
        self._weather_index %= len(self._weather_presets)
        preset = self._weather_presets[self._weather_index]
        self.hud.notification('Weather: %s' % preset[1])
        self.player.get_world().set_weather(preset[0])

    def next_map_layer(self, reverse=False):
        self.current_map_layer += -1 if reverse else 1
        self.current_map_layer %= len(self.map_layer_names)
        selected = self.map_layer_names[self.current_map_layer]
        self.hud.notification('LayerMap selected: %s' % selected)

    def load_map_layer(self, unload=False):
        selected = self.map_layer_names[self.current_map_layer]
        if unload:
            self.hud.notification('Unloading map layer: %s' % selected)
            self.world.unload_map_layer(selected)
        else:
            self.hud.notification('Loading map layer: %s' % selected)
            self.world.load_map_layer(selected)

    def toggle_radar(self):
        if self.radar_sensor is None:
            self.radar_sensor = RadarSensor(self.player)
        elif self.radar_sensor.sensor is not None:
            self.radar_sensor.sensor.destroy()
            self.radar_sensor = None

    def modify_vehicle_physics(self, actor):
        #If actor is not a vehicle, we cannot use the physics control
        try:
            physics_control = actor.get_physics_control()
            physics_control.use_sweep_wheel_collision = True
            actor.apply_physics_control(physics_control)
        except Exception:
            pass

    def tick(self, clock):
        self.hud.tick(self, clock)

    def render(self, display):
        self.camera_manager.render(display)
        self.hud.render(display)

    def destroy_sensors(self):
        self.camera_manager.sensor.destroy()
        self.camera_manager.sensor = None
        self.camera_manager.index = None

    def modify_beyond_car_args(self):
        global auto_piloted_y_list,auto_piloted_x_list,ran_autopilot_x,ran_autopilot_y,traffic_manager
        # print(f"grepdbg_steer (x,y) = ({self.player.get_transform().location.x},{self.player.get_transform().location.y}) steer {self.player.get_control().steer}")

        if LESSON_ID == 0:
            velocity = self.player.get_velocity()
            speed = velocity.length()
            to_set = speed * 2 if speed <= 20 else 10
            if self.beyond_car.get_transform().location.x <= -50.0:
                to_set = 0
            set_speed(self.beyond_car,to_set)
        elif LESSON_ID == 1:
            velocity = self.player.get_velocity()
            speed = velocity.length()
            abs_locXspeed = abs(self.player.get_transform().location.x + 89 ) * speed
            # print(f"(grepdbg)abs_locXspeed = {abs_locXspeed}")

            if self.beyond_car.get_transform().location.y <= 24.5:
                set_speed(self.beyond_car, speed * 0)
            elif abs_locXspeed > 500 :
                set_speed(self.beyond_car, speed * 5)
            elif self.player.get_transform().location.x > 10:
                set_speed(self.beyond_car, 50)
            else:
                set_speed(self.beyond_car, 1)
        elif LESSON_ID == 2:

            goal_location = carla.Location(x=215.6, y=-9.9, z=0)  # Set the goal coordinates (change as needed)
            # Get the map and find the closest waypoint to the goal location
            carla_map = self.map
            goal_waypoint = carla_map.get_waypoint(goal_location)

            velocity = self.player.get_velocity()
            speed = velocity.length()
            if ran_autopilot_y is False and speed > 2:
                ran_autopilot_y = True
                for car in auto_piloted_y_list:
                    print(f"setting {car} to be autopiloted")
                    auto_piloted_y_list[car].set_autopilot(True,traffic_manager.get_port())
                    traffic_manager.set_route(auto_piloted_y_list[car], ["Straight","Left","Straight"])


            if ran_autopilot_x is False and self.player.get_transform().location.y >= -75.0:
                self.hud.lesson_notification("At the roundabout continue straight", seconds=2)
                ran_autopilot_x = True
                for car in auto_piloted_x_list:
                    print(f"setting {car} to be autopiloted")
                    auto_piloted_x_list[car].set_autopilot(True,traffic_manager.get_port())
                    traffic_manager.set_route(auto_piloted_x_list[car], ["Left","Straight","Straight","Left"])


    def destroy(self):
        global telemetry
        global auto_piloted_y_list, auto_piloted_x_list, ran_autopilot_x, ran_autopilot_y
        global to_destroy_spawn_list
        if self.radar_sensor is not None:
            self.toggle_radar()
        sensors = [
            self.camera_manager.sensor,
            self.collision_sensor.sensor,
            self.lane_invasion_sensor.sensor,
            self.gnss_sensor.sensor,
            self.imu_sensor.sensor]
        disable_auto_pilot_cars()
        for sensor in sensors:
            if sensor is not None:
                sensor.stop()
                sensor.destroy()
        for key in to_destroy_spawn_list:
            if to_destroy_spawn_list[key] is not None:
                print(f"destroying an obj, name: {key}  typeid = {to_destroy_spawn_list[key].type_id}")
                to_destroy_spawn_list[key].destroy()
        destroy_auto_piloted_cars()

        to_destroy_spawn_list = {}



        self.player = None
        self.beyond_car = None
        reset_telemetry()
        recording_handler.restart()

# ==============================================================================
# -- KeyboardControl -----------------------------------------------------------
# ==============================================================================


class KeyboardControl(object):
    """Class that handles keyboard input."""
    def __init__(self, world, start_in_autopilot):
        self._autopilot_enabled = start_in_autopilot
        self._ackermann_enabled = False
        self._ackermann_reverse = 1
        if isinstance(world.player, carla.Vehicle):
            self._control = carla.VehicleControl()
            self._ackermann_control = carla.VehicleAckermannControl()
            self._lights = carla.VehicleLightState.NONE
            world.player.set_autopilot(self._autopilot_enabled)
            world.player.set_light_state(self._lights)
            set_up_lights(world.player,self._lights)

        elif isinstance(world.player, carla.Walker):
            self._control = carla.WalkerControl()
            self._autopilot_enabled = False
            self._rotation = world.player.get_transform().rotation
        else:
            raise NotImplementedError("Actor type not supported")
        self._steer_cache = 0.0
        world.hud.notification("Press 'H' or '?' for help.", seconds=4.0)

        # initialize steering wheel
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count > 1:
            raise ValueError("Please Connect Just One Joystick")

        self._joystick = pygame.joystick.Joystick(0)
        self._joystick.init()

        self._parser = ConfigParser()
        self._parser.read('wheel_config.ini')

        # To get a list of sections:
        sections = self._parser.sections()
        print("sections", sections,f"joystick count : {joystick_count}")

        self._parser.add_section('Joystick')
        self._parser.set('Joystick', 'steering_wheel', '0')
        self._parser.set('Joystick', 'throttle', '1')
        self._parser.set('Joystick', 'brake', '2')
        self._parser.set('Joystick', 'reverse', '3')
        self._parser.set('Joystick', 'handbrake', '4')

        # Now you can access the options just like before
        self._steer_idx = int(self._parser.get('Joystick', 'steering_wheel'))
        self._throttle_idx = int(self._parser.get('Joystick', 'throttle'))
        self._brake_idx = int(self._parser.get('Joystick', 'brake'))
        self._reverse_idx = int(self._parser.get('Joystick', 'reverse'))
        self._handbrake_idx = int(self._parser.get('Joystick', 'handbrake'))

    def _parse_vehicle_keys(self, keys, milliseconds):
        self._control.throttle = 1.0 if keys[K_UP] or keys[K_w] else 0.0
        steer_increment = 5e-4 * milliseconds
        if keys[K_LEFT] or keys[K_a]:
            self._steer_cache -= steer_increment
        elif keys[K_RIGHT] or keys[K_d]:
            self._steer_cache += steer_increment
        else:
            self._steer_cache = 0.0
        self._steer_cache = min(0.7, max(-0.7, self._steer_cache))
        self._control.steer = round(self._steer_cache, 1)
        self._control.brake = 1.0 if keys[K_DOWN] or keys[K_s] else 0.0
        self._control.hand_brake = keys[K_SPACE]

    def _parse_vehicle_wheel(self):
        numAxes = self._joystick.get_numaxes()
        jsInputs = [float(self._joystick.get_axis(i)) for i in range(numAxes)]
        # print (jsInputs)
        jsButtons = [float(self._joystick.get_button(i)) for i in
                     range(self._joystick.get_numbuttons())]

        # Custom function to map range of inputs [1, -1] to outputs [0, 1] i.e 1 from inputs means nothing is pressed
        # For the steering, it seems fine as it is
        K1 = 1.0  # 0.55
        steerCmd = K1 * math.tan(1.1 * jsInputs[self._steer_idx])

        K2 = 1.6  # 1.6
        throttleCmd = K2 + (2.05 * math.log10(
            -0.7 * jsInputs[self._throttle_idx] + 1.4) - 1.2) / 0.92
        if throttleCmd <= 0:
            throttleCmd = 0
        elif throttleCmd > 1:
            throttleCmd = 1

        brakeCmd = 1.6 + (2.05 * math.log10(
            -0.7 * jsInputs[self._brake_idx] + 1.4) - 1.2) / 0.92
        if brakeCmd <= 0:
            brakeCmd = 0
        elif brakeCmd > 1:
            brakeCmd = 1

        self._control.steer = steerCmd
        self._control.brake = brakeCmd
        self._control.throttle = throttleCmd
        current_lights = self._lights
        if self._control.brake:
            current_lights |= carla.VehicleLightState.Brake
        else:
            current_lights &= ~carla.VehicleLightState.Brake

        if self._control.reverse:
            current_lights |= carla.VehicleLightState.Reverse
        else:  # Remove the Reverse flag
            current_lights &= ~carla.VehicleLightState.Reverse

        self._lights = current_lights


        # toggle = jsButtons[self._reverse_idx]

        self._control.hand_brake = bool(jsButtons[self._handbrake_idx])

    def _parse_walker_keys(self, keys, milliseconds):
        self._control.speed = 0.0
        if keys[K_DOWN] or keys[K_s]:
            self._control.speed = 0.0
        if keys[K_LEFT] or keys[K_a]:
            self._control.speed = .01
            self._rotation.yaw -= 0.08 * milliseconds
        if keys[K_RIGHT] or keys[K_d]:
            self._control.speed = .01
            self._rotation.yaw += 0.08 * milliseconds
        if keys[K_UP] or keys[K_w]:
            self._control.speed = 5.556 if pygame.key.get_mods() & KMOD_SHIFT else 2.778
        self._control.jump = keys[K_SPACE]
        self._rotation.yaw = round(self._rotation.yaw, 1)
        self._control.direction = self._rotation.get_forward_vector()

    @staticmethod
    def _is_quit_shortcut(key):
        return (key == K_ESCAPE) or (key == K_q and pygame.key.get_mods() & KMOD_CTRL)

    def parse_events(self, client, world, clock, sync_mode):
        if isinstance(self._control, carla.VehicleControl):
            current_lights = self._lights
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            elif event.type == pygame.JOYBUTTONDOWN:
                if DEBUG_EN : print(f"event buttom : {event.button}")
                if event.button == 0:
                    world.restart()
                elif event.button == 1:
                    tk_thread = threading.Thread(target=show_telemetry, args=(world, client,))
                    tk_thread.daemon = True  # Ensure Tkinter window closes when the program exits
                    tk_thread.start()
                elif event.button == 2:
                    world.camera_manager.toggle_camera()
                elif event.button == 3:
                    self._control.gear = 1 if self._control.reverse else -1
                elif event.button == self._reverse_idx:
                    self._control.gear = 1 if self._control.reverse else -1
                elif event.button == 23:
                    world.camera_manager.next_sensor()


                if event.button == 4:
                    blinker_is_on = current_lights & carla.VehicleLightState.RightBlinker
                    if blinker_is_on:
                        current_lights &= ~carla.VehicleLightState.RightBlinker
                    else:
                        current_lights ^= carla.VehicleLightState.RightBlinker
                        current_lights &= ~carla.VehicleLightState.LeftBlinker
                elif event.button == 5:
                    blinker_is_on = current_lights & carla.VehicleLightState.LeftBlinker
                    if blinker_is_on:
                        current_lights &= ~carla.VehicleLightState.LeftBlinker
                    else:
                        current_lights ^= carla.VehicleLightState.LeftBlinker
                        current_lights &= ~carla.VehicleLightState.RightBlinker

                if current_lights != self._lights:
                    self._lights = current_lights
                    world.player.set_light_state(carla.VehicleLightState(self._lights))

            elif event.type == pygame.KEYUP:
                if self._is_quit_shortcut(event.key):
                    return True
                elif event.key == K_BACKSPACE:
                    print("grepdbg K_BACKSPACE !!!!!!!!!!!!!!!")
                    if self._autopilot_enabled:
                        world.player.set_autopilot(False)
                        world.restart()
                        world.player.set_autopilot(True)
                    else:
                        world.restart()
                elif event.key == K_F1:
                    world.hud.toggle_info()
                elif event.key == K_v and pygame.key.get_mods() & KMOD_SHIFT:
                    world.next_map_layer(reverse=True)
                elif event.key == K_v:
                    world.next_map_layer()
                elif event.key == K_b and pygame.key.get_mods() & KMOD_SHIFT:
                    world.load_map_layer(unload=True)
                elif event.key == K_b:
                    world.load_map_layer()
                elif event.key == K_h or (event.key == K_SLASH and pygame.key.get_mods() & KMOD_SHIFT):
                    world.hud.help.toggle()
                elif event.key == K_TAB:
                    world.camera_manager.toggle_camera()
                elif event.key == K_c and pygame.key.get_mods() & KMOD_SHIFT:
                    world.next_weather(reverse=True)
                elif event.key == K_c:
                    world.next_weather()
                elif event.key == K_g:
                    world.toggle_radar()
                elif event.key == K_BACKQUOTE:
                    world.camera_manager.next_sensor()
                elif event.key == K_n:
                    world.camera_manager.next_sensor()
                elif event.key == K_w and (pygame.key.get_mods() & KMOD_CTRL):
                    if world.constant_velocity_enabled:
                        world.player.disable_constant_velocity()
                        world.constant_velocity_enabled = False
                        world.hud.notification("Disabled Constant Velocity Mode")
                    else:
                        world.player.enable_constant_velocity(carla.Vector3D(17, 0, 0))
                        world.constant_velocity_enabled = True
                        world.hud.notification("Enabled Constant Velocity Mode at 60 km/h")
                elif event.key == K_o:
                    try:
                        if world.doors_are_open:
                            world.hud.notification("Closing Doors")
                            world.doors_are_open = False
                            world.player.close_door(carla.VehicleDoor.All)
                        else:
                            world.hud.notification("Opening doors")
                            world.doors_are_open = True
                            world.player.open_door(carla.VehicleDoor.All)
                    except Exception:
                        pass
                elif event.key == K_t:
                    tk_thread = threading.Thread(target=show_telemetry, args=(world,client,))
                    tk_thread.daemon = True  # Ensure Tkinter window closes when the program exits
                    tk_thread.start()
                    # if world.show_vehicle_telemetry:
                    #     world.player.show_debug_telemetry(False)
                    #     world.show_vehicle_telemetry = False
                    #     world.hud.notification("Disabled Vehicle Telemetry")
                    # else:
                    #     try:
                    #         world.player.show_debug_telemetry(True)
                    #         world.show_vehicle_telemetry = True
                    #         world.hud.notification("Enabled Vehicle Telemetry")
                    #     except Exception:
                    #         pass
                elif event.key > K_0 and event.key <= K_9:
                    index_ctrl = 0
                    if pygame.key.get_mods() & KMOD_CTRL:
                        index_ctrl = 9
                    world.camera_manager.set_sensor(event.key - 1 - K_0 + index_ctrl)
                elif event.key == K_r and not (pygame.key.get_mods() & KMOD_CTRL):
                    world.camera_manager.toggle_recording()
                elif event.key == K_r and (pygame.key.get_mods() & KMOD_CTRL):
                    if (world.recording_enabled):
                        client.stop_recorder()
                        world.recording_enabled = False
                        world.hud.notification("Recorder is OFF")
                    else:
                        client.start_recorder("manual_recording.rec")
                        world.recording_enabled = True
                        world.hud.notification("Recorder is ON")
                elif event.key == K_p and (pygame.key.get_mods() & KMOD_CTRL):
                    # stop recorder
                    client.stop_recorder()
                    world.recording_enabled = False
                    # work around to fix camera at start of replaying
                    current_index = world.camera_manager.index
                    world.destroy_sensors()
                    # disable autopilot
                    self._autopilot_enabled = False
                    world.player.set_autopilot(self._autopilot_enabled)
                    world.hud.notification("Replaying file 'manual_recording.rec'")
                    # replayer
                    client.replay_file("manual_recording.rec", world.recording_start, 0, 0)
                    world.camera_manager.set_sensor(current_index)
                elif event.key == K_MINUS and (pygame.key.get_mods() & KMOD_CTRL):
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        world.recording_start -= 10
                    else:
                        world.recording_start -= 1
                    world.hud.notification("Recording start time is %d" % (world.recording_start))
                elif event.key == K_EQUALS and (pygame.key.get_mods() & KMOD_CTRL):
                    if pygame.key.get_mods() & KMOD_SHIFT:
                        world.recording_start += 10
                    else:
                        world.recording_start += 1
                    world.hud.notification("Recording start time is %d" % (world.recording_start))
                if isinstance(self._control, carla.VehicleControl):
                    if event.key == K_f:
                        # Toggle ackermann controller
                        self._ackermann_enabled = not self._ackermann_enabled
                        world.hud.show_ackermann_info(self._ackermann_enabled)
                        world.hud.notification("Ackermann Controller %s" %
                                               ("Enabled" if self._ackermann_enabled else "Disabled"))
                    if event.key == K_q:
                        if not self._ackermann_enabled:
                            self._control.gear = 1 if self._control.reverse else -1
                        else:
                            self._ackermann_reverse *= -1
                            # Reset ackermann control
                            self._ackermann_control = carla.VehicleAckermannControl()
                    elif event.key == K_m:
                        self._control.manual_gear_shift = not self._control.manual_gear_shift
                        self._control.gear = world.player.get_control().gear
                        world.hud.notification('%s Transmission' %
                                               ('Manual' if self._control.manual_gear_shift else 'Automatic'))
                    elif self._control.manual_gear_shift and event.key == K_COMMA:
                        self._control.gear = max(-1, self._control.gear - 1)
                    elif self._control.manual_gear_shift and event.key == K_PERIOD:
                        self._control.gear = self._control.gear + 1
                    elif event.key == K_p and not pygame.key.get_mods() & KMOD_CTRL:
                        if not self._autopilot_enabled and not sync_mode:
                            print("WARNING: You are currently in asynchronous mode and could "
                                  "experience some issues with the traffic simulation")
                        self._autopilot_enabled = not self._autopilot_enabled
                        world.player.set_autopilot(self._autopilot_enabled)
                        world.hud.notification(
                            'Autopilot %s' % ('On' if self._autopilot_enabled else 'Off'))
                    elif event.key == K_l and pygame.key.get_mods() & KMOD_CTRL:
                        current_lights ^= carla.VehicleLightState.Special1
                    elif event.key == K_l and pygame.key.get_mods() & KMOD_SHIFT:
                        current_lights ^= carla.VehicleLightState.HighBeam
                    elif event.key == K_l:
                        # Use 'L' key to switch between lights:
                        # closed -> position -> low beam -> fog
                        if not self._lights & carla.VehicleLightState.Position:
                            world.hud.notification("Position lights")
                            current_lights |= carla.VehicleLightState.Position
                        else:
                            world.hud.notification("Low beam lights")
                            current_lights |= carla.VehicleLightState.LowBeam
                        if self._lights & carla.VehicleLightState.LowBeam:
                            world.hud.notification("Fog lights")
                            current_lights |= carla.VehicleLightState.Fog
                        if self._lights & carla.VehicleLightState.Fog:
                            world.hud.notification("Lights off")
                            current_lights ^= carla.VehicleLightState.Position
                            current_lights ^= carla.VehicleLightState.LowBeam
                            current_lights ^= carla.VehicleLightState.Fog
                    elif event.key == K_i:
                        current_lights ^= carla.VehicleLightState.Interior
                    elif event.key == K_z:
                        current_lights ^= carla.VehicleLightState.LeftBlinker
                    elif event.key == K_x:
                        current_lights ^= carla.VehicleLightState.RightBlinker

            if not self._autopilot_enabled:
                if isinstance(self._control, carla.VehicleControl):
                    current_lights = self._lights
                    self._parse_vehicle_keys(pygame.key.get_pressed(), clock.get_time())
                    self._parse_vehicle_wheel()
                    self._control.reverse = self._control.gear < 0
                elif isinstance(self._control, carla.WalkerControl):
                    self._parse_walker_keys(pygame.key.get_pressed(), clock.get_time())
                world.player.apply_control(self._control)
                if self._lights != current_lights:
                    world.player.set_light_state(carla.VehicleLightState(self._lights))




# ==============================================================================
# -- HUD -----------------------------------------------------------------------
# ==============================================================================


class HUD(object):
    def __init__(self, width, height):
        self.dim = (width, height)
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        font_name = 'courier' if os.name == 'nt' else 'mono'
        fonts = [x for x in pygame.font.get_fonts() if font_name in x]
        default_font = 'ubuntumono'
        mono = default_font if default_font in fonts else fonts[0]
        mono = pygame.font.match_font(mono)
        self._font_mono = pygame.font.Font(mono, 12 if os.name == 'nt' else 14)
        if DEBUG_EN: print(f"width = {width}, height = {height}")
        self._notifications = FadingText(font, (width, 40), (0, height - 40))
        self.lesson_notifications = FadingText(font, (width // 2, 40), (200, (height - 40) // 2))
        self.help = HelpText(pygame.font.Font(mono, 16), width, height)
        self.server_fps = 0
        self.frame = 0
        self.simulation_time = 0
        self._show_info = True
        self._info_text = []
        self._server_clock = pygame.time.Clock()

        self._show_ackermann_info = False
        self._ackermann_control = carla.VehicleAckermannControl()

    def on_world_tick(self, timestamp):
        self._server_clock.tick()
        self.server_fps = self._server_clock.get_fps()
        self.frame = timestamp.frame
        self.simulation_time = timestamp.elapsed_seconds

    def tick(self, world, clock):
        self._notifications.tick(world, clock)
        self.lesson_notifications.tick(world, clock)
        if not self._show_info:
            return
        t = world.player.get_transform()
        v = world.player.get_velocity()
        c = world.player.get_control()
        compass = world.imu_sensor.compass
        heading = 'N' if compass > 270.5 or compass < 89.5 else ''
        heading += 'S' if 90.5 < compass < 269.5 else ''
        heading += 'E' if 0.5 < compass < 179.5 else ''
        heading += 'W' if 180.5 < compass < 359.5 else ''
        colhist = world.collision_sensor.get_collision_history()
        collision = [colhist[x + self.frame - 200] for x in range(0, 200)]
        max_col = max(1.0, max(collision))
        collision = [x / max_col for x in collision]
        vehicles = world.world.get_actors().filter('vehicle.*')
        speed = 3.6 * math.sqrt(v.x**2 + v.y**2 + v.z**2)
        if (len(telemetry["speed"]) == 0 and speed > 0) or (len(telemetry["speed"]) > 0 and abs(speed - telemetry["speed"][-1]["curr_speed"]) > 3):
            telemetry["speed"].append({"frame":self.frame,"curr_speed":speed})

        # if len(telemetry["locations"]) == 0 or dist(telemetry["locations"][-1],(t.location.x, t.location.y)):
        #     telemetry["locations"].append((t.location.x, t.location.y))

        update_Speed_info(speed)
        self._info_text = [
            'Server:  % 16.0f FPS' % self.server_fps,
            'Client:  % 16.0f FPS' % clock.get_fps(),
            '',
            'Vehicle: % 20s' % get_actor_display_name(world.player, truncate=20),
            'Map:     % 20s' % world.map.name.split('/')[-1],
            'Simulation time: % 12s' % datetime.timedelta(seconds=int(self.simulation_time)),
            '',
            'Speed:   % 15.0f km/h' % speed,
            u'Compass:% 17.0f\N{DEGREE SIGN} % 2s' % (compass, heading),
            'Accelero: (%5.1f,%5.1f,%5.1f)' % (world.imu_sensor.accelerometer),
            'Gyroscop: (%5.1f,%5.1f,%5.1f)' % (world.imu_sensor.gyroscope),
            'Location:% 20s' % ('(% 5.1f, % 5.1f)' % (t.location.x, t.location.y)),
            'GNSS:% 24s' % ('(% 2.6f, % 3.6f)' % (world.gnss_sensor.lat, world.gnss_sensor.lon)),
            'Height:  % 18.0f m' % t.location.z,
            '']

        if isinstance(c, carla.VehicleControl):
            self._info_text += [
                ('Throttle:', c.throttle, 0.0, 1.0),
                ('Steer:', c.steer, -1.0, 1.0),
                ('Brake:', c.brake, 0.0, 1.0),
                ('Reverse:', c.reverse),
                ('Hand brake:', c.hand_brake),
                ('Manual:', c.manual_gear_shift),
                'Gear:        %s' % {-1: 'R', 0: 'N'}.get(c.gear, c.gear)]
            if self._show_ackermann_info:
                self._info_text += [
                    '',
                    'Ackermann Controller:',
                    '  Target speed: % 8.0f km/h' % (3.6*self._ackermann_control.speed),
                ]
        elif isinstance(c, carla.WalkerControl):
            self._info_text += [
                ('Speed:', c.speed, 0.0, 5.556),
                ('Jump:', c.jump)]
        self._info_text += [
            '',
            'Collision:',
            collision,
            '',
            'Number of vehicles: % 8d' % len(vehicles)]
        if len(vehicles) > 1:
            self._info_text += ['Nearby vehicles:']
            distance = lambda l: math.sqrt((l.x - t.location.x)**2 + (l.y - t.location.y)**2 + (l.z - t.location.z)**2)
            vehicles = [(distance(x.get_location()), x) for x in vehicles if x.id != world.player.id]
            for d, vehicle in sorted(vehicles, key=lambda vehicles: vehicles[0]):
                if d > 200.0:
                    break
                vehicle_type = get_actor_display_name(vehicle, truncate=22)
                self._info_text.append('% 4dm %s' % (d, vehicle_type))

    def show_ackermann_info(self, enabled):
        self._show_ackermann_info = enabled

    def update_ackermann_control(self, ackermann_control):
        self._ackermann_control = ackermann_control

    def toggle_info(self):
        self._show_info = not self._show_info

    def notification(self, text, seconds=2.0):
        self._notifications.set_text(text, seconds=seconds)

    def lesson_notification(self, text, seconds=2.0):
        self.lesson_notifications.set_text(text, seconds=seconds)

    def error(self, text):
        self._notifications.set_text('Error: %s' % text, (255, 0, 0))

    def render(self, display):
        if self._show_info:
            info_surface = pygame.Surface((220, self.dim[1]))
            info_surface.set_alpha(100)
            display.blit(info_surface, (0, 0))
            v_offset = 4
            bar_h_offset = 100
            bar_width = 106
            for item in self._info_text:
                if v_offset + 18 > self.dim[1]:
                    break
                if isinstance(item, list):
                    if len(item) > 1:
                        points = [(x + 8, v_offset + 8 + (1.0 - y) * 30) for x, y in enumerate(item)]
                        pygame.draw.lines(display, (255, 136, 0), False, points, 2)
                    item = None
                    v_offset += 18
                elif isinstance(item, tuple):
                    if isinstance(item[1], bool):
                        rect = pygame.Rect((bar_h_offset, v_offset + 8), (6, 6))
                        pygame.draw.rect(display, (255, 255, 255), rect, 0 if item[1] else 1)
                    else:
                        rect_border = pygame.Rect((bar_h_offset, v_offset + 8), (bar_width, 6))
                        pygame.draw.rect(display, (255, 255, 255), rect_border, 1)
                        f = (item[1] - item[2]) / (item[3] - item[2])
                        if item[2] < 0.0:
                            rect = pygame.Rect((bar_h_offset + f * (bar_width - 6), v_offset + 8), (6, 6))
                        else:
                            rect = pygame.Rect((bar_h_offset, v_offset + 8), (f * bar_width, 6))
                        pygame.draw.rect(display, (255, 255, 255), rect)
                    item = item[0]
                if item:  # At this point has to be a str.
                    surface = self._font_mono.render(item, True, (255, 255, 255))
                    display.blit(surface, (8, v_offset))
                v_offset += 18
        self._notifications.render(display)
        self.lesson_notifications.render(display)
        self.help.render(display)


# ==============================================================================
# -- FadingText ----------------------------------------------------------------
# ==============================================================================


class FadingText(object):
    def __init__(self, font, dim, pos):
        self.font = font
        self.dim = dim
        self.pos = pos
        self.seconds_left = 0
        self.surface = pygame.Surface(self.dim)

    def set_text(self, text, color=(255, 255, 255), seconds=2.0):
        text_texture = self.font.render(text, True, color)
        self.surface = pygame.Surface(self.dim)
        self.seconds_left = seconds
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(text_texture, (10, 11))

    def tick(self, _, clock):
        delta_seconds = 1e-3 * clock.get_time()
        self.seconds_left = max(0.0, self.seconds_left - delta_seconds)
        self.surface.set_alpha(500.0 * self.seconds_left)

    def render(self, display):
        display.blit(self.surface, self.pos)


# ==============================================================================
# -- HelpText ------------------------------------------------------------------
# ==============================================================================


class HelpText(object):
    """Helper class to handle text output using pygame"""
    def __init__(self, font, width, height):
        lines = __doc__.split('\n')
        self.font = font
        self.line_space = 18
        self.dim = (780, len(lines) * self.line_space + 12)
        self.pos = (0.5 * width - 0.5 * self.dim[0], 0.5 * height - 0.5 * self.dim[1])
        self.seconds_left = 0
        self.surface = pygame.Surface(self.dim)
        self.surface.fill((0, 0, 0, 0))
        for n, line in enumerate(lines):
            text_texture = self.font.render(line, True, (255, 255, 255))
            self.surface.blit(text_texture, (22, n * self.line_space))
            self._render = False
        self.surface.set_alpha(220)

    def toggle(self):
        self._render = not self._render

    def render(self, display):
        if self._render:
            display.blit(self.surface, self.pos)


# ==============================================================================
# -- CollisionSensor -----------------------------------------------------------
# ==============================================================================


class CollisionSensor(object):
    def __init__(self, parent_actor, hud):
        self.sensor = None
        self.history = []
        self._parent = parent_actor
        self.hud = hud
        self.prev_collision = None
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.collision')
        self.sensor = world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: CollisionSensor._on_collision(weak_self, event))

    def get_collision_history(self):
        history = collections.defaultdict(int)
        for frame, intensity in self.history:
            history[frame] += intensity
        return history

    @staticmethod
    def _on_collision(weak_self, event):
        self = weak_self()
        if not self:
            return
        actor_type = get_actor_display_name(event.other_actor)
        self.hud.notification('Collision with %r' % actor_type)
        if f"Collision with {actor_type}" not in telemetry:
            telemetry[f"Collision with {actor_type}"] = 0
        telemetry[f"Collision with {actor_type}"] += 1
        telemetry[f"collisions"].append({"frame": event.frame})


        impulse = event.normal_impulse
        intensity = math.sqrt(impulse.x**2 + impulse.y**2 + impulse.z**2)
        self.history.append((event.frame, intensity))
        if len(self.history) > 4000:
            self.history.pop(0)


# ==============================================================================
# -- LaneInvasionSensor --------------------------------------------------------
# ==============================================================================


class LaneInvasionSensor(object):
    def __init__(self, parent_actor, hud):
        self.sensor = None
        self.prev_cross = None
        # If the spawn object is not a vehicle, we cannot use the Lane Invasion Sensor
        if parent_actor.type_id.startswith("vehicle."):
            self._parent = parent_actor
            self.hud = hud
            world = self._parent.get_world()
            bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
            self.sensor = world.spawn_actor(bp, carla.Transform(), attach_to=self._parent)
            # We need to pass the lambda a weak reference to self to avoid circular
            # reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(lambda event: LaneInvasionSensor._on_invasion(weak_self, event))

    @staticmethod
    def _on_invasion(weak_self, event):
        self = weak_self()
        if not self:
            return
        lane_types = set(x.type for x in event.crossed_lane_markings)
        text = ['%r' % str(x).split()[-1] for x in lane_types]
        self.hud.notification('Crossed line %s' % ' and '.join(text))
        curr_cross = 'Crossed line %s' % ' and '.join(text)
        if curr_cross not in telemetry:
            telemetry[curr_cross] = 0
        telemetry[curr_cross] += 1


# ==============================================================================
# -- GnssSensor ----------------------------------------------------------------
# ==============================================================================


class GnssSensor(object):
    def __init__(self, parent_actor):
        self.sensor = None
        self._parent = parent_actor
        self.lat = 0.0
        self.lon = 0.0
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.gnss')
        self.sensor = world.spawn_actor(bp, carla.Transform(carla.Location(x=1.0, z=2.8)), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: GnssSensor._on_gnss_event(weak_self, event))

    @staticmethod
    def _on_gnss_event(weak_self, event):
        self = weak_self()
        if not self:
            return
        self.lat = event.latitude
        self.lon = event.longitude


# ==============================================================================
# -- IMUSensor -----------------------------------------------------------------
# ==============================================================================


class IMUSensor(object):
    def __init__(self, parent_actor):
        self.sensor = None
        self._parent = parent_actor
        self.accelerometer = (0.0, 0.0, 0.0)
        self.gyroscope = (0.0, 0.0, 0.0)
        self.compass = 0.0
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.imu')
        self.sensor = world.spawn_actor(
            bp, carla.Transform(), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda sensor_data: IMUSensor._IMU_callback(weak_self, sensor_data))

    @staticmethod
    def _IMU_callback(weak_self, sensor_data):
        self = weak_self()
        if not self:
            return
        limits = (-99.9, 99.9)
        self.accelerometer = (
            max(limits[0], min(limits[1], sensor_data.accelerometer.x)),
            max(limits[0], min(limits[1], sensor_data.accelerometer.y)),
            max(limits[0], min(limits[1], sensor_data.accelerometer.z)))
        self.gyroscope = (
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.x))),
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.y))),
            max(limits[0], min(limits[1], math.degrees(sensor_data.gyroscope.z))))
        self.compass = math.degrees(sensor_data.compass)


# ==============================================================================
# -- RadarSensor ---------------------------------------------------------------
# ==============================================================================


class RadarSensor(object):
    def __init__(self, parent_actor):
        self.sensor = None
        self._parent = parent_actor
        bound_x = 0.5 + self._parent.bounding_box.extent.x
        bound_y = 0.5 + self._parent.bounding_box.extent.y
        bound_z = 0.5 + self._parent.bounding_box.extent.z

        self.velocity_range = 7.5 # m/s
        world = self._parent.get_world()
        self.debug = world.debug
        bp = world.get_blueprint_library().find('sensor.other.radar')
        bp.set_attribute('horizontal_fov', str(35))
        bp.set_attribute('vertical_fov', str(20))
        self.sensor = world.spawn_actor(
            bp,
            carla.Transform(
                carla.Location(x=bound_x + 0.05, z=bound_z+0.05),
                carla.Rotation(pitch=5)),
            attach_to=self._parent)
        # We need a weak reference to self to avoid circular reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(
            lambda radar_data: RadarSensor._Radar_callback(weak_self, radar_data))

    @staticmethod
    def _Radar_callback(weak_self, radar_data):
        self = weak_self()
        if not self:
            return
        # To get a numpy [[vel, altitude, azimuth, depth],...[,,,]]:
        # points = np.frombuffer(radar_data.raw_data, dtype=np.dtype('f4'))
        # points = np.reshape(points, (len(radar_data), 4))

        current_rot = radar_data.transform.rotation
        for detect in radar_data:
            azi = math.degrees(detect.azimuth)
            alt = math.degrees(detect.altitude)
            # The 0.25 adjusts a bit the distance so the dots can
            # be properly seen
            fw_vec = carla.Vector3D(x=detect.depth - 0.25)
            carla.Transform(
                carla.Location(),
                carla.Rotation(
                    pitch=current_rot.pitch + alt,
                    yaw=current_rot.yaw + azi,
                    roll=current_rot.roll)).transform(fw_vec)

            def clamp(min_v, max_v, value):
                return max(min_v, min(value, max_v))

            norm_velocity = detect.velocity / self.velocity_range # range [-1, 1]
            r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
            g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
            b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
            self.debug.draw_point(
                radar_data.transform.location + fw_vec,
                size=0.075,
                life_time=0.06,
                persistent_lines=False,
                color=carla.Color(r, g, b))

# ==============================================================================
# -- CameraManager -------------------------------------------------------------
# ==============================================================================


class CameraManager(object):
    def __init__(self, parent_actor, hud, gamma_correction):
        self.sensor = None
        self.surface = None
        self._parent = parent_actor
        self.hud = hud
        self.recording = False
        bound_x = 0.5 + self._parent.bounding_box.extent.x
        bound_y = 0.5 + self._parent.bounding_box.extent.y
        bound_z = 0.5 + self._parent.bounding_box.extent.z
        Attachment = carla.AttachmentType

        if not self._parent.type_id.startswith("walker.pedestrian"):
            self._camera_transforms = [
                (carla.Transform(carla.Location(x=-2.0*bound_x, y=+0.0*bound_y, z=2.0*bound_z), carla.Rotation(pitch=8.0)), Attachment.SpringArmGhost),
                (carla.Transform(carla.Location(x=+0.8*bound_x, y=+0.0*bound_y, z=1.3*bound_z)), Attachment.Rigid),
                (carla.Transform(carla.Location(x=+1.9*bound_x, y=+1.0*bound_y, z=1.2*bound_z)), Attachment.SpringArmGhost),
                (carla.Transform(carla.Location(x=-2.8*bound_x, y=+0.0*bound_y, z=4.6*bound_z), carla.Rotation(pitch=6.0)), Attachment.SpringArmGhost),
                (carla.Transform(carla.Location(x=-1.0, y=-1.0*bound_y, z=0.4*bound_z)), Attachment.Rigid)]
        else:
            self._camera_transforms = [
                (carla.Transform(carla.Location(x=-2.5, z=0.0), carla.Rotation(pitch=-8.0)), Attachment.SpringArmGhost),
                (carla.Transform(carla.Location(x=1.6, z=1.7)), Attachment.Rigid),
                (carla.Transform(carla.Location(x=2.5, y=0.5, z=0.0), carla.Rotation(pitch=-8.0)), Attachment.SpringArmGhost),
                (carla.Transform(carla.Location(x=-4.0, z=2.0), carla.Rotation(pitch=6.0)), Attachment.SpringArmGhost),
                (carla.Transform(carla.Location(x=0, y=-2.5, z=-0.0), carla.Rotation(yaw=90.0)), Attachment.Rigid)]

        self.transform_index = 1
        self.sensors = [
            ['sensor.camera.rgb', cc.Raw, 'Camera RGB', {}],
            ['sensor.camera.depth', cc.Raw, 'Camera Depth (Raw)', {}],
            ['sensor.camera.depth', cc.Depth, 'Camera Depth (Gray Scale)', {}],
            ['sensor.camera.depth', cc.LogarithmicDepth, 'Camera Depth (Logarithmic Gray Scale)', {}],
            ['sensor.camera.semantic_segmentation', cc.Raw, 'Camera Semantic Segmentation (Raw)', {}],
            ['sensor.camera.semantic_segmentation', cc.CityScapesPalette, 'Camera Semantic Segmentation (CityScapes Palette)', {}],
            ['sensor.camera.instance_segmentation', cc.CityScapesPalette, 'Camera Instance Segmentation (CityScapes Palette)', {}],
            ['sensor.camera.instance_segmentation', cc.Raw, 'Camera Instance Segmentation (Raw)', {}],
            ['sensor.lidar.ray_cast', None, 'Lidar (Ray-Cast)', {'range': '50'}],
            ['sensor.camera.dvs', cc.Raw, 'Dynamic Vision Sensor', {}],
            ['sensor.camera.rgb', cc.Raw, 'Camera RGB Distorted',
                {'lens_circle_multiplier': '3.0',
                'lens_circle_falloff': '3.0',
                'chromatic_aberration_intensity': '0.5',
                'chromatic_aberration_offset': '0'}],
            ['sensor.camera.optical_flow', cc.Raw, 'Optical Flow', {}],
            ['sensor.camera.normals', cc.Raw, 'Camera Normals', {}],
        ]
        world = self._parent.get_world()
        bp_library = world.get_blueprint_library()
        for item in self.sensors:
            bp = bp_library.find(item[0])
            if item[0].startswith('sensor.camera'):
                bp.set_attribute('image_size_x', str(hud.dim[0]))
                bp.set_attribute('image_size_y', str(hud.dim[1]))
                if bp.has_attribute('gamma'):
                    bp.set_attribute('gamma', str(gamma_correction))
                for attr_name, attr_value in item[3].items():
                    bp.set_attribute(attr_name, attr_value)
            elif item[0].startswith('sensor.lidar'):
                self.lidar_range = 50

                for attr_name, attr_value in item[3].items():
                    bp.set_attribute(attr_name, attr_value)
                    if attr_name == 'range':
                        self.lidar_range = float(attr_value)

            item.append(bp)
        self.index = None

    def toggle_camera(self):
        self.transform_index = (self.transform_index + 1) % len(self._camera_transforms)
        self.set_sensor(self.index, notify=False, force_respawn=True)

    def set_sensor(self, index, notify=True, force_respawn=False):
        index = index % len(self.sensors)
        needs_respawn = True if self.index is None else \
            (force_respawn or (self.sensors[index][2] != self.sensors[self.index][2]))
        if needs_respawn:
            if self.sensor is not None:
                self.sensor.destroy()
                self.surface = None
            self.sensor = self._parent.get_world().spawn_actor(
                self.sensors[index][-1],
                self._camera_transforms[self.transform_index][0],
                attach_to=self._parent,
                attachment_type=self._camera_transforms[self.transform_index][1])
            # We need to pass the lambda a weak reference to self to avoid
            # circular reference.
            weak_self = weakref.ref(self)
            self.sensor.listen(lambda image: CameraManager._parse_image(weak_self, image))
        if notify:
            self.hud.notification(self.sensors[index][2])
        self.index = index

    def next_sensor(self):
        self.set_sensor(self.index + 1)

    def toggle_recording(self):
        self.recording = not self.recording
        self.hud.notification('Recording %s' % ('On' if self.recording else 'Off'))

    def render(self, display):
        if self.surface is not None:
            display.blit(self.surface, (0, 0))

    @staticmethod
    def _parse_image(weak_self, image):
        self = weak_self()
        if not self:
            return
        if self.sensors[self.index][0].startswith('sensor.lidar'):
            points = np.frombuffer(image.raw_data, dtype=np.dtype('f4'))
            points = np.reshape(points, (int(points.shape[0] / 4), 4))
            lidar_data = np.array(points[:, :2])
            lidar_data *= min(self.hud.dim) / (2.0 * self.lidar_range)
            lidar_data += (0.5 * self.hud.dim[0], 0.5 * self.hud.dim[1])
            lidar_data = np.fabs(lidar_data)  # pylint: disable=E1111
            lidar_data = lidar_data.astype(np.int32)
            lidar_data = np.reshape(lidar_data, (-1, 2))
            lidar_img_size = (self.hud.dim[0], self.hud.dim[1], 3)
            lidar_img = np.zeros((lidar_img_size), dtype=np.uint8)
            lidar_img[tuple(lidar_data.T)] = (255, 255, 255)
            self.surface = pygame.surfarray.make_surface(lidar_img)
        elif self.sensors[self.index][0].startswith('sensor.camera.dvs'):
            # Example of converting the raw_data from a carla.DVSEventArray
            # sensor into a NumPy array and using it as an image
            dvs_events = np.frombuffer(image.raw_data, dtype=np.dtype([
                ('x', np.uint16), ('y', np.uint16), ('t', np.int64), ('pol', np.bool)]))
            dvs_img = np.zeros((image.height, image.width, 3), dtype=np.uint8)
            # Blue is positive, red is negative
            dvs_img[dvs_events[:]['y'], dvs_events[:]['x'], dvs_events[:]['pol'] * 2] = 255
            self.surface = pygame.surfarray.make_surface(dvs_img.swapaxes(0, 1))
        elif self.sensors[self.index][0].startswith('sensor.camera.optical_flow'):
            image = image.get_color_coded_flow()
            array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        else:
            image.convert(self.sensors[self.index][1])
            array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            array = array[:, :, ::-1]
            self.surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))
        if self.recording:
            image.save_to_disk('_out/%08d' % image.frame)


# ==============================================================================
# -- game_loop() ---------------------------------------------------------------
# ==============================================================================

import inputs
def game_loop(args):
    global start_flag,traffic_manager

    pygame.init()
    pygame.font.init()
    world = None
    original_settings = None

    try:
        client = carla.Client(args.host, args.port)
        client.set_timeout(2000.0)
        if not (LESSON_ID == 0 or LESSON_ID == 1):
            client.load_world("Town03")#Town10HD
        else:
            client.load_world("Town10HD_Opt")
            # client.load_world("Town10HD_Opt")

        if LESSON_ID == 2:
            traffic_manager = client.get_trafficmanager(8000)  # Port for Traffic Manager
            traffic_manager.set_global_distance_to_leading_vehicle(2.0)
            print(f"SET THE TRAFFIC MANAGER ! {traffic_manager}")


        sim_world = client.get_world()
        if args.sync:
            original_settings = sim_world.get_settings()
            settings = sim_world.get_settings()
            if not settings.synchronous_mode:
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 0.05
            sim_world.apply_settings(settings)

            _traffic_manager = client.get_trafficmanager()
            _traffic_manager.set_synchronous_mode(True)

        if args.autopilot and not sim_world.get_settings().synchronous_mode:
            print("WARNING: You are currently in asynchronous mode and could "
                  "experience some issues with the traffic simulation")

        display = pygame.display.set_mode(
            (args.width, args.height),
            pygame.HWSURFACE | pygame.DOUBLEBUF)
        display.fill((0,0,0))
        pygame.display.flip()

        hud = HUD(args.width, args.height)
        world = World(sim_world, hud, args)
        weather_info = world._weather_presets[world._weather_index][0]
        telemetry["Weather Info"] = f'precipitation : {int(weather_info.precipitation)}%, fog_density: {weather_info.fog_density}%'

        controller = KeyboardControl(world, args.autopilot)

        if args.sync:
            sim_world.tick()
        else:
            sim_world.wait_for_tick()

        clock = pygame.time.Clock()

        while True:
            if args.sync:
                sim_world.tick()
            clock.tick_busy_loop(60)
            if controller.parse_events(client, world, clock, args.sync):
                return
            start_flag = True
            world.modify_beyond_car_args()
            recording_handler.handle_recording(client,world)
            world.tick(clock)
            world.render(display)
            pygame.display.flip()


    finally:
        print("grepdbg FINALLY !!!!!!!!!!!!!!!")
        if original_settings:
            sim_world.apply_settings(original_settings)

        if (world and world.recording_enabled):
            client.stop_recorder()
        if world is not None:
            world.destroy()


        pygame.quit()


# ==============================================================================
# -- main() --------------------------------------------------------------------
# ==============================================================================


def main():
    argparser = argparse.ArgumentParser(
        description='CARLA Manual Control Client')
    argparser.add_argument(
        '-v', '--verbose',
        action='store_true',
        dest='debug',
        help='print debug information')
    argparser.add_argument(
        '--host',
        metavar='H',
        default='127.0.0.1',
        help='IP of the host server (default: 127.0.0.1)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port to listen to (default: 2000)')
    argparser.add_argument(
        '-a', '--autopilot',
        action='store_true',
        help='enable autopilot')
    argparser.add_argument(
        '--res',
        metavar='WIDTHxHEIGHT',
        default='1280x720',
        help='window resolution (default: 1280x720)')
    argparser.add_argument(
        '--filter',
        metavar='PATTERN',
        # default='vehicle.*',
        default=PLAYER_BLUEPRINT_ID,
        help='actor filter (default: "vehicle.*")')
    argparser.add_argument(
        '--generation',
        metavar='G',
        default='2',
        help='restrict to certain actor generation (values: "1","2","All" - default: "2")')
    argparser.add_argument(
        '--rolename',
        metavar='NAME',
        default='hero',
        help='actor role name (default: "hero")')
    argparser.add_argument(
        '--gamma',
        default=2.2,
        type=float,
        help='Gamma correction of the camera (default: 2.2)')
    argparser.add_argument(
        '--sync',
        action='store_true',
        help='Activate synchronous mode execution')



    args = argparser.parse_args()

    args.width, args.height = [int(x) for x in args.res.split('x')]

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    logging.info('listening to server %s:%s', args.host, args.port)

    print(__doc__)

    try:

        game_loop(args)

    except KeyboardInterrupt:
        print('\nCancelled by user. Bye!')


if __name__ == '__main__':
    recording_handler = RecordingHandler()
    main()
