from dataclasses import dataclass, field
from enum import Enum
import random
from typing import List


class PrescriptionLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def get_random_level(self):
        if self == PrescriptionLevel.LOW:
            return 0.9
        elif self == PrescriptionLevel.MEDIUM:
            return 0.5
        elif self == PrescriptionLevel.HIGH:
            return 0.1
        return 0.0


@dataclass
class Person:
    name: str
    wanted_prescriptions: list[str]
    received_prescriptions: list[str] = field(default_factory=list)
    prescription_score: int = 0


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
    person_name: str = ""


def prescription_queue_algorithm() -> tuple[List[Prescription], List[Person]]:
    queues = {
        PrescriptionLevel.HIGH: [],
        PrescriptionLevel.MEDIUM: [],
        PrescriptionLevel.LOW: [],
    }

    prescription_mapping = {
        ASPIRIN: PrescriptionLevel.LOW,
        IBUPROFEN: PrescriptionLevel.LOW,
        LISINOPRIL: PrescriptionLevel.MEDIUM,
        METFORMIN: PrescriptionLevel.MEDIUM,
        MORPHINE: PrescriptionLevel.HIGH,
        ANTIBIOTIC: PrescriptionLevel.HIGH,
    }

    people = [
        Person(
            name=f"Person_{i}",
            wanted_prescriptions=[
                drug
                for drug in DROGAS
                if random.random()
                < prescription_mapping[drug].get_random_level()
            ],
        )
        for i in range(100)
    ]

    # Lag en Perscription_Score kalkulator greie, som gir hver PerscriptionLevel en score(1-3) basert på (LOW-HIGH) og del på antall Perscriptions
    # Gi hver person en Perscription_Score variabel og filtrer rekkefølgen på hvem som skal få delt ut hva basert på det
    # Lag også en Queue Selector (HIGH PerscriptionLevel) eller (MEDIUM PerscriptionLevel) blir du plassert i den queue'en og senere filtrert innad i den queue'en

    for person in people:
        score = 0

        for drug in person.wanted_prescriptions:
            level = prescription_mapping[drug]

            if level == PrescriptionLevel.LOW:
                score += 1
            elif level == PrescriptionLevel.MEDIUM:
                score += 2
            elif level == PrescriptionLevel.HIGH:
                score += 3

        person.prescription_score = score

    people.sort(
        key=lambda person: person.prescription_score
        / len(person.wanted_prescriptions),
        reverse=True,
    )

    filtered = []

    for person in people:
        for drug in person.wanted_prescriptions:
            level = prescription_mapping[drug]

            prescription = Prescription(drug, level, person.name)
            filtered.append(prescription)
            person.received_prescriptions.append(drug)

    return filtered, people

    # # O(n * m)
    # #   n = number of people
    # #   m = prescriptions per person
    # for person in people:
    #     for prescription_name in person.wanted_prescriptions:
    #         level = prescription_mapping[prescription_name]
    #         queues[level].append(
    #             Prescription(prescription_name, level, person.name)
    #         )
    #         person.received_prescriptions.append(prescription_name)

    # filtered = []

    # # O(n)
    # #   n = total number of prescriptions in all queues
    # for level in [
    #     PrescriptionLevel.HIGH,
    #     PrescriptionLevel.MEDIUM,
    #     PrescriptionLevel.LOW,
    # ]:
    #     for prescription in queues[level]:
    #         filtered.append(prescription)

    # # Overall complexity
    # #   O(n * m) + O(n) = O(n * m)
    # return filtered, people


def drug_inventory_algorithm():
    class Batch:
        def __init__(self, batch_id: str, expiry_date: str, quantity: int):
            self.batch_id = batch_id
            self.expiry_date = expiry_date
            self.quantity = quantity
            self.next = None

    class DrugInventory:
        def __init__(self):
            self.inventory = {}

        def add_batch(
            self, drug_id: str, batch_id: str, expiry_date: str, quantity: int
        ):
            new_batch = Batch(batch_id, expiry_date, quantity)
            if drug_id not in self.inventory:
                self.inventory[drug_id] = new_batch
            else:
                current = self.inventory[drug_id]
                if new_batch.expiry_date < current.expiry_date:
                    new_batch.next = current
                    self.inventory[drug_id] = new_batch
                else:
                    # O(n)
                    #   n = number of batches for the drug
                    while (
                        current.next
                        and current.next.expiry_date < new_batch.expiry_date
                    ):
                        current = current.next
                    new_batch.next = current.next
                    current.next = new_batch

        def dispense_drug(self, drug_id: str, quantity: int) -> bool:
            if drug_id not in self.inventory:
                return False

            current = self.inventory[drug_id]
            # O(n)
            #   n = number of batches for the drug
            while current and quantity > 0:
                if current.quantity >= quantity:
                    current.quantity -= quantity
                    return True
                quantity -= current.quantity
                current = current.next

            return False

    drug_inventory = DrugInventory()
    drug_inventory.add_batch(ASPIRIN, "BATCH001", "2024-01-01", 100)
    drug_inventory.add_batch(ASPIRIN, "BATCH002", "2023-12-01", 50)
    drug_inventory.add_batch(ASPIRIN, "BATCH003", "2024-02-01", 75)
    drug_inventory.add_batch(IBUPROFEN, "BATCH001", "2024-03-01", 200)
    drug_inventory.add_batch(IBUPROFEN, "BATCH002", "2024-04-01", 150)
    drug_inventory.add_batch(LISINOPRIL, "BATCH001", "2024-05-01", 100)
    drug_inventory.add_batch(METFORMIN, "BATCH001", "2024-06-01", 120)

    if drug_inventory.dispense_drug(ASPIRIN, 30):
        print("Dispensed 30 Aspirin.")
    else:
        print("Failed to dispense Aspirin.")

    if drug_inventory.dispense_drug(IBUPROFEN, 50):
        print("Dispensed 50 Ibuprofen.")
    else:
        print("Failed to dispense Ibuprofen.")

    def print_linked_lists(drug_inventory: DrugInventory):
        for drug_id, batch in drug_inventory.inventory.items():
            print(f"Drug: {drug_id}")
            current = batch
            while current:
                print(
                    f"  Batch ID: {current.batch_id}, Expiry Date: {current.expiry_date}, Quantity: {current.quantity}"
                )
                current = current.next

    print_linked_lists(drug_inventory)

    # Overall complexity
    #   O(n) for adding batches (where n is the number of batches)
    #   O(n) for dispensing drugs (where n is the number of batches)
    #   Total: O(n)


if __name__ == "__main__":
    prescriptions, people = prescription_queue_algorithm()

    for person in people:
        if person.received_prescriptions:
            print(
                f"{person.name} received: {', '.join(person.received_prescriptions)}"
            )

    print("\nPrescription queue:")
    for p in prescriptions:
        print(f"{p.person_name} - {p.name} ({p.level.name})")

    print("\nDrug Inventory Algorithm:")
    drug_inventory_algorithm()
