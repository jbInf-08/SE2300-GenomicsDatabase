import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Union
import json
import os

class GeneSequence:
    def __init__(self, gene_id: str, sequence: str, mutation_status: str = None):
        self.gene_id = gene_id
        self.sequence = sequence
        self.mutation_status = mutation_status

    def validate_sequence(self) -> bool:
        """Validate if the sequence contains only valid nucleotides."""
        valid_nucleotides = set('ATCG')
        return all(nucleotide in valid_nucleotides for nucleotide in self.sequence.upper())

    def detect_mutation(self, reference_sequence: str) -> Optional[str]:
        """Compare with reference sequence to detect mutations."""
        if len(self.sequence) != len(reference_sequence):
            return "Length mismatch with reference sequence"
        
        mutations = []
        for pos, (ref, current) in enumerate(zip(reference_sequence, self.sequence)):
            if ref != current:
                mutations.append(f"{ref}{pos+1}{current}")
        
        return ','.join(mutations) if mutations else None

class PatientRecord:
    def __init__(self, patient_id: str, name: str = "Unknown", age: int = 0, diagnosis: str = "Unknown"):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.diagnosis = diagnosis
        self.gene_sequences: Dict[str, GeneSequence] = {}

    def validate_patient_data(self) -> bool:
        """Validate patient data fields."""
        if not isinstance(self.age, int) or self.age < 0 or self.age > 150:
            return False
        if not self.patient_id:
            return False
        return True

    def add_gene_sequence(self, gene_sequence: GeneSequence):
        """Add a gene sequence to the patient record."""
        self.gene_sequences[gene_sequence.gene_id] = gene_sequence

class CancerGenomicsDatabase:
    def __init__(self, csv_path: str = None, database_path: str = "genomics_data.json"):
        self.database_path = database_path
        self.patients: Dict[str, PatientRecord] = {}
        if csv_path:
            self.load_from_csv(csv_path)
        else:
            self.load_database()

    def load_from_csv(self, csv_path: str):
        """Load data from METABRIC CSV file."""
        try:
            print(f"Loading data from {csv_path}...")
            df = pd.read_csv(csv_path)
            print(f"Found {len(df)} records. Processing...")
            
            # Process each row in the dataframe
            for index, row in df.iterrows():
                # Create patient ID from index if not available
                patient_id = str(index)
                
                # Create a new patient record
                patient = PatientRecord(patient_id=patient_id)
                
                # Process each column (gene) in the row
                for gene_name in df.columns:
                    if gene_name not in ['patient_id', 'name', 'age', 'diagnosis']:  # Skip non-gene columns
                        mutation_value = row[gene_name]
                        if not pd.isna(mutation_value):  # Only process non-null values
                            gene_sequence = GeneSequence(
                                gene_id=gene_name,
                                sequence="",  # Actual sequence not provided in mutation data
                                mutation_status=str(mutation_value)
                            )
                            patient.add_gene_sequence(gene_sequence)
                
                self.patients[patient_id] = patient
                
                # Progress indicator
                if (index + 1) % 100 == 0:
                    print(f"Processed {index + 1} records...")
            
            print(f"Successfully loaded {len(self.patients)} patient records.")
            self.save_database()  # Save to JSON for future quick loading
            
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            raise

    def load_database(self):
        """Load database from JSON file if it exists."""
        if os.path.exists(self.database_path):
            try:
                with open(self.database_path, 'r') as f:
                    data = json.load(f)
                    for patient_data in data:
                        patient = PatientRecord(
                            patient_data['patient_id'],
                            patient_data.get('name', 'Unknown'),
                            patient_data.get('age', 0),
                            patient_data.get('diagnosis', 'Unknown')
                        )
                        for gene_data in patient_data.get('gene_sequences', []):
                            gene_seq = GeneSequence(
                                gene_data['gene_id'],
                                gene_data.get('sequence', ''),
                                gene_data['mutation_status']
                            )
                            patient.add_gene_sequence(gene_seq)
                        self.patients[patient.patient_id] = patient
            except Exception as e:
                print(f"Error loading database: {e}")

    def save_database(self):
        """Save database to file."""
        data = []
        for patient in self.patients.values():
            patient_data = {
                'patient_id': patient.patient_id,
                'name': patient.name,
                'age': patient.age,
                'diagnosis': patient.diagnosis,
                'gene_sequences': [
                    {
                        'gene_id': seq.gene_id,
                        'sequence': seq.sequence,
                        'mutation_status': seq.mutation_status
                    }
                    for seq in patient.gene_sequences.values()
                ]
            }
            data.append(patient_data)
        
        with open(self.database_path, 'w') as f:
            json.dump(data, f, indent=2)

    def add_patient(self, patient: PatientRecord) -> bool:
        """Add a new patient to the database."""
        if not patient.validate_patient_data():
            return False
        self.patients[patient.patient_id] = patient
        self.save_database()
        return True

    def get_patient(self, patient_id: str) -> Optional[PatientRecord]:
        """Retrieve a patient record by ID."""
        return self.patients.get(patient_id)

    def query_by_diagnosis(self, diagnosis: str) -> List[PatientRecord]:
        """Query patients by diagnosis."""
        return [p for p in self.patients.values() if p.diagnosis.lower() == diagnosis.lower()]

# ... (rest of the code remains the same)

def main():
    # Initialize database with CSV file
    csv_path = r"C:\Users\jbaut\Downloads\archive.zip\METABRIC_RNA_Mutation.csv"
    try:
        db = CancerGenomicsDatabase(csv_path=csv_path)
    except Exception as e:
        print(f"Failed to load CSV file: {e}")
        print("Starting with empty database...")
        db = CancerGenomicsDatabase()
    
    while True:
        print("\nCancer Genomics Data Management System")
        print("1. Add new patient")
        print("2. Add gene sequence to patient")
        print("3. Query patient by ID")
        print("4. Query patients by diagnosis")
        print("5. Generate mutation report")
        print("6. Reload data from CSV")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice == "1":
            patient_id = input("Enter patient ID: ")
            name = input("Enter patient name: ")
            age = int(input("Enter patient age: "))
            diagnosis = input("Enter diagnosis: ")
            
            patient = PatientRecord(patient_id, name, age, diagnosis)
            if db.add_patient(patient):
                print("Patient added successfully")
            else:
                print("Error: Invalid patient data")
                
        elif choice == "2":
            patient_id = input("Enter patient ID: ")
            patient = db.get_patient(patient_id)
            if patient:
                gene_id = input("Enter gene ID: ")
                sequence = input("Enter gene sequence: ")
                mutation_status = input("Enter mutation status (or press Enter if unknown): ")
                
                gene_sequence = GeneSequence(gene_id, sequence, mutation_status or None)
                if gene_sequence.validate_sequence():
                    patient.add_gene_sequence(gene_sequence)
                    db.save_database()
                    print("Gene sequence added successfully")
                else:
                    print("Error: Invalid sequence")
            else:
                print("Error: Patient not found")
                
        elif choice == "3":
            patient_id = input("Enter patient ID: ")
            patient = db.get_patient(patient_id)
            if patient:
                print(f"\nPatient ID: {patient.patient_id}")
                print(f"Name: {patient.name}")
                print(f"Age: {patient.age}")
                print(f"Diagnosis: {patient.diagnosis}")
                print("Gene Sequences:")
                for gene_id, sequence in patient.gene_sequences.items():
                    print(f"  {gene_id}: {sequence.mutation_status or 'No mutation detected'}")
            else:
                print("Error: Patient not found")
                
        elif choice == "4":
            diagnosis = input("Enter diagnosis to search: ")
            patients = db.query_by_diagnosis(diagnosis)
            if patients:
                print(f"\nFound {len(patients)} patients with diagnosis '{diagnosis}':")
                for patient in patients:
                    print(f"  {patient.patient_id}: {patient.name}")
            else:
                print("No patients found with that diagnosis")
                
        elif choice == "5":
            report = AnalysisTool.generate_mutation_report(db)
            print("\nMutation Report:")
            print(report)
            
        elif choice == "6":
            try:
                db = CancerGenomicsDatabase(csv_path=csv_path)
                print("Data reloaded successfully")
            except Exception as e:
                print(f"Failed to reload data: {e}")
                
        elif choice == "7":
            print("Exiting system...")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()