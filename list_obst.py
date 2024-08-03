import carla


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


def main():
    # Connect to the CARLA server
    client = carla.Client('localhost', 2000)  # Adjust the host and port if needed
    client.set_timeout(10.0)

    # List available obstacle blueprints
    list_obstacle_blueprints(client)


if __name__ == '__main__':
    main()
