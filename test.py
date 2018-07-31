with open('ScanResults/250720181645.txt', 'r') as fileReadObj:
    rows = fileReadObj.read()
    text_lines = rows.split('#################')
    for i, row in enumerate(text_lines):
        if 'Apache' in str(row):
            print(text_lines[i - 1])