#Needs to be properly tested 

import numpy as np

def convert_time(data, input_unit):
    data = np.asarray(data, dtype=float)

    if input_unit == "s":
        return data
    if input_unit == "ms":
        return data / 1000
    if input_unit in "µs":
        return data / 1000000

    raise ValueError(f"Unsupported time unit: {input_unit}")

def convert_signal(
    data,
    input_unit,
    output_unit,
    sensitivity_mV_per_Pa=None,
    voltage_offset=0.0
):
    data = np.asarray(data, dtype=float)

    # Convert input to either volts or pascals.
    if input_unit == "V":
        voltage = data
        pressure = None
    elif input_unit == "mV":
        voltage = data / 1000
        pressure = None
    elif input_unit == "Pa":
        pressure = data
        voltage = None
    elif input_unit == "kPa":
        pressure = data * 1000
        voltage = None
    else:
        raise ValueError(f"Unsupported signal unit: {input_unit}")

    # Convert between voltage and pressure if necessary.
    if output_unit in ("V", "mV"):
        if pressure is not None:
            if sensitivity_mV_per_Pa is None or sensitivity_mV_per_Pa <= 0:
                raise ValueError(
                    "Positive microphone sensitivity is required."
                )

            sensitivity_V_per_Pa = sensitivity_mV_per_Pa / 1000
            voltage = pressure * sensitivity_V_per_Pa + voltage_offset

        return voltage if output_unit == "V" else voltage * 1000

    elif output_unit in ("Pa", "kPa"):
        if voltage is not None:
            if sensitivity_mV_per_Pa is None or sensitivity_mV_per_Pa <= 0:
                raise ValueError(
                    "Positive microphone sensitivity is required."
                )

            sensitivity_V_per_Pa = sensitivity_mV_per_Pa / 1000
            pressure = (voltage - voltage_offset) / sensitivity_V_per_Pa

        return pressure if output_unit == "Pa" else pressure / 1000

    raise ValueError(f"Unsupported output unit: {output_unit}")
