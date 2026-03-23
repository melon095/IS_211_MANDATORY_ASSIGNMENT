# Pharmacy Priority Queue Simulation

- [Pharmacy Priority Queue Simulation](#pharmacy-priority-queue-simulation)
  - [How to Run](#how-to-run)
  - [What It Does](#what-it-does)
  - [Changing Parameters](#changing-parameters)


A simulation of a pharmacy patient queue system that prioritizes patients based on the urgency of their medication needs.

## How to Run

On windows you might run it as:

```bash
py main.py
```

On macOS or Linux you might run it as:

```bash
python3 main.py
```


The project does not use any external dependencies, only the Python standard library.

## What It Does

The simulation models a pharmacy where:
- Between 0-3 random patients arrive per tick
- Each patient needs a specific medication with different urgency levels
- Staff can serve up to 2 patients per tick
- Patients are served based on urgency, e.g, highest priortity served first
- The simulation runs until $P$ patients are served

## Changing Parameters

You can adjust the parameters of the simulation by modifying the `main.py` file. The `total_parameter_patients`, `staff_capacity_per_tick` variables are used to denote the total number of patients that arrive and the number of patients that can be served per tick, respectively. You can change these values to see how it affects the simulation.

```diff
- total_parameter_patients = 60
- staff_capacity_per_tick = 2
+ total_parameter_patients = 100
+ staff_capacity_per_tick = 3
```