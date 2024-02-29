# CMMC CUIRegulationList
Python script for skimming through contracts and creating a CSV file containing any matching regulations pertaining to a specific CUI category

Step 1: Open command prompt as administrator
Step 2: Navigate to directory where contract is located (I recommend just creating a folder and placing current current contracts in that folder to read through)
Step 3: Ensure CUI Registry.csv (found in this repository) is located in the same directory as contracts
Step 4: ensure PyMuPDF is installed by running 'pip install PyMuPDF'
Step 5: Use the following syntax while in the same directory as the contract and CUI Registry.cvs: python RLBuilder.py <contract.txt>
Step 6: A new csv file will be created containing any regulations found with a corresponding CUI category called <filename>_CUI_Reg_list.csv

Important Notes:
* Contract must be in .txt or .pdf format to run!
* Regex pattern used for regulation searching isn't the best but it should yield results so long as the regulations in the contracts are in the correct format
