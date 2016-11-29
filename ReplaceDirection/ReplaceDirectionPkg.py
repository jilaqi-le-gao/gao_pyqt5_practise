"""
This only contains one function for replace target column with another column
"""

def ReplaceDirection(infile, outfile, columnTarget, columnBackup):
    Fin = open(infile, 'r')
    Fout = open(outfile, 'w')

    # skip the useless rows
    for OneLine in Fin:
        splitted = OneLine.split('\t')
        if splitted[0] == "Date/Time":
            # delete useless column here and write header
            splitted.remove(splitted[columnBackup])
            Fout.write('\t'.join(splitted))
            break
        Fout.write(OneLine)

    for OneLine in Fin:
        Fout.write(OneLineReplace(OneLine, columnTarget, columnBackup))

    Fin.close()
    Fout.close()


def OneLineReplace(infoString, columnTarget, columnBackup):
    splitted = infoString.replace('\n','').split('\t')
    if splitted[columnTarget] == '':
        splitted[columnTarget] = splitted[columnBackup]
    splitted.remove(splitted[columnBackup])
    return '\t'.join(splitted)+'\n'


def ReadInFile(filePath, row_number):
    Fin = open(filePath)
    # skip the useless rows
    for OneLine in Fin:
        splitted = OneLine.split('\t')
        if splitted[0] == "Date/Time":
            # delete useless column here and write header
            break

    if splitted[0] != "Date/Time":
        return None
    # found data has useless \n or '' delete it
    while('\n' in splitted):
        splitted.remove('\n')
    while('' in splitted):
        splitted.remove('')


    ret = {'column': len(splitted),
           'row'   : row_number,
           'header': splitted
           }
    i=0
    data_rows = []
    for OneLine in Fin:
        data_rows.append(OneLine.split('\t'))
        i+=1
        if(i>row_number):
            break
    ret['data'] = data_rows

    Fin.close()
    return ret