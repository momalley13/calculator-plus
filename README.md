# Calculator+

Calculator+ is a single-app toolkit for calibrating and diagnosing sensors, probes, and transmitters used in pharmaceutical environmental stability chambers.

## Features (v1)

- **RTD Calculator** — Pt100 / Pt1000 using the IEC 60751 Callendar–Van Dusen equation (temperature ↔ resistance) with tolerance classes
- **4–20 mA Scaling** — bidirectional linear conversion between engineering units and loop current
- **Diagnosis helpers** — guided checks for RTD open/short/drift and 4–20 mA loop faults
- **Sensor Library** — overview of temperature, humidity, light, and other signals by chamber type
- **Photostability** — ICH Q1B dose calculator (1.2 M lux-hours visible + 200 Wh/m² UV)

## Usage

Open `index.html` in any modern browser. No build step or dependencies required.

The Python module `pt100_calculator.py` provides the same RTD formulas for scripting or further development.

## Standards referenced

- IEC 60751 (Pt100 / Pt1000)
- ICH Q1A(R2) and Q1B
- NAMUR NE43 (4–20 mA fault bands)

## License

MIT
