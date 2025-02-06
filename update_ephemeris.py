#!/usr/bin/env python3
import telnetlib
import time
import json
import re
from datetime import datetime


def connect_to_horizons():
    """Connect to Horizons telnet server."""
    HOST = "horizons.jpl.nasa.gov"
    PORT = 6775

    try:
        tn = telnetlib.Telnet(HOST, PORT)
        return tn
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None


def extract_orbital_elements(data):
    """Extract orbital elements from Horizons output."""
    # Convert bytes to string if necessary
    if isinstance(data, bytes):
        data = data.decode("utf-8")

    print("Raw data received:")
    print(data)  # Debug output

    # Regular expressions to match the values
    patterns = {
        "epoch": r"EPOCH=\s*(\d+\.\d+)\s*!\s*([^(]+)",
        "semimajor_axis": r"A=\s*([\d.]+)",
        "eccentricity": r"EC=\s*([\d.]+)",
        "inclination": r"IN=\s*([\d.]+)",
        "longitude_ascending_node": r"OM=\s*([\d.]+)",
        "argument_periapsis": r"W=\s*([\d.]+)",
        "mean_anomaly": r"MA=\s*([\d.]+)",
    }

    results = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, data)
        if match:
            if key == "epoch":
                results[key] = match.group(1)
                results["epoch_description"] = match.group(2).strip()
            else:
                try:
                    results[key] = float(
                        match.group(1).split()[0]
                    )  # Take first part in case there are spaces
                except (ValueError, IndexError) as e:
                    print(f"Error parsing {key}: {e}")
                    print(f"Raw match: {match.group(1)}")

    if results:
        print("\nExtracted elements:")
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print("\nNo elements were extracted!")

    return results


def update_ephemeris_file(elements):
    """Update the ephemeris.json file with new orbital elements."""
    # Create the new JSON structure
    data = {
        "name": "2024 YR4",
        "epoch": elements["epoch"],
        "epoch_description": elements["epoch_description"],
        "orbital_elements": {
            "semimajor_axis": {"value": elements["semimajor_axis"], "unit": "AU"},
            "eccentricity": elements["eccentricity"],
            "inclination": {"value": elements["inclination"], "unit": "deg"},
            "longitude_ascending_node": {
                "value": elements["longitude_ascending_node"],
                "unit": "deg",
            },
            "argument_periapsis": {
                "value": elements["argument_periapsis"],
                "unit": "deg",
            },
            "mean_anomaly": {"value": elements["mean_anomaly"], "unit": "deg"},
        },
    }

    # Write to file with nice formatting
    with open("ephemeris.json", "w") as f:
        json.dump(data, f, indent=2)

    print(f"Updated ephemeris.json at {datetime.now()}")


def main():
    tn = connect_to_horizons()
    if not tn:
        return

    try:
        # Wait for initial prompt and send object name
        tn.read_until(b"Horizons> ")
        tn.write(b"2024 YR4\n")

        # Wait for and handle the confirmation prompt
        tn.read_until(b"Continue [ <cr>=yes, n=no, ? ] :")
        tn.write(b"\n")

        # Wait a bit for the data to arrive
        time.sleep(2)

        # Read the full response
        data = b""
        while True:
            try:
                chunk = tn.read_eager()
                if not chunk:
                    break
                data += chunk
                if b"Select ... [A]pproaches," in chunk:
                    break
                time.sleep(0.5)
            except EOFError:
                break

        # Extract orbital elements
        elements = extract_orbital_elements(data)

        if elements:
            update_ephemeris_file(elements)
        else:
            print("Failed to extract orbital elements")

    except Exception as e:
        print(f"Error during data fetch: {e}")
    finally:
        try:
            # Try to exit cleanly
            tn.write(b"x\n")  # 'x' to exit
            tn.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    main()
