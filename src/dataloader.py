import os
import csv
import pandas as pd

local_dir = os.path.abspath(os.path.join(__file__, "../../data/"))
course_files1 = os.path.join(local_dir, "course_files", "new")
course_output_file = os.path.join(local_dir, "Course_output_data.xlsx")
# processed_data = os.path.join(local_dir, "processed_data10.csv")


def dataloader(course_files, course_output_file):
    
    try:
        for course_file in os.listdir(course_files):
            input_file = os.path.join(course_files, course_file)
            print(input_file)
            if os.path.exists(course_output_file):
                df_existing = pd.read_excel(course_output_file, engine='openpyxl')
                # print(f"existing output file is present")
            else:
                df_existing = pd.DataFrame()
            # df_existing = pd.read_excel(course_output_file)
            
            for col in ['keywords_processed', 'embeddings_processed']:
                if col not in df_existing.columns:
                    print(col)
                    df_existing[col] = ''
        
            fieldnames = ['Serial number', 'Course name', 'Author', 'Date', 'Version','Course_name', 'Cluster', '1.1 Domain', '1.2 Potential AI Use Cases', '1.3 Data in the Domain', 
                                '1.4 Implications of Using AI', '1.5 Additional Learning Resources', 
                                '2.1 Learners and Their Interaction with AI', 
                                '2.2 Instructors', '2.3 Internal Support', '3.1 Learning Outcomes', 
                                '3.2 Assessment', '3.3 Learning Activities', 'keywords_processed','embeddings_processed'] 
            
            data_dict = {field: "" for field in fieldnames}  # Initialize with empty values
            
            # Find the last Serial Number (if the file exists)
            if not df_existing.empty and 'Serial number' in df_existing.columns:
                last_serial_number = df_existing['Serial number'].max()  # Get the highest existing serial number
                # print(last_serial_number)
            else:
                last_serial_number = 0  # If no data, start from 0
            print(f" {last_serial_number} is before {course_file}" )
            # Set the new row's Serial Number
            data_dict['Serial number'] = last_serial_number + 1
            data_dict['Course name'] = f"AI in {course_file}"
            data_dict['Author'] = 'ABC'
            data_dict['Date'] = "28-02-2025"
            data_dict['Version'] = '1.0'
            data_dict['Course_name'] = course_file
            data_dict['keywords_processed'] = 'No'
            data_dict['embeddings_processed'] = 'No'

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
            with open(input_file, 'r', encoding='ISO-8859-1') as file:
                # lines = file.readlines()
            
                # Variable to keep track of the current section
                current_section = None
                
                # Process each line
                for line in file:
                    line = line.replace('**', '').strip()  # Remove any leading "*"
                    line = line.replace('*', '').strip()
                    
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
                        # print(current_section)
                        # Convert the data_dict into a DataFrame
                df_new = pd.DataFrame([data_dict])

                print(df_new)
                # Ensure new data aligns with the existing structure
                if not df_existing.empty:
                    df_new = df_new[df_existing.columns]  # Maintain column order
                # Append new data
                # df_combined = df_existing.append([df_existing, df_new], ignore_index=True)
                df_combined = pd.concat([df_existing, df_new])
                print(f"file saved")
                # Save the combined data to Excel
                df_combined.to_excel(course_output_file, index=False, engine='openpyxl')
        

    except Exception as e:
      print(f"Error processing file: {e}")
    return df_new

if __name__ == "__main__":

    # print("hellp")
    
    df = dataloader(course_files1, course_output_file)