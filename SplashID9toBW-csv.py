# SplashID9toBW-csv.py by Clif Kranish 2025  
# Download from https://github.com/ckran/SplashWarden
# Format conversion tool to read SplashId Pro 9 CSV and generate a Bitwarden CSV import file.
# Based on SplashIDtoBW-csv.py by Glenn Seaton. Revised to process the new format 
# Data is now exported with three columns of data for each field: value, label, type 
# This will convert all fields, but does not include any attached files 
#
# Splash Id supports many types of entries, each with its own unique list of fields 
# Only the fields in new_columns (see below) are included in bitwarden 
# Additional fields can be embedded in the "fields" field.
# This program looks for some common fields: account, routing, pin, etc. 
# Amy other fields are recreated as Field3, Field4, ... Field0
# The Date when that SplashId record was updated will have the field name "Last_Updated"
#
'''
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 '''
import csv 
import json
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Function to get input file from the user
def get_input_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select the SplashId CSV file to convert:",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    return file_path

print("Convert SplashId csv to Bitwarden csv format.")
print('To import into Bitwarden select file format "Bitwarden (csv)".')

# Define input and output CSV file paths
# Ask the user to select an input file
input_file = get_input_file()
output_file = 'output.csv'

# Column names based on CSV file produced by Splash ID Pro 9 
column_names = [
    'category', 'type', 'name', 
    'field 1', 'field 1 label', 'field 1 type',
    'field 2', 'field 2 label', 'field 2 type', 
    'field 3', 'field 3 label', 'field 3 type', 
    'field 4', 'field 4 label', 'field 5 type', 
    'field 5', 'field 5 label', 'field 5 type', 
    'field 6', 'field 6 label', 'field 6 type', 
    'field 7', 'field 7 label', 'field 7 type', 
    'field 8', 'field 8 label', 'field 8 type', 
    'field 9', 'field 9 label', 'field 9 type', 
    'note 1', 'create timestamp', 'update timestamp', 'favorite', 'syncable'
]

# New column names based on layout for bitwarden CSV file. Any other fields are assigned within 'fields' 
new_columns = [
    'folder', 'favorite', 'type', 'name', 'notes', 'fields',
    'reprompt', 'login_uri', 'login_username', 'login_password', 'login_totp'
]


# Read and process the CSV
with open(input_file, mode='r', newline='') as infile:
    #reader = csv.DictReader(infile)
    reader = csv.DictReader(infile, fieldnames=column_names)
    # Skip the header row
    next(reader)
   
    # Prepare data for output
    output_data = []
    for row in reader:

        # Assign value for account when used 
        if row['field 5 label'] == 'Account':
            account = row['field 5']         
        elif row['field 4 label'] == 'Account':
            account = row['field 4'] 
        elif row['field 3 label'] == 'Account':
            account = row['field 3']
        elif row['field 1 label'] in  ['Account' , 'Number', 'Card', 'Card #', 'Policy #'] :
            account = row['field 1']
        else:
            account = ''
       
        # Assign value for login username when used 
        if row['field 1 label'] in  ['Username' , 'User', 'Userid', 'User ID'] :
            username = row['field 1']
        elif row['field 3 label'] in  ['Userid' , 'Username'] :
            account = row['field 3']   
        else:
            username = ''

        # Assign value for login password when used
        if row['field 2 label'] == 'Password' :
            password = row['field 2']
        elif row['field 4 label'] == 'Password' :
            password = row['field 4']
        elif row['field 5 label'] == 'Password' :
            password = row['field 5']
        else:
            password = ''

        # Reformat last update withouth T, Z and Milliseocnds to make it readable       
        if row['update timestamp'] != '' :
            lastupdate = datetime.strptime(row['update timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ").replace(microsecond=0).strftime("%Y-%m-%d %H:%M:%S") 
        else :
            lastupdate = '' 
                
                 
        # Create a dictionary for each 'fields' entry as key-value pairs
        # Blank out fieldx values already explicitly named 
        fields = {
            'account': account ,
            'routing' : row['field 6'] if row['field 6 label'] == 'Routing' else '' ,        
            'pin' : row['field 2'] if row['field 2 label'] == 'PIN' else '' , 
            'field3': row['field 3'] if row['field 3 label'] not in ['URL','Account','Userid'] else '',
            'field4': row['field 4'] if row['field 4 label'] not in ['Account','Password'] else '',
            'field5': row['field 5'],
            'field6': row['field 6'] if row['field 6 label'] != 'Routing' else '',
            'field7': row['field 7'],
            'field8': row['field 8'],
            'field9': row['field 9'],
            'Last_Updated': lastupdate
        }
        # Filter out any fields with blank values
        filtered_fields = {k: v for k, v in fields.items() if v.strip()}
        #
        # Filter brackets and  single quotes from array
        # replace comma separator with newline character
        fieldsout = str(filtered_fields)
        fieldsout = fieldsout.replace("{",'')
        fieldsout = fieldsout.replace("}",'')
        fieldsout = fieldsout.replace("'","")
        fieldsout = fieldsout.replace(",","\n")

               
        # SplashId export Vertical Tab as new line in Notes Field
        # Replace Vertical Tab character with  NewLine character
        # notesfield = row['notes 1']
        # notesfield = notesfield.replace("\x0B","\n" )

             
        # Map new columns to row values, with fields as JSON-like text
        output_row = {
            'folder': row['type'],
            'favorite': '',  # Placeholder for undefined column
            'type': 'login', # row['type'],
            'name': row['name'],
            'notes': '',  # notesfield,
            'fields': fieldsout,  # Convert fields dictionary to string
            'reprompt': '',  # Placeholder for undefined column
            'login_uri': row['field 3'] if row['field 3 label'] == 'URL' else '' , 
            'login_username': username ,
            'login_password': password , 
            'login_totp': ''  # Placeholder for undefined column
        }
        output_data.append(output_row)

        # Dump some records for debugging  
        # if row['name'][0] == 'A':
        #    pretty_json = json.dumps(output_row, indent=4)
        #    print(pretty_json)            


# Write to the new CSV file
with open(output_file, mode='w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=new_columns)
    writer.writeheader()
    writer.writerows(output_data)

print(f"Data written to {output_file}")
