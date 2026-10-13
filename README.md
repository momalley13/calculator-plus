# Calculator+

Calculator+ is a single-app toolkit for calibrating and diagnosing sensors, probes, and transmitters used in pharmaceutical environmental stability chambers.

## Features

- **RTD Calculator** — Pt100 / Pt1000 (IEC 60751 Callendar–Van Dusen) with tolerance classes and lead-wire compensation
- **Thermocouple Calculator** — Type K, T, J (approximate)
- **mA Scaling** — bidirectional linear conversion for 4–20 mA and 0–20 mA
- **Voltage Scaling** — bidirectional linear scaling for 0–5 Vdc and 0–10 Vdc
- **Humidity Tools** — dew point from T/%RH and %RH from T/dew point
- **Tolerance / Pass-Fail Checker** — compare expected vs measured against a set tolerance
- **Multi-Point Calibration Worksheet** — generate as-found/as-left tables (printable)
- **4–20 mA Loop Compliance Calculator** — voltage drop and margin at the transmitter
- **ICH Condition Reference** — common stability setpoints
- **Photostability Tools** — ICH Q1B dose calculator, light sensor offset, and spatial mapping helper
- **Diagnosis Helpers** — guided checks for RTD, mA, voltage, humidity, and light sensors
- **Additional Tools** — thermistor example, calibration due-date reminder (local storage), simple uncertainty sketch

## Documentation

Full documentation for core components, formulas, standards references, and usage notes is available in [DOCUMENTATION.md](DOCUMENTATION.md).

## Usage

Open `index.html` in any modern browser. No build step or dependencies required. All calculations run locally.

The Python module `pt100_calculator.py` provides the same RTD formulas for scripting or further development.

## Standards referenced

- IEC 60751 (Pt100 / Pt1000)
- ICH Q1A(R2) and Q1B
- NAMUR NE43 (4–20 mA fault bands)

## License

MIT
