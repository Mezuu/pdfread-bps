from cProfile import label
import pdfplumber
import pandas as pd
import re

with pdfplumber.open("doc3.pdf") as pdf:
    for i in range(len(pdf.pages)):
        first_page = pdf.pages[i]
        title = first_page.extract_text()
        table = pd.DataFrame(first_page.extract_table())
        try:
            title = re.search('Tabel[\w\s\n.,\-\(\)]+', title).group()
            print(title)
            # new line
            line = pd.DataFrame([title], index=[0])
            # concatenate two dataframe
            df2 = pd.concat([line, table.ix[:]]).reset_index(drop=True)
        except:
            pass
        for j in table:
            # print(table[j])
            for k in range(len(table[j])):
                try:
                    text = table[j][k]
                    newlinepos = text.rfind('\n')
                    if newlinepos != -1 and newlinepos < len(text)-len('\n'):
                        table[j][k] = text[newlinepos+len('\n'):]
                    if text[len(text)-2] == ' ':
                        table[j][k] = table[j][k][:len(table[j][k])-2]
                    if re.search('[0-9]+\s[0-9]+', table[j][k]):  # type: ignore
                        table[j][k] = table[j][k].replace(
                            ' ', '').replace('.', '')
                    if re.search('-', table[j][k]) and re.search('\D', table[j][k]):
                        table[j][k] = '-'
                    if re.search('[0-9]+', table[j][k]) and re.search('\w', table[j][k]) and re.search('[^()]', table[j][k]):
                        table[j][k] = re.search('[0-9]+', table[j][k]).group()
                except:
                    pass

        table.to_csv(
            'csv/doc-page{}.csv'.format(i), index=False)
