"""
Pt100 / Pt1000 RTD Calculator
IEC 60751 Callendar-Van Dusen implementation
For pharmaceutical stability chamber calibration and diagnosis

Supports:
- Temperature → Resistance
- Resistance → Temperature
- Pt100 and Pt1000
- Tolerance classes (AA, A, B, C)
- Sensitivity (dR/dT)
"""

import math
from typing import Literal

# IEC 60751 coefficients (α = 0.003851)
A = 3.9083e-3
B = -5.775e-7
C = -4.183e-12


def rtd_resistance(temp_c: float, r0: float = 100.0) -> float:
    """
    Calculate RTD resistance from temperature (Callendar-Van Dusen).
    
    Args:
        temp_c: Temperature in °C
        r0: Resistance at 0 °C (100 for Pt100, 1000 for Pt1000)
    
    Returns:
        Resistance in ohms
    """
    if temp_c >= 0:
        return r0 * (1 + A * temp_c + B * temp_c**2)
    else:
        return r0 * (1 + A * temp_c + B * temp_c**2 + C * (temp_c - 100) * temp_c**3)


def rtd_temperature(resistance: float, r0: float = 100.0, max_iter: int = 50, tol: float = 1e-8) -> float:
    """
    Calculate temperature from RTD resistance.
    
    Uses closed-form quadratic above 0 °C and Newton-Raphson below 0 °C.
    
    Args:
        resistance: Measured resistance in ohms
        r0: Resistance at 0 °C (100 for Pt100, 1000 for Pt1000)
        max_iter: Maximum iterations for sub-zero solver
        tol: Convergence tolerance
    
    Returns:
        Temperature in °C
    """
    ratio = resistance / r0

    # Above 0 °C: quadratic solution
    if resistance >= r0:
        discriminant = A**2 - 4 * B * (1 - ratio)
        if discriminant < 0:
            raise ValueError("Resistance out of valid range for this RTD")
        temp = (-A + math.sqrt(discriminant)) / (2 * B)
        return temp

    # Below 0 °C: Newton-Raphson iteration
    # Start with a reasonable guess
    t = (resistance - r0) / (r0 * A)  # linear approximation
    t = max(t, -200.0)

    for _ in range(max_iter):
        # f(t) = calculated R - measured R
        r_calc = rtd_resistance(t, r0)
        f = r_calc - resistance

        if abs(f) < tol:
            return t

        # Derivative dR/dt
        if t >= 0:
            dr_dt = r0 * (A + 2 * B * t)
        else:
            dr_dt = r0 * (
                A + 2 * B * t
                + C * (4 * t**3 - 300 * t**2)
            )

        if abs(dr_dt) < 1e-12:
            break

        t_new = t - f / dr_dt
        t_new = max(min(t_new, 0.0), -200.0)

        if abs(t_new - t) < tol:
            return t_new
        t = t_new

    return t


def rtd_sensitivity(temp_c: float, r0: float = 100.0) -> float:
    """
    Instantaneous sensitivity dR/dT in Ω/°C.
    """
    if temp_c >= 0:
        return r0 * (A + 2 * B * temp_c)
    else:
        return r0 * (
            A + 2 * B * temp_c
            + C * (4 * temp_c**3 - 300 * temp_c**2)
        )


def tolerance_class(temp_c: float, class_name: Literal["AA", "A", "B", "C"] = "A") -> float:
    """
    IEC 60751 tolerance at given temperature (°C).
    Returns the ± tolerance value in °C.
    """
    t = abs(temp_c)
    if class_name == "AA":
        return 0.10 + 0.0017 * t
    elif class_name == "A":
        return 0.15 + 0.002 * t
    elif class_name == "B":
        return 0.30 + 0.005 * t
    elif class_name == "C":
        return 0.60 + 0.01 * t
    else:
        raise ValueError("Class must be 'AA', 'A', 'B', or 'C'")


def lead_wire_error(lead_resistance_ohm: float, temp_c: float, r0: float = 100.0) -> float:
    """
    Approximate temperature error caused by lead wire resistance (2-wire).
    Returns error in °C.
    """
    sens = rtd_sensitivity(temp_c, r0)
    if sens == 0:
        return 0.0
    return lead_resistance_ohm / sens


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------

def pt100_resistance(temp_c: float) -> float:
    return rtd_resistance(temp_c, r0=100.0)


def pt100_temperature(resistance: float) -> float:
    return rtd_temperature(resistance, r0=100.0)


def pt1000_resistance(temp_c: float) -> float:
    return rtd_resistance(temp_c, r0=1000.0)


def pt1000_temperature(resistance: float) -> float:
    return rtd_temperature(resistance, r0=1000.0)


# ---------------------------------------------------------------------------
# Demo / verification against known IEC values
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Pt100 / Pt1000 Calculator — IEC 60751 Callendar-Van Dusen")
    print("=" * 60)

    test_temps = [0, 25, 30, 40, 60, 100, -20, -40]

    print("\nPt100 Reference Values:")
    print(f"{'Temp (°C)':>10} {'R (Ω)':>12} {'Sens (Ω/°C)':>14} {'Class A (±°C)':>14}")
    print("-" * 55)
    for t in test_temps:
        r = pt100_resistance(t)
        s = rtd_sensitivity(t, 100.0)
        tol = tolerance_class(t, "A")
        print(f"{t:10.1f} {r:12.4f} {s:14.4f} {tol:14.3f}")

    print("\nInverse check (Resistance → Temperature):")
    known = [
        (100.00, 0.0),
        (109.73, 25.0),
        (115.54, 40.0),
        (138.51, 100.0),
    ]
    for r, expected_t in known:
        calc_t = pt100_temperature(r)
        print(f"  {r:7.2f} Ω  →  {calc_t:8.4f} °C  (expected ≈ {expected_t})")

    print("\nExample: 2-wire lead error at 25 °C with 0.5 Ω total lead resistance")
    err = lead_wire_error(0.5, 25.0, r0=100.0)
    print(f"  Approximate temperature error: {err:.3f} °C")

    print("\nPt1000 at 25 °C:", round(pt1000_resistance(25), 2), "Ω")
