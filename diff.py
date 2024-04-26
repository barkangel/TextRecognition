# Program to diff the two file outputs, seeing which file scanned the text more accurately: before or after filter applied

def file_diff(file1_path, file2_path):
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            file1_lines = file1.readlines()
            file2_lines = file2.readlines()

            # Compare line by line
            for i, (line1, line2) in enumerate(zip(file1_lines, file2_lines), start=1):
                if line1 != line2:
                    print(f"Difference found at line {i}:")
                    print(f"File 1: {line1.strip()}")
                    print(f"File 2: {line2.strip()}")
                    print()
            
            # Check for extra lines in file 1
            if len(file1_lines) > len(file2_lines):
                print("Additional lines in File 1:")
                for line in file1_lines[len(file2_lines):]:
                    print(f"File 1: {line.strip()}")
                print()

            # Check for extra lines in file 2
            elif len(file2_lines) > len(file1_lines):
                print("Additional lines in File 2:")
                for line in file2_lines[len(file1_lines):]:
                    print(f"File 2: {line.strip()}")
                print()

            print("Comparison completed.")

    except FileNotFoundError:
        print("File not found. Please provide valid file paths.")


if __name__ == "__main__":
    file1_path = input("Enter the path of the first file: ")
    file2_path = input("Enter the path of the second file: ")
    file_diff(file1_path, file2_path)
