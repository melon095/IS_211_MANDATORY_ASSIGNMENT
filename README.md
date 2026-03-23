# Pharmacy Priority Queue Simulation

- [Pharmacy Priority Queue Simulation](#pharmacy-priority-queue-simulation)
  - [How to Run](#how-to-run)
  - [What It Does](#what-it-does)
  - [Data Structures Used](#data-structures-used)
    - [1. Min-Heap based priority queue](#1-min-heap-based-priority-queue)
    - [2. Dictionary (Hash Table)](#2-dictionary-hash-table)
    - [3. Enum](#3-enum)
    - [4. Dataclass](#4-dataclass)
  - [Time Complexities](#time-complexities)
    - [PharmacyPriorityQueue Operations:](#pharmacypriorityqueue-operations)
    - [PatientRegistry Operations:](#patientregistry-operations)
    - [Overall Simulation Complexity:](#overall-simulation-complexity)


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
- The simulation runs until all $P$ patients are served

## Data Structures Used

### 1. Min-Heap based priority queue
- Class: `PharmacyPriorityQueue`
- Implementation: Uses Python's `heapq` module
- Purpose: Maintains patients in priority order
- Structure: Stores tuples of `(urgency_value, sequence_number, patient)`
  - `urgency_value`: Lower values = higher priority (0 = IMMEDIATE, 3 = ROUTINE)
  - `sequence_number`: Ensures FIFO ordering for same urgency level
  - `patient`: The actual patient object

### 2. Dictionary (Hash Table)
- Class: `PatientRegistry`
- Implementation: Python `dict` mapping `patient_id -> PatientRecord`
- Purpose: Track patient status (WAITING or SERVED) and maintain overall statistics
- Key-value: Integer ID maps to PatientRecord object

### 3. Enum
- Classes: `Urgency` and `Drug`
- Purpose: Define fixed sets of values for urgency levels and drug types

### 4. Dataclass
- Classes: `Patient` and `PatientRecord`

## Time Complexities

### PharmacyPriorityQueue Operations:
- `check_in()`: $O(log n)$ - heap insertion
- `serve_next()`: $O(log n)$ - heap extraction
- `peek_next()`: $O(1)$ - just looks at heap[0]
- `waiting_count()`: $O(1)$ - returns length of heap

### PatientRegistry Operations:
- `add_waiting_patient()`: $O(1)$ - dictionary insertion
- `mark_served()`: $O(1)$ - dictionary lookup and update
- `status_for()`: $O(1)$ - dictionary lookup
- `total_patients()`: $O(1)$ - returns length of dictionary
- `waiting_patients()`: $O(n)$ - iterates through all records
- `served_patients()`: $O(n)$ - iterates through all records
- `all_served()`: $O(n)$ - calls waiting_patients()

### Overall Simulation Complexity:
$O(P log P)$ operations total since $P$ patients are processed and each patient is added and served once.
