
with open('file.txt', 'r') as f:
    rows = f.read()
    text_lines = rows.split('#################')
    for i, row in enumerate(text_lines):
        if 'Apache' in str(row):
            host = text_lines[i - 1]
            # host = host.strip('Host: ')
            #print(host)
    print(len(host))




