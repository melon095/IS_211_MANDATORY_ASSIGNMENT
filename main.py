from dataclasses import dataclass
from enum import Enum
import random


class PrescriptionLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Person:
    name: str
    wanted_prescriptions: list[str]


ASPIRIN = "Aspirin"
LISINOPRIL = "Lisinopril"
METFORMIN = "Metformin"
MORPHINE = "Morphine"
IBUPROFEN = "Ibuprofen"
ANTIBIOTIC = "Antibiotic"

DROGAS = [ASPIRIN, LISINOPRIL, METFORMIN, MORPHINE, IBUPROFEN, ANTIBIOTIC]


@dataclass
class Prescription:
    name: str
    level: PrescriptionLevel


def main():
    queues = {
        PrescriptionLevel.HIGH: [],
        PrescriptionLevel.MEDIUM: [],
        PrescriptionLevel.LOW: [],
    }

    people = [
        Person(
            name=f"Person_{i}",
            wanted_prescriptions=[drug for drug in DROGAS if random.random() > 0.5],
        )
        for i in range(100)
    ]

    prescription_mapping = {
        ASPIRIN: PrescriptionLevel.LOW,
        IBUPROFEN: PrescriptionLevel.LOW,
        LISINOPRIL: PrescriptionLevel.MEDIUM,
        METFORMIN: PrescriptionLevel.MEDIUM,
        MORPHINE: PrescriptionLevel.HIGH,
        ANTIBIOTIC: PrescriptionLevel.HIGH,
    }

    for person in people:
        for prescription_name in person.wanted_prescriptions:
            level = prescription_mapping[prescription_name]
            queues[level].append(Prescription(prescription_name, level))

    for level in [
        PrescriptionLevel.HIGH,
        PrescriptionLevel.MEDIUM,
        PrescriptionLevel.LOW,
    ]:
        for prescription in queues[level]:
            print(
                f"Processing prescription: {prescription.name} with level {prescription.level.name}"
            )


if __name__ == "__main__":
    main()
