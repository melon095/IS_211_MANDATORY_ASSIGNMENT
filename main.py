#!/usr/bin/env python3
from __future__ import annotations

import heapq
import itertools
import random
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class Urgency(Enum):
    IMMEDIATE = 0
    WITHIN_HOUR = 1
    TODAY = 2
    ROUTINE = 3


class Drug(Enum):
    INSULIN = ("Insulin", Urgency.IMMEDIATE, "Dose is time-critical")
    ADRENALINE_AUTO_INJECTOR = (
        "Adrenaline Auto-Injector",
        Urgency.IMMEDIATE,
        "Emergency refill",
    )
    ANTIBIOTIC = (
        "Antibiotic",
        Urgency.WITHIN_HOUR,
        "Maintain treatment window",
    )
    ASTHMA_INHALER = (
        "Asthma Inhaler",
        Urgency.WITHIN_HOUR,
        "Breathing support",
    )
    BLOOD_PRESSURE_MED = (
        "Blood Pressure Medication",
        Urgency.TODAY,
        "Daily control",
    )
    THYROID_MED = (
        "Thyroid Medication",
        Urgency.TODAY,
        "Regular hormonal therapy",
    )
    VITAMIN_D = ("Vitamin D", Urgency.ROUTINE, "Routine supplement")
    OMEGA_3 = ("Omega-3", Urgency.ROUTINE, "Routine supplement")

    @property
    def label(self) -> str:
        return self.value[0]

    @property
    def urgency(self) -> Urgency:
        return self.value[1]

    @property
    def reason(self) -> str:
        return self.value[2]


@dataclass
class Patient:
    patient_id: int
    name: str
    drug: Drug
    check_in_tick: int


class PharmacyPriorityQueue:
    def __init__(self) -> None:
        self._heap: List[Tuple[int, int, Patient]] = []
        self._sequence = itertools.count()

    def check_in(self, patient: Patient) -> None:
        heapq.heappush(
            self._heap,
            (patient.drug.urgency.value, next(self._sequence), patient),
        )

    def serve_next(self) -> Optional[Patient]:
        if not self._heap:
            return None
        _, _, patient = heapq.heappop(self._heap)
        return patient

    def peek_next(self) -> Optional[Patient]:
        if not self._heap:
            return None
        return self._heap[0][2]

    def waiting_count(self) -> int:
        return len(self._heap)


def random_name() -> str:
    first_names = [
        "Alex",
        "Sam",
        "Taylor",
        "Jordan",
        "Morgan",
        "Riley",
        "Casey",
        "Avery",
    ]
    last_names = [
        "Smith",
        "Khan",
        "Nilsen",
        "Patel",
        "Lopez",
        "Garcia",
        "Johnson",
        "Kim",
    ]
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def random_drug() -> Drug:
    all_drugs = [
        Drug.INSULIN,
        Drug.ADRENALINE_AUTO_INJECTOR,
        Drug.ANTIBIOTIC,
        Drug.ASTHMA_INHALER,
        Drug.BLOOD_PRESSURE_MED,
        Drug.THYROID_MED,
        Drug.VITAMIN_D,
        Drug.OMEGA_3,
    ]
    weights = [3, 1, 5, 4, 8, 7, 10, 10]
    return random.choices(all_drugs, weights=weights, k=1)[0]


def print_dashboard(tick: int, queue: PharmacyPriorityQueue) -> None:
    next_patient = queue.peek_next()
    print("\n" + "=" * 72)
    print(f"TICK {tick:02d} | Waiting: {queue.waiting_count()}")
    if next_patient is None:
        print("Dashboard: No patient waiting.")
    else:
        print(
            "Dashboard: Next is "
            f"#{next_patient.patient_id} {next_patient.name} | "
            f"{next_patient.drug.label} | "
            f"Priority: {next_patient.drug.urgency.name} | "
            f"Reason: {next_patient.drug.reason}"
        )
    print("=" * 72)


def run_simulation() -> None:
    # random.seed(211)

    total_new_patients = 60
    staff_capacity_per_tick = 2

    queue = PharmacyPriorityQueue()
    next_patient_id = 1
    created_patients = 0
    served_patients = 0
    total_wait_time = 0

    tick = 1
    while created_patients < total_new_patients or queue.waiting_count() > 0:
        print_dashboard(tick, queue)

        # New check-ins
        arrivals = random.randint(0, 3)
        for _ in range(arrivals):
            if created_patients >= total_new_patients:
                break
            patient = Patient(
                patient_id=next_patient_id,
                name=random_name(),
                drug=random_drug(),
                check_in_tick=tick,
            )
            queue.check_in(patient)
            print(
                f"CHECK-IN      #{patient.patient_id} {patient.name:<16} | "
                f"{patient.drug.label:<24} | "
                f"Priority {patient.drug.urgency.name}"
            )
            created_patients += 1
            next_patient_id += 1

        # Serving
        for _ in range(staff_capacity_per_tick):
            patient = queue.serve_next()
            if patient is None:
                print("SERVE        No patient to serve this slot.")
                continue

            wait_time = tick - patient.check_in_tick
            total_wait_time += wait_time
            served_patients += 1
            print(
                f"SERVE         #{patient.patient_id} {patient.name:<16} | "
                f"{patient.drug.label:<24} | "
                f"Urgency {patient.drug.urgency.name:<11} | "
                f"Wait {wait_time} tick(s)"
            )

        tick += 1

    average_wait = total_wait_time / served_patients if served_patients else 0.0

    print("\n" + "#" * 72)
    print("Simulation complete")
    print(f"Patients created: {created_patients}")
    print(f"Patients served : {served_patients}")
    print(f"Average wait    : {average_wait:.2f} tick(s)")
    print("#" * 72)


if __name__ == "__main__":
    run_simulation()
