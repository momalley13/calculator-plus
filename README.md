# Calculator+

Calculator+ is a single-app toolkit for calibrating and diagnosing sensors, probes, and transmitters used in pharmaceutical environmental stability chambers.

## Features

- **RTD Calculator** — Pt100 / Pt1000 using the IEC 60751 Callendar–Van Dusen equation (temperature ↔ resistance) with tolerance classes
- **mA Scaling** — bidirectional linear conversion for both 4–20 mA and 0–20 mA
- **0–5 Vdc / 0–10 Vdc Scaling** — bidirectional linear scaling for voltage-output sensors (common on photostability light sensors)
- **Diagnosis helpers** — guided checks for RTD, mA loops, voltage outputs, humidity, and photostability light sensors
- **Sensor Library** — overview of temperature, humidity, light, and other signals by chamber type
- **Photostability Dose Calculator** — ICH Q1B exposure time (1.2 M lux-hours visible + 200 Wh/m² UV)
- **Photostability Light Sensor Calibration** — procedure + offset / correction-factor calculator for lux and UV sensors

## Documentation

Full documentation for every component, formulas, standards references, and usage notes is available in [DOCUMENTATION.md](DOCUMENTATION.md).

## Usage

Open `index.html` in any modern browser. No build step or dependencies required.

The Python module `pt100_calculator.py` provides the same RTD formulas for scripting or further development.

## Standards referenced

- IEC 60751 (Pt100 / Pt1000)
- ICH Q1A(R2) and Q1B
- NAMUR NE43 (4–20 mA fault bands)

## License

MIT
