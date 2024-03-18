import sys #to read command line arguments
import os #to read working directory and list its contents
import csv #to create a CSV file of the CUI Regulations found
import re #regex searching
import fitz #pip install PyMuPDF

#tool for building accurate regex for pattern searching: https://pythex.org/

def get_file_type(file_name): #function to get file type
    file_pattern = r"(\.txt|\.pdf)"
    file_type_match = re.search(file_pattern, file_name)
    try:
        file_type = file_type_match.group(0) #if file is .txt or .pdf continue
    except AttributeError: #if file is not .txt or .pdf, display following message and quit:
        print(f'\nFile type not supported!!\nPlease only use .txt or .pdf files!!\n')
        quit()
    return file_type

def main():
    file_name = sys.argv[1] #file_name == the first argument called on the command line after python RLBuilder.py
    file_type = get_file_type(file_name)

    current_directory = os.getcwd() #first get working directory
    files_in_dir = os.listdir(current_directory) #list out all files in working directory

    regulation_pattern = r"\d* USC [\d.()\-\w]* [\d.()\-\w]* [\d.()\-\w]*|\d* USC [\d.()\-\w]* [\d.()\-\w]*|\d* USC [\d.()\-\w]*|\d* CFR [\d.()\-\w,]* [\d.()\-\w,]* [\d.()\-\w,]* [\d.()\-\w]* [\d.()\-\w]*|\d* CFR [\d.()\-\w,]* [\d.()\-\w]* [\d.()\-\w]* [\d.()\-\w]*|\d* CFR [\d.()\-\w,]* [\d.()\-\w]* [\d.()\-\w]*|\d* CFR [\d.()\-\w]* [\d.()\-\w]*|\d* CFR [\d.()\-\w]*|FAR [\d.()\-\w]*|FAR [\d.()\-\w]* [\d.()\-\w]*|DFARS [\d.()\-\w]*|DFARS [\d.()\-\w]* [\d.()\-\w]*|\d* FR [\d.()\-\w]* [\d.()\-\w]* [\d.()\-\w]*|NATO [\d.()\-\w]*|Intelligence Community Directive \d*|Federal Rules of \w* \w* [\d.()\-\w]*|\d* Federal Register \d*|Executive Order \d*|HSPD \d*|NSPM \d*|FinCen BSA|GSA PBS \w* [\d.]*|P.L. [\d\-]*|OMB \w* [\w\-]* [\w]* [\d.]*|OMB \w* [\w\-]*|OMB [\w\-]*|IRS Publication \d*|United States Constitution, Article \d, Section \d|Provisional Approval [\d\-]*|Federal Continuity Directive \d*|Presidential Policy Directive \d*|United States Security Authority for NATO, Instruction [\d\-]*|The Risk Management Process for Federal Facilities: An Interagency Security Committee Standard|US Attorney's Manual"

    if file_name in files_in_dir: #search for the contract in the current working directory (where you ran the python script)

        if file_type == '.txt': #if txt
            file = open(file_name, 'r') #open file and read only
            content = file.read() #content will hold all text from .txt file
            matches = re.findall(regulation_pattern, content) #search content for regulation matches
            file.close() #close file when finished

        elif file_type == '.pdf': #if pdf
            file = fitz.open(file_name) #open file
            content = '' #initialize content string
            for page in file: #iterate through each pdf file page
                content += page.get_text() #add extracted text to content string
            matches = re.findall(regulation_pattern, content) #search content for regulation matches
            file.close() #close file when finished
            
    else:
        print(f'\nFile not found in current directory: {current_directory}\nPlease navigate to directory where {file_name} is located and try running {sys.argv[0]} again!\n')
        quit()

    registry_dict = {} #dictionary for storing each key(regulation), value (category) pair
    with open("CUI Registry.csv", newline='') as registry_file: #open CUI Registry.csv
        registry = csv.DictReader(registry_file) #create an iterable csv.DictReader object out of it's contents
        for row in registry: #iterate through each row
            regulation = row['Regulation'] #regulation will be the key
            category = row['Category'] #category will be the value
            registry_dict[regulation] = category #append each key,value pair to registry_dict dictionary
        
    with open(f'{file_name.split(".")[0]}_CUI_Reg_list.csv', 'w', newline='') as file: #create new csv file and name it file_name_CUI_Reg_List (will remove .filetype)
            writer = csv.writer(file) #begin writing to CSV file
            writer.writerow(['Regulation','CUI Category (if applicable)']) #first row will contain 'Regulation' and 'CUI Category (if applicable) columns

            for match in matches: #iterate through each match found from imported file
                match = match.rstrip() #delete trailing whitespace that sometimes occurs with PDF's
                if match not in registry_dict.keys():
                    writer.writerow([match,"CONFIRM NOT A MATCH!"])
                else:
                    for reg in registry_dict: #iterate through each key value in registry_dict dictionary
                        if reg == match: #if match from imported file matches key (regulation) from dictionary, then write the following row:
                            writer.writerow([match,registry_dict[reg]]) #write the match, and the corresponding CUI Category

                

    print(f'\n{file_name.split(".")[0]}_CUI_Reg_List.csv successfully created!\n')

if __name__=="__main__":
    main()

#Created by Dustin Mobley
#Purpose: assist organizations determine what CUI they may be handling or creating by skimming through contracts and 
#compiling a list of relevant regulations and their respective CUI category
