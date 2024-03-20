# CMMC CUI Regulation List Generator
Python script for skimming through contracts and creating an Excel file containing any matching regulations pertaining to a specific CUI category (will also include non-matches that must be verified to not pertain to a specific CUI category)

Usage:
1. Create a new folder
2. Copy all contracts to newly created folder (contracts must be in .pdf or .txt format)
3. Copy CUI Registry.xlsx file (found in this repository) to newly created folder
4. Copy RLBuilder.py script (found in this repository) to newly created folder
5. While having the newly created folder open, hold 'SHIFT' key (Windows device only) and right click anywhere there is empty space within the empty folder
6. A drop down will appear - click 'Open PowerShell window here'
7. A PowerShell prompt will appear
8. Install the necessary packages by entering the following commands into the PowerShell prompt (do not include quotes):
   'pip install openpyxl'
   'pip install PyMuPDF'
10. Once necessary packages are installed, type the following command into the PowerShell prompt (do not inlcude quotes):
    'Python RLBuilder.py'
12. If steps performed correctly you should see a message in the PowerShell prompt stating that the CUI Regulation List.xlsx file has been created successfully
13. Exit out of the PowerShell prompt
14. Open the newly created CUI Regulation List.xlsx file located in the newly created folder
15. Look through CUI Regulation List and ensure any non-matches (highlighted in red) do not relate to a specific CUI Category
    Note: The easiest way to do this is copy the non-match regulation and search for it in the CUI Registry 'Search the Registry' search box (https://www.archives.gov/cui/registry/category-list)
16. Once non-matches have been confirmed to not match a CUI category, remove them from the CUI Regulation List
    
Important Notes:
* Contract must be in .txt or .pdf format to be recognized by script!
* Regex pattern used for regulation searching will likely result in several false positives
