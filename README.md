# SE2300-GenomicsDatabase
This system is designed to facilitate the storage, retrieval, and analysis of cancer genomic data. Researchers can input genomic sequences, mutation data, and patient metadata for analysis. The system supports querying, visualization, and reporting functionalities to enhance cancer genomics research.

Features

User Management: Add, update, and delete patient records.

Genomic Data Handling: Store and analyze gene sequences and mutations.

Mutation Analysis: Detect and track cancer-related mutations.

Visualization: Generate bar charts and heatmaps for gene expression analysis.

Data Persistence: Save data in a PostgreSQL database or JSON format.

Command-Line Interface: Simple interactive CLI for users.

Data Import: Load datasets from CSV files.

Error Handling & Validation: Ensures data integrity and proper format.

Installation

Prerequisites

Ensure you have the following installed:

Python 3.8+

pip (Python package manager)

PostgreSQL (Optional, for database storage)

Dependencies

Run the following command to install required Python libraries:
pip install pandas numpy matplotlib seaborn flask

Usage

Running the System

Clone the repository:
https://github.com/jbInf-08/SE2300-GenomicsDatabase.git

Navigate to the project directory:
cd GenomicsDatabase

Run the main program:
python genomics_system.py

Follow on-screen instructions to add, query, and visualize genomic data.

Data Import from CSV

To load the dataset from Kaggle:

Download the cancer genomic dataset (e.g., METABRIC) from Kaggle (https://www.kaggle.com/datasets/raghadalharbi/breast-cancer-gene-expression-profiles-metabric?resource=download)

Save it as METABRIC_RNA_Mutation.csv in the project directory.

Run:
python genomics_system.py --load-csv METABRIC_RNA_Mutation.csv

Testing

To verify system functionality, run:
python version_system.py
This script will check Python version, dependencies, and dataset accessibility.
