# Program to take average of condifence values from output csv files

import csv
import re

# Function to extract confidence values from the CSV file
def extract_confidence_values(csv_filename):
    confidence_values = []
    with open(csv_filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for item in row:
                # Use regular expression to find confidence values
                match = re.search(r"Confidence: ([0-9.]+)", item)
                if match:
                    confidence_values.append(float(match.group(1)))
    return confidence_values

# Function to calculate the average confidence value
def calculate_average_confidence(confidence_values):
    if confidence_values:
        return sum(confidence_values) / len(confidence_values)
    else:
        return None

# Main function
def main():
    # Prompt the user for the CSV filename
    csv_filename = input("Enter the name of the CSV file (including extension): ")

    # Extract confidence values from the CSV file
    confidence_values = extract_confidence_values(csv_filename)

    # Calculate the average confidence value
    average_confidence = calculate_average_confidence(confidence_values)

    # Output the average confidence value to the terminal
    if average_confidence is not None:
        print(f"Average confidence value: {average_confidence}")
    else:
        print("No confidence values found in the CSV file.")

# Call the main function
if __name__ == "__main__":
    main()
