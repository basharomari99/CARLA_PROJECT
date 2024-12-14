import carla
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def list_obstacle_blueprints(client):
    # Get the world and blueprint library
    world = client.get_world()
    blueprint_library = world.get_blueprint_library()

    # Define categories of interest
    obstacle_categories = ['vehicle', 'walker.pedestrian', 'static']

    # Iterate through the categories and print available blueprints
    for category in obstacle_categories:
        print(f"Available blueprints for category '{category}':")
        for blueprint in blueprint_library.filter(category):
            print(f"- {blueprint.id}")
        print()


def graphs():
    # Example telemetry data (you can modify this for your actual use case)
    telemetry_data_1 = [
        {'frame': 297021, 'curr_speed': 0.0},
        {'frame': 297022, 'curr_speed': 10.0},
        {'frame': 297023, 'curr_speed': 15.0},
        {'frame': 297024, 'curr_speed': 20.0},
        {'frame': 297025, 'curr_speed': 25.0}
    ]

    telemetry_data_2 = [
        {'frame': 297021, 'curr_speed': 0.0},
        {'frame': 297022, 'curr_speed': 5.0},
        {'frame': 297023, 'curr_speed': 10.0},
        {'frame': 297024, 'curr_speed': 15.0},
        {'frame': 297025, 'curr_speed': 20.0}
    ]

    # Extract frames and speeds for both data sets
    frames_1 = [entry['frame'] for entry in telemetry_data_1]
    speeds_1 = [entry['curr_speed'] for entry in telemetry_data_1]

    frames_2 = [entry['frame'] for entry in telemetry_data_2]
    speeds_2 = [entry['curr_speed'] for entry in telemetry_data_2]

    # Create subplots (1 row, 2 columns)
    fig, axs = plt.subplots(1, 2, figsize=(15, 6))

    # Plot the first graph (Speed vs Frames)
    axs[0].plot(frames_1, speeds_1, marker='o', linestyle='-', color='b')
    axs[0].set_title('Speed over Time (Graph 1)', fontsize=12)
    axs[0].set_xlabel('Frame', fontsize=10)
    axs[0].set_ylabel('Speed (m/s)', fontsize=10)
    axs[0].grid(True)

    # Plot the second graph (Speed vs Frames)
    axs[1].plot(frames_2, speeds_2, marker='x', linestyle='-', color='r')
    axs[1].set_title('Speed over Time (Graph 2)', fontsize=12)
    axs[1].set_xlabel('Frame', fontsize=10)
    axs[1].set_ylabel('Speed (m/s)', fontsize=10)
    axs[1].grid(True)

    # Create a table with sample data
    # This could be information like collision counts, line breaks, etc.
    table_data = [
        ['Collisions', 3],
        ['Line Breaks', 5],
        ['Max Speed', 25.0],
        ['Min Speed', 0.0],
        ['Avg Speed', 12.5]
    ]

    # Create a table with the specified data
    table = plt.table(cellText=table_data,
                      colLabels=['Metric', 'Value'],
                      cellLoc='center',
                      loc='bottom',  # Place the table below the graph
                      colColours=['#f0f0f0'] * 2,  # Light gray background for columns
                      bbox=[0.2, -0.3, 0.6, 0.2])  # Adjust the position of the table

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots and table
    plt.show()

def graphs1():

    # Example telemetry data (can be modified)
    telemetry_data_1 = [
        {'frame': 297021, 'curr_speed': 0.0},
        {'frame': 297022, 'curr_speed': 10.0},
        {'frame': 297023, 'curr_speed': 15.0},
        {'frame': 297024, 'curr_speed': 20.0},
        {'frame': 297025, 'curr_speed': 25.0}
    ]

    telemetry_data_2 = [
        {'frame': 297021, 'curr_speed': 0.0},
        {'frame': 297022, 'curr_speed': 5.0},
        {'frame': 297023, 'curr_speed': 10.0},
        {'frame': 297024, 'curr_speed': 15.0},
        {'frame': 297025, 'curr_speed': 20.0}
    ]

    # Extract frames and speeds for both datasets
    frames_1 = [entry['frame'] for entry in telemetry_data_1]
    speeds_1 = [entry['curr_speed'] for entry in telemetry_data_1]

    frames_2 = [entry['frame'] for entry in telemetry_data_2]
    speeds_2 = [entry['curr_speed'] for entry in telemetry_data_2]

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Telemetry Data Visualization")

    # Create a figure and subplots with an increased figure height (adjusted to 12)
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Further increase figure height to 12

    # Plot the first graph
    axs[0].plot(frames_1, speeds_1, marker='o', linestyle='-', color='b')
    axs[0].set_title('Speed over Time (Graph 1)', fontsize=12)
    axs[0].set_xlabel('Frame', fontsize=10)
    axs[0].set_ylabel('Speed (m/s)', fontsize=10)
    axs[0].grid(True)

    # Plot the second graph
    axs[1].plot(frames_2, speeds_2, marker='x', linestyle='-', color='r')
    axs[1].set_title('Speed over Time (Graph 2)', fontsize=12)
    axs[1].set_xlabel('Frame', fontsize=10)
    axs[1].set_ylabel('Speed (m/s)', fontsize=10)
    axs[1].grid(True)

    # Create a table above the plots (sample data)
    table_data = [
        ['Collisions', 3],
        ['Line Breaks', 5],
        ['Max Speed', 25.0],
        ['Min Speed', 0.0],
        ['Avg Speed', 12.5]
    ]

    # Add the table (adjust its position to the top)
    table = plt.table(cellText=table_data,
                      colLabels=['Metric', 'Value'],
                      cellLoc='center',
                      loc='upper center',  # Position the table in the upper-center
                      colColours=['#f0f0f0'] * 2,
                      bbox=[0.25, 0.9, 0.5, 0.1])  # Further adjust bbox to leave more space for graphs

    # Adjust the layout to avoid overlap
    plt.tight_layout(pad=5.0)  # Add more padding to ensure space between table and graphs

    # Embed the plot into the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)  # Embed the figure in the Tkinter window
    canvas.draw()

    # Place the canvas in the Tkinter window
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Add a button to close the window
    button = tk.Button(root, text="Close", command=root.quit)
    button.pack()

    # Start the Tkinter main loop (this opens the pop-up window)
    root.mainloop()


def cars_list():
    # Assuming you already have a CARLA client and world object
    client = carla.Client('localhost', 2000)
    world = client.get_world()

    # Get the blueprint library
    blueprint_library = world.get_blueprint_library()

    # Filter for vehicle blueprints
    vehicle_blueprints = blueprint_library.filter('vehicle')

    # Print the names of all available vehicles
    for vehicle in vehicle_blueprints:
        print(vehicle.id)

def main():
    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)  # Adjust the host and port if needed
    client.set_timeout(10.0)

    # List available obstacle blueprints
    list_obstacle_blueprints(client)

    available_maps = client.get_available_maps()

    # Print available maps
    print("Available maps:", available_maps)

# Example telemetry data
telemetry = {
    "collisions": [{"frame": 1}, {"frame": 2}, {"frame": 3}],
    "speed": [{"frame": 1, "curr_speed": 50}, {"frame": 2, "curr_speed": 60}, {"frame": 3, "curr_speed": 70}],
    "max_speed": 70,
    "avg_speed": 60,
    "samples_num": 3
}

def show_telemetry():
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Telemetry Data Visualization")

    # Create a frame for the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)

    # Create the button click functions
    def show_collisions():
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
        fig, ax = plt.subplots(figsize=(8, 6))
        table_data = [
            ["MAX Speed", f"{telemetry['max_speed']:.3f} km/h"],
            ["AVG Speed", f"{telemetry['avg_speed']:.3f} km/h"]
        ]
        for key in telemetry:
            if not isinstance(telemetry[key], list):
                table_data.append([key, telemetry[key]])

        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=table_data, colLabels=['Metric', 'Value'], cellLoc='center', loc='center')
        show_plot(fig)

    # Function to display the plot in the window
    def show_plot(fig):
        # Clear the current plot and create a new canvas for each plot
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Create the buttons
    button1 = tk.Button(button_frame, text="Collisions Graph", command=show_collisions)
    button1.pack(side=tk.LEFT, padx=10, pady=10)

    button2 = tk.Button(button_frame, text="Speed Graph", command=show_speed)
    button2.pack(side=tk.LEFT, padx=10, pady=10)

    button3 = tk.Button(button_frame, text="Table", command=show_table)
    button3.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a frame for displaying the plot or table
    canvas_frame = tk.Frame(root)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    # Start the Tkinter main loop
    root.mainloop()

# Call the function to show the telemetry



if __name__ == '__main__':
    cars_list()
    # show_telemetry()