import json
from pathlib import Path
from uuid import uuid4



DATA_FILE = Path(__file__).with_name("patients.json")


class Patient:
    def __init__(self, name, date_of_birth, phone, patient_id=None):
        self.patient_id = patient_id or str(uuid4())[:8]
        self.name = name.strip()
        self.date_of_birth = date_of_birth.strip()
        self.phone = phone.strip()

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "phone": self.phone,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            date_of_birth=data["date_of_birth"],
            phone=data["phone"],
            patient_id=data["patient_id"],
        )

    def __str__(self):
        return (
            f"ID: {self.patient_id} | Name: {self.name} | "
            f"Date of birth: {self.date_of_birth} | Phone: {self.phone}"
        )


class PatientRecordSystem:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = Path(data_file)
        self.patients = {}
        self.load_records()

    def load_records(self):
        if not self.data_file.exists():
            return

        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                records = json.load(file)
            self.patients = {
                record["patient_id"]: Patient.from_dict(record)
                for record in records
            }
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"Could not load patient records: {error}")

    def save_records(self):
        records = [patient.to_dict() for patient in self.patients.values()]
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)

    def add_patient(self, name, date_of_birth, phone):
        patient = Patient(name, date_of_birth, phone)
        self.patients[patient.patient_id] = patient
        self.save_records()
        return patient

    def find_patient(self, patient_id):
        return self.patients.get(patient_id.strip())

    def list_patients(self):
        return sorted(self.patients.values(), key=lambda patient: patient.name.lower())

    def delete_patient(self, patient_id):
        patient = self.patients.pop(patient_id.strip(), None)
        if patient is not None:
            self.save_records()
        return patient


def ask_required(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field is required.")


def main():
    system = PatientRecordSystem()

    while True:
        print("\nPatient Record System")
        print("1. Add patient")
        print("2. List patients")
        print("3. Search by patient ID")
        print("4. Delete patient")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            patient = system.add_patient(
                ask_required("Full name: "),
                ask_required("Date of birth (YYYY-MM-DD): "),
                ask_required("Phone number: "),
            )
            print(f"Patient added. ID: {patient.patient_id}")
        elif choice == "2":
            patients = system.list_patients()
            if not patients:
                print("No patient records found.")
            for patient in patients:
                print(patient)
        elif choice == "3":
            patient = system.find_patient(input("Patient ID: "))
            print(patient if patient else "Patient not found.")
        elif choice == "4":
            patient = system.delete_patient(input("Patient ID to delete: "))
            print(
                f"Deleted record for {patient.name}."
                if patient
                else "Patient not found."
            )
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
