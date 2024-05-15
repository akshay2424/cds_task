import os
import csv

def csv_file_exists(output_folder, csv_filename):
    return os.path.exists(os.path.join(output_folder, csv_filename))

# Function to read data from .dat files and consolidate into a single CSV file
def convert_dat_to_csv(dat_folder, output_folder):
    unique_emails = set()
    result_data = []
    result_csv_filename = 'result.csv'
    result_csv_filepath = os.path.join(output_folder, result_csv_filename)

    # Check if result CSV file already exists, if not create a new one
    if not csv_file_exists(output_folder, result_csv_filename):
        with open(result_csv_filepath, 'w', newline='') as result_csv:
            writer = csv.writer(result_csv)
            writer.writerow(['id', 'first_name', 'last_name', 'email', 'job_title', 'basic_salary', 'allowances'])

    # List all .dat files in the folder
    dat_files = [f for f in os.listdir(dat_folder) if f.endswith('.dat')]

    for dat_file in dat_files:
        with open(os.path.join(dat_folder, dat_file), 'r') as file:
            data = file.readlines()

        # Parse data from .dat file, skipping header row
        parsed_data = [line.strip().split('\t') for line in data[1:]]

        # Add parsed data to result_data and unique_emails
        for row in parsed_data:
            email = row[3]
            if email not in unique_emails:
                unique_emails.add(email)
                result_data.append(row)

    # Append new data to result CSV file
    with open(result_csv_filepath, 'a', newline='') as result_csv:
        writer = csv.writer(result_csv)
        for row in result_data:
            writer.writerow(row)

    # Calculate footer details
    try:
        basic_salaries = [int(row[5]) for row in result_data]
        allowances = [int(row[6]) for row in result_data]
        total_salaries = [basic + allowance for basic, allowance in zip(basic_salaries, allowances)]
        sorted_salaries = sorted(set(total_salaries))

        second_highest_salary = sorted_salaries[-2] if len(sorted_salaries) > 1 else None
        average_salary = sum(total_salaries) / len(total_salaries) if len(total_salaries) > 0 else None

        # Append footer to result CSV file
        with open(result_csv_filepath, 'a', newline='') as result_csv:
            writer = csv.writer(result_csv)
            writer.writerow(['', '', '', '', '', '', ''])
            writer.writerow(['', '2nd Highest Salary', '', '', '', second_highest_salary, ''])
            writer.writerow(['', 'Average Salary', '', '', '', average_salary, ''])
    except (ValueError, IndexError):
        print("Error calculating footer details.")

# Example usage
dat_folder = '/home/hp/Documents/CDS_Task'  # Replace 'input_folder' with your actual input folder path
output_folder = '/home/hp/Documents/CDS_Task'  # Replace 'output_folder' with your desired output folder path

convert_dat_to_csv(dat_folder, output_folder)
