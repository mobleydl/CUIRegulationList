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

    regulation_pattern = r"(DFARS \d*[.-]+\d*[.-]\d+|FAR \d*[.-]+\d*[.-]\d+|\d* CFR Part \d* \- Part \d*|\d* CFR Part \d*\- Part \d*|\d* CFR Part \d*\-Part \d*|\d* CFR Part \d*\.\d*|\d* CFR Part \d* [a-zA-Z]* [A-Z]\([a-z]\)|\d* CFR Part \d*|\d* CFR \d*[.]\d*\([a-z]\)\([0-9]\)\([a-z]\)|\d* CFR \d*[.]\d*\([a-z]\)\([0-9]\)\-\([0-9]\)|\d* CFR \d*[.]\d*\([a-z]\)\([0-9]\)\([a-z]*\)|\d* CFR \d*[.]\d*\([a-z]\) \([0-9]\)\-\([a-z]\)|\d* CFR \d*[.]\d*\([a-z]\)\([0-9]\)\-\([a-z]\)\([0-9]\)|\d* CFR \d*[.]\d*\([a-z]\)\([0-9]\)|\d* CFR \d*[.]\d*\([a-z]\)\-[0-9]\([a-z]\)|\d* CFR \d*[.]\d*\([a-z]\)|\d* CFR \d*[.]\d*\-\d*\([a-z]\)|\d* CFR \d*[.]\d*\-\d*|\d* CFR \d*[.]\d*[a-zA-Z]\([a-z]\)|\d* CFR \d*[a-z]\.\d*\([a-z]\)|\d* CFR \d*[a-z][.]\d*|\d* CFR \d*[.]\d*|\d* CFR \d*[a-z]\.[0-9]|\d* CFR \d*\, Subpart [A-Z]\, Appendix [A-Z]|\d* CFR \d*\, Subpart [A-Z]|\d* CFR \d*|\d* USC Appendix \d[A-Z]\([a-z]\)\(\d*\)\([A-Z]\)|\d* USC Appendix \d[A-Z]\([a-z]\)|\d* USC Appendix \d*\([a-z]\)|\d* USC \d*\([a-z]\)\([0-9]\)\([A-Z]\)\([a-z]*\)\([A-Z]*\)|\d* USC \d*\([a-z]\)\([0-9]\)\([A-Z]\)\([a-z]*\)|\d* USC \d*\([a-z]\)\([0-9]\)\([A-Z]\)|\d* CFR \d*|\d* USC \d*\([a-z]\)\([0-9]\)|\d* USC \d*\([a-z]\)|\d* USC \d*\([0-9]\)|\d* USC \d*[a-z]\([a-z]\)\([0-9]\)\([A-Z]\)|\d* USC \d*[a-z]\([a-z]\)\([0-9]\)|\d* USC \d*[a-z]\([a-z]\)|\d* USC \d*[a-z]\([0-9]\)\([A-Z]\)\([a-z]*\)|\d* USC \d*[a-z]\([0-9]*\)\([A-Z]\)|\d* USC \d*[a-z]\-[0-9]*\([a-z]\)\([0-9]\)|\d* USC \d*[a-z]\-[0-9]*\([a-z]\)|\d* USC \d*[a-z]* [0-9]*[A-Z]\([a-z]\)\([0-9]\)\([A-Z]\)|\d* USC \d*[a-z]* [0-9]*[A-Z]\([a-z]\)|\d* USC \d*[a-z]* [0-9]*\([a-z]\)|\d* USC \d*[a-z]*\-[0-9] [a-z]*\([a-z]\)|\d* USC \d*[a-z]*\-[0-9]\([a-z]\)|\d* USC \d*[a-z]*\-[0-9]|\d* USC \d*[a-z]*|\d* USC \d*|Federal Continuity Directive [0-9]|Presidential Policy Directive [0-9]*|GSA [a-zA-Z]* [A-Z] \d*\.\d*|The Risk Management Process for Federal Facilities: An Interagency Security Committee Standard|P.L. \d*\-\d*|FinCen BSA|Executive Order \d*|Intelligence Community Directive \d*|OMB Circular A-\d* section \d*.\d*|OMB Circular A-\d*|OMB [A-Z]-\d*-\d*|NSPM \d*|HSPD \d*|Federal Rules of Criminal Procedure \d*\([a-z]*\)\([0-9]\)|Federal Rules of Criminal Procedure \d*\([a-z]*\)|Federal Rules of Civil Procedure \d*\([a-z]\)\([0-9]\)|Federal Rules of Civil Procedure \d*\([a-z]\)|US Attorney's Manual|\d* Federal Register \d*|Federal Rules of Evidence Rules \d* and \d*\([a-z]\)|United States Constitution, Article \d*, Section \d*|United States Security Authority for NATO, Instruction \d*\-\d*|NATO [A-Z]\-[A-Z]\(\d*\)\d*|Provisional Approval 2018-09-07|\d* FR \d* Sec. [0-9]\([a-z]\)|IRS Publication \d*)"

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
                for reg in registry_dict: #iterate through each key value in registry_dict dictionary
                    if reg == match: #if match from imported file matches key (regulation) from dictionary, then write the following row:
                        writer.writerow([match,registry_dict[reg]]) #write the match, and the corresponding CUI Category

    print(f'\n{file_name.split(".")[0]}_CUI_Reg_List.csv successfully created!\n')

if __name__=="__main__":
    main()