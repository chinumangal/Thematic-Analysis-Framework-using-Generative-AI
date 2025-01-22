import os
import csv
import pandas as pd

local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
input_file = os.path.join(local_dir, "Course Outline-Radiology.txt")
output_file = os.path.join(local_dir, "output.csv")

file_path = os.path.join(local_dir, "abcd.txt")

def dataloader(response_file):
    """
    Reads the course outline from a text file and saves it to a CSV file.

    Args:
      response_file: Path to the text file containing the course outline.

    Returns:
      None (saves the output to the specified CSV file).
    """

    try:
        # with open(response_file, 'r') as course_outline:
            # course_outline = f.read() 

    
        fieldnames = ['1.1 Domain', '1.2 Potential AI Use Cases', '1.3 Data in the Domain', 
                            '1.4 Implications of Using AI', '1.5 Additional Resources', 
                            '2.1 Learners and Their Interaction with AI', 
                            '2.2 Instructors', '2.3 Internal Support', '3.1 Learning Outcomes', 
                            '3.2 Assessment', '3.3 Learning Activities'] 
        
        data_dict = {field: "" for field in fieldnames}  # Initialize with empty values
        # Create a mapping of section headers to fieldnames
        section_mapping = {
            '1.1 Domain:': '1.1 Domain',
            '1.2 Potential AI Use Cases': '1.2 Potential AI Use Cases',
            '1.3 Data in the Domain': '1.3 Data in the Domain',
            '1.4 Implications of Using AI': '1.4 Implications of Using AI',
            '1.5 Additional Learning Resources': '1.5 Additional Learning Resources',
            '2.1 Learners and Their Interaction with AI' : '2.1 Learners and Their Interaction with AI', 
            '2.2 Instructors': '2.2 Instructors', 
            '2.3 Internal Support': '2.3 Internal Support', 
            '3.1 Learning Outcomes': '3.1 Learning Outcomes', 
            '3.2 Assessment': '3.2 Assessment',
            '3.3 Learning Activities': '3.3 Learning Activities'
        }
        
    # Read the input file and process it
        with open(input_file, 'r', encoding='utf-8') as file:
            # lines = file.readlines()
        
            # Variable to keep track of the current section
            current_section = None
            
            # Process each line
            for line in file:
                line = line.replace('**', '').strip()  # Remove any leading "*"
                # line = line.strip()
                
                # Check if the line matches any section header
                for section_header, fieldname in section_mapping.items():
                    if line.startswith(section_header):
                        current_section = fieldname
                        # Extract the content for '1.1 Domain' since it has inline data
                        if ':' in section_header:
                            data_dict[current_section] = line.split(':', 1)[1].strip()
                        else:
                            data_dict[current_section] = ''
                        break
                else:
                    # Append content to the current section
                    if current_section:
                        # Add a space between lines to ensure single-row format
                        if data_dict[current_section]:
                            data_dict[current_section] += ' ' + line
                        else:
                            data_dict[current_section] = line

                    # Convert the data_dict into a DataFrame
            df = pd.DataFrame([data_dict])

            # Save the DataFrame to an Excel file
            df.to_csv(output_file, index=False, sep=';')
 

    except Exception as e:
      print(f"Error processing file: {e}")

if __name__ == "__main__":
    dataloader(input_file)