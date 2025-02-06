# 2024 YR4 Orbit Visualizer

Welcome to the **2024 YR4 Orbit Visualizer** – a retro‑futuristic, sensational simulation that brings you the cosmic drama of near‑Earth asteroid 2024 YR4. This interactive visualization uses state‑of‑the‑art Three.js graphics with a heavy dose of vintage sci‑fi aesthetics to present orbital mechanics, impact risk, and uncertainty in an eye‑popping display.

## Features

- **3D Orbit Visualization:**  
  Rendered with Three.js, the orbit is computed using the classic equation:  
  `r = a(1 - e²) / (1 + e cos f)`  
  with successive rotations for the argument of periapsis, inclination, and ascending node.

- **Live Countdown & Impact Simulation:**  
  A real‑time countdown to the next potential impact (with probabilities converted to percentages) and a dynamic impact cone (scaled by the residual RMS error) provide an engaging “time bomb” effect.

- **Data-Driven Updates:**  
  Orbital elements, physical parameters, and impact risk data are loaded from `ephemeris.json` and updated via dedicated Python scripts:

  - `update_ephemeris.py` (fetches orbital elements from JPL Horizons)
  - `update_sentry.py` (retrieves impact risk details from the JPL Sentry System)

- **Info Pop‑Up:**  
  An interactive modal explains the math, the data sources, and the inner workings of the visualization—perfect for the curious casual consumer.

## Data Sources

- **JPL Sentry System:**  
  [Sentry Details](https://cneos.jpl.nasa.gov/sentry/details.html#?des=2024%20YR4)  
  [Sentry API Documentation](https://ssd-api.jpl.nasa.gov/doc/sentry.html)

- **NASA/JPL-Caltech Center for Near Earth Object Studies**  
  (Ephemeris and observation data provided)

## Usage

Simply open `index.html` in your modern web browser to experience:

- The orbit and dynamic threat simulation.
- A live countdown to the next potential impact.
- On‑demand info pop‑up detailing the orbital math and data sources.

> **Note:** This visualization is for informational and entertainment purposes only. While it uses real data and standard orbital calculations, it is meant to be a fun, gimmicky experience rather than an authoritative risk assessment tool.

Happy orbiting, and stay sensational!
