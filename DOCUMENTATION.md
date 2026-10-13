# Calculator+ Documentation

**Calculator+** is a single-tool application for calibration and diagnosis of sensors, probes, and transmitters used in pharmaceutical environmental stability chambers. It supports ICH Q1A and Q1B conditions and common electrical signals.

**Repository:** https://github.com/momalley13/calculator-plus  
**Live app (after GitHub Pages is enabled):** https://momalley13.github.io/calculator-plus/

---

## Table of Contents

1. [Overview](#overview)
2. [RTD Calculator (IEC 60751)](#rtd-calculator-iec-60751)
3. [4–20 mA Scaling Module](#420-ma-scaling-module)
4. [Diagnosis Helpers](#diagnosis-helpers)
5. [Sensor Library](#sensor-library)
6. [Photostability Dose Calculator (ICH Q1B)](#photostability-dose-calculator-ich-q1b)
7. [Photostability Light Sensor Calibration](#photostability-light-sensor-calibration)
8. [Standards Reference](#standards-reference)
9. [Usage Notes](#usage-notes)

---

## Overview

Calculator+ is designed as a practical field and laboratory support tool for pharmaceutical stability work. It focuses on the sensors and signals commonly found in:

- Reach-in and walk-in stability chambers
- Photostability chambers
- CO₂ incubators
- Cold storage and related environmental equipment

All calculations run client-side in the browser. No installation or external dependencies are required.

---

## RTD Calculator (IEC 60751)

### Purpose
Bidirectional conversion between temperature and resistance for platinum RTDs (Pt100 and Pt1000) using the Callendar–Van Dusen equation defined in IEC 60751.

### Supported Sensors
- Pt100 (R₀ = 100 Ω at 0 °C)
- Pt1000 (R₀ = 1000 Ω at 0 °C)

### Equations Implemented

**Temperature → Resistance (t ≥ 0 °C):**
\[
R_t = R_0 (1 + A t + B t^2)
\]

**Temperature → Resistance (t < 0 °C):**
\[
R_t = R_0 [1 + A t + B t^2 + C (t - 100) t^3]
\]

**Resistance → Temperature (t ≥ 0 °C)** — closed-form quadratic:
\[
t = \frac{-A + \sqrt{A^2 - 4B(1 - R_t/R_0)}}{2B}
\]

Coefficients (IEC 60751, α = 0.003851):
- \( A = 3.9083 \times 10^{-3} \)
- \( B = -5.775 \times 10^{-7} \)
- \( C = -4.183 \times 10^{-12} \)

### Tolerance Classes (IEC 60751)

| Class | Tolerance Formula (°C) | Example at 0 °C | Example at 100 °C |
|-------|------------------------|-----------------|-------------------|
| AA    | ±(0.10 + 0.0017\|t\|)  | ±0.10 °C        | ±0.27 °C          |
| A     | ±(0.15 + 0.002\|t\|)   | ±0.15 °C        | ±0.35 °C          |
| B     | ±(0.30 + 0.005\|t\|)   | ±0.30 °C        | ±0.80 °C          |
| C     | ±(0.60 + 0.01\|t\|)    | ±0.60 °C        | ±1.60 °C          |

**Note:** Validity ranges differ for wire-wound vs. thin-film elements. Class A and B are most commonly used in pharmaceutical applications.

### Additional Features
- Instantaneous sensitivity (dR/dT) in Ω/°C
- Approximate 2-wire lead-resistance temperature error estimate

### Typical Stability Chamber Points
| Temperature | Pt100 Resistance |
|-------------|------------------|
| 0 °C        | 100.00 Ω         |
| 25 °C       | ≈ 109.73 Ω       |
| 30 °C       | ≈ 111.67 Ω       |
| 40 °C       | ≈ 115.54 Ω       |
| 100 °C      | ≈ 138.51 Ω       |

---

## 4–20 mA Scaling Module

### Purpose
Bidirectional linear conversion between engineering units (process value) and loop current for standard 4–20 mA transmitters.

### Formulas

**Engineering Units → mA:**
\[
I = 4 + 16 \times \frac{(PV - LRV)}{(URV - LRV)}
\]

**mA → Engineering Units:**
\[
PV = LRV + \frac{(I - 4)}{16} \times (URV - LRV)
\]

### NAMUR NE43 Fault Bands (reference)
- < 3.6 mA → low fault / sensor open
- 4–20 mA → normal operating range
- > 21 mA → high fault / over-range / short

### Typical Uses in Stability Chambers
- Temperature transmitters
- Humidity transmitters
- Differential pressure transmitters
- CO₂ transmitters

---

## Diagnosis Helpers

Guided, symptom-based checklists that integrate with the calculators. Use the relevant calculator to generate expected values, then compare against measured values.

### Available Paths

**RTD / Temperature Sensor**
1. Measure resistance at transmitter terminals (sensor disconnected).
2. Compare to expected resistance from the RTD Calculator.
3. Infinite resistance → open circuit (leads or element).
4. Near 0 Ω → short.
5. Finite but outside tolerance → drift, wrong type, or lead resistance.
6. Simulate expected resistance into transmitter and verify 4–20 mA output.

**4–20 mA Loop**
1. Measure actual loop current.
2. 0 mA → open loop or no power.
3. < ~3.6 mA → low fault (NAMUR).
4. Value within 4–20 mA but incorrect → use scaling calculator to verify expected vs displayed.
5. > ~21 mA → high fault.
6. Substitute loop calibrator to isolate sensor/transmitter from receiver.

**Humidity Sensor**
- Compare to calibrated reference hygrometer at the same location.
- Check for condensation, contamination, or hysteresis after high-RH exposure.
- Verify temperature compensation is active.
- Check output scaling against expected %RH.

**Photostability Light Sensor**
- Verify reference meter is calibrated and traceable.
- Compare chamber sensor to reference at the same location (use Offset Calculator).
- Check for dirty sensor window, lamp aging, or spatial non-uniformity.
- Confirm visible (lux) and UV (W/m²) channels independently.
- Re-map chamber if offset exceeds acceptance limits.

---

## Sensor Library

High-level categorization of sensors and signals commonly found in pharmaceutical stability equipment.

| Category       | Typical Sensors                  | Common Outputs          | Chamber Types                  |
|----------------|----------------------------------|-------------------------|--------------------------------|
| Temperature    | Pt100/Pt1000 RTD, Thermocouple, Thermistor | 4–20 mA, 0–10 V, digital | All stability chambers        |
| Humidity       | Capacitive polymer, combined T/RH | 4–20 mA, digital       | ICH 25 °C/60 % RH, 40 °C/75 % RH |
| Light          | Lux meter, UV radiometer         | Analog / digital        | Photostability chambers       |
| Other          | CO₂, differential pressure, door switches | 4–20 mA, digital     | CO₂ incubators, walk-ins      |

---

## Photostability Dose Calculator (ICH Q1B)

### Purpose
Estimate the exposure time required to meet ICH Q1B confirmatory study thresholds from measured chamber intensity.

### ICH Q1B Minimum Exposure (Confirmatory Studies)
- Visible light: **≥ 1.2 million lux-hours**
- Near UV (320–400 nm): **≥ 200 Wh/m²**

### Formula
\[
\text{Time (hours)} = \frac{\text{Target Dose}}{\text{Measured Intensity}}
\]

- Visible: \( 1{,}200{,}000 / \text{lux} \)
- UV: \( 200 / \text{W/m²} \)

Use the longer of the two calculated times when both conditions must be met.

### Light Source Options (ICH Q1B)
- **Option 1:** Single source approximating D65/ID65 daylight (filtered xenon or metal halide).
- **Option 2:** Cool white fluorescent + near-UV fluorescent (most common in pharmaceutical labs).

---

## Photostability Light Sensor Calibration

### Purpose
Provide a practical procedure for verifying and correcting lux meters and UV radiometers used in photostability chambers, plus a calculator for sensor offsets and correction factors.

### Calibration Procedure Summary

1. **Pre-checks** — Confirm reference standard is in calibration (NIST-traceable or ISO 17025). Inspect sensor window. Control ambient light.
2. **Stabilization** — Allow reference lamp and unit under test 5–15 minutes warm-up.
3. **Positioning** — Place sensor at the same distance and orientation as the reference; match sample-plane height used in the chamber.
4. **Multi-point checks**
   - Visible (lux): typical points 500, 1000, 5000, 10000 lux (or chamber-typical values).
   - UV (W/m²): points covering expected chamber range (e.g., 0.5–5 W/m²).
5. **Readings** — Take 3–5 replicates at each point.
6. **Calculate** — Average, then compute offset, % error, and correction factor.
7. **Acceptance (typical GMP practice)** — Deviation ≤ ±5 % (some SOPs use ±10 %). Repeatability CV ≤ 2 %. Document as-found / as-left.
8. **Apply correction** — Enter offset or multiplier in chamber controller if permitted; re-verify.
9. **Documentation** — Certificate with traceability, serial numbers, conditions, analyst, and next due date (typically 6–12 months).

### Offset / Correction Factor Formulas

\[
\text{Offset} = \text{Reference} - \text{Measured}
\]

\[
\text{Correction Factor} = \frac{\text{Reference}}{\text{Measured}}
\]

\[
\% \text{ Error} = \left( \frac{\text{Measured} - \text{Reference}}{\text{Reference}} \right) \times 100
\]

\[
\text{Corrected Reading} = \text{Measured} \times \text{Correction Factor}
\]

The calculator supports both lux (visible) and W/m² (UV) units and flags results outside a typical ±5 % acceptance band.

---

## Standards Reference

| Standard / Guideline | Relevance |
|----------------------|-----------|
| **IEC 60751**        | Platinum RTD Callendar–Van Dusen equation and tolerance classes (AA, A, B, C) |
| **ICH Q1A(R2)**      | Stability conditions (e.g., 25 °C/60 % RH, 40 °C/75 % RH, Zone IVb 30 °C/75 % RH) |
| **ICH Q1B**          | Photostability testing: ≥1.2 million lux-hours visible + ≥200 Wh/m² near UV |
| **NAMUR NE43**       | 4–20 mA transmitter fault indication bands |
| **ISO 17025**        | Calibration laboratory competence and traceability |

---

## Usage Notes

- All calculations are performed locally in the browser. No data is transmitted.
- Results are intended for calibration support, diagnosis, and training. Always follow your site’s validated SOPs and quality system for GxP decisions.
- For official calibration certificates, use traceable reference standards and accredited laboratories.
- The Python module `pt100_calculator.py` implements the same RTD formulas and can be used for scripting or further development.

---

*Calculator+ — Pharmaceutical Stability Chamber Calibration & Diagnosis Tool*
