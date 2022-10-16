import json

from universe.universe import universe

if __name__ == "__main__":
    print()
    print("Starting universe.")
    print("Press Ctrl+C to quit!")
    print()

    # Open the demo configuration file
    with open("./demo_config.json") as file:
        demo_data = json.load(file)

    universe(data=demo_data, timed=False)
