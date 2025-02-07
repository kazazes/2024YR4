#!/usr/bin/env python3
import json
import requests
from datetime import datetime


def fetch_sentry_data():
    """Fetch data from CNEOS Sentry API."""
    url = "https://ssd-api.jpl.nasa.gov/sentry.api"
    params = {"des": "2024 YR4"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching Sentry data: {e}")
        return None


def parse_sentry_data(api_data):
    """Parse the Sentry API response and extract relevant data."""
    if not api_data or "data" not in api_data:
        return None

    print("Raw API response:")
    print(json.dumps(api_data, indent=2))  # Debug output

    # Get the summary data
    summary = api_data.get("summary", {})

    # Find the impact with maximum Torino Scale
    max_torino_impact = None
    max_ps_impact = None
    for impact in api_data["data"]:
        if max_torino_impact is None or float(impact.get("ts", 0)) > float(
            max_torino_impact.get("ts", 0)
        ):
            max_torino_impact = impact
        if max_ps_impact is None or float(impact.get("ps", 0)) > float(
            max_ps_impact.get("ps", 0)
        ):
            max_ps_impact = impact

    # Initialize data structure with API values
    data = {
        "impact_risk": {
            "source": "JPL Sentry System",
            "last_updated": summary.get("cdate", "").split()[
                0
            ],  # Get just the date part
            "status": "monitored",
            "impact_probability": (
                float(max_torino_impact.get("ip", 0)) if max_torino_impact else 0
            ),
            "palermo_scale": {
                "maximum": float(summary.get("ps_max", 0)),
                "cumulative": float(summary.get("ps_cum", 0)),
            },
            "torino_scale": {"maximum": int(summary.get("ts_max", 0))},
            "potential_impacts": {
                "count": int(summary.get("n_imp", 0)),
                "dates": [],
                "probabilities": [],
            },
            "impact_velocity": {
                "value": float(summary.get("v_imp", 0)),
                "unit": "km/s",
            },
        }
    }

    # Add impact data
    if api_data["data"]:
        impacts = []
        probabilities = []
        for impact in sorted(api_data["data"], key=lambda x: x["date"]):
            impacts.append(impact["date"])
            probabilities.append(float(impact["ip"]))

        data["impact_risk"]["potential_impacts"]["dates"] = impacts
        data["impact_risk"]["potential_impacts"]["probabilities"] = probabilities
        data["impact_risk"]["potential_impacts"]["count"] = len(impacts)

    print("\nExtracted data:")
    print(json.dumps(data, indent=2))  # Debug output

    return data


def update_json_file(sentry_data):
    """Update the ephemeris.json file with Sentry data."""
    try:
        # Read existing file
        with open("ephemeris.json", "r") as f:
            data = json.load(f)

        # Update or create impact risk data
        if sentry_data and "impact_risk" in sentry_data:
            if "impact_risk" not in data:
                data["impact_risk"] = {}
            data["impact_risk"].update(sentry_data["impact_risk"])

        # Write updated data back to file
        with open("ephemeris.json", "w") as f:
            json.dump(data, f, indent=2)

        print(f"Updated ephemeris.json with Sentry data at {datetime.now()}")

    except Exception as e:
        print(f"Error updating JSON file: {e}")
        # Print the current state of data for debugging
        print("\nCurrent data structure:")
        print(json.dumps(data, indent=2))


def main():
    print("Fetching Sentry data for 2024 YR4...")
    api_data = fetch_sentry_data()
    if api_data:
        sentry_data = parse_sentry_data(api_data)
        if sentry_data:
            update_json_file(sentry_data)
        else:
            print("No Sentry data could be parsed")
    else:
        print("Failed to fetch Sentry data")


if __name__ == "__main__":
    main()
