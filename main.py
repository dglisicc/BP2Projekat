import csv

dataTable = None
indexTable = None


# ==========================Klase============================
class DataTable:
    def __init__(self, names, data, dCount, fCount):
        self.name = "DataTable"
        self.columnNames = names
        self.data = data

        self.dCount = dCount
        self.fCount = fCount


class BitMapIndex:
    def __init__(self, name, names, data):
        self.name = name
        self.columnNames = names
        self.data = data
        self.indexes = self.createIndexes()

    def createIndexes(self):
        indexes = {}
        values = [x[0] for x in self.data]
        unique = set(values)
        for u in unique:
            index = ""
            for row in self.data:
                if row[0] == u:
                    index += "1"
                else:
                    index += "0"
            indexes[u] = index

        print(indexes)
        return indexes


# ==========================Funkcije=============================

def createDataTable(filename):
    names = None
    data = []
    dCount = 0
    fCount = 0
    with open(filename, 'r') as f:
        names = f.readline().strip().split(',')

        for name in names:
            if name[0] == 'D':
                dCount += 1
            elif name[0] == 'F':
                fCount += 1

        for line in f:
            data.append(line.strip().split(','))

    return DataTable(names, data, dCount, fCount)


def createIndexDict(dataTable):
    indexDict = {}
    for i in range(len(dataTable.columnNames)):
        if dataTable.columnNames[i][0] == 'D':
            # Ime indeksa
            indexName = dataTable.columnNames[i]

            # Imena kolona indeksa
            indexColumnNames = [indexName]
            for j in range(dataTable.fCount):
                indexColumnNames.append(dataTable.columnNames[1 + dataTable.dCount + j])

            # print(indexColumnNames)

            # DATA
            data = []
            for row in dataTable.data:
                dataRow = [row[i]]
                for j in range(dataTable.fCount):
                    dataRow.append(row[1 + dataTable.dCount + j])
                # print(dataRow)
                data.append(dataRow)

            indexDict[indexName] = BitMapIndex(indexName, indexColumnNames, data)

    return indexDict


# ========================Metode=========================
def ANDdata(indexes):
    bitsList = []
    result = ""
    for index in indexes:
        bits = []
        for bit in index:
            bits.append(int(bit))

        bitsList.append(bits)
    for i in range(len(bitsList[0])):
        num = 1
        for j in range(len(bitsList)):
            num &= bitsList[j][i]
        result += str(num)

    print(result)
    return result


def ORdata(indexes):
    bitsList = []
    result = ""
    for index in indexes:
        bits = []
        for bit in index:
            bits.append(int(bit))

        bitsList.append(bits)
    for i in range(len(bitsList[0])):
        num = 0
        for j in range(len(bitsList)):
            num |= bitsList[j][i]
        result += str(num)

    print(result)
    return result


# Funkcija treba da mi najde sve informacije
def search(indexedColumns, searchOP, searchWithIndex):
    indexes = []
    data = []
    if searchWithIndex:
        for index in indexedColumns:
            indexes.append(index[0].indexes[index[1]])

        if len(searchOP) > 1:
            # Ako treba obe operacije
            andRes = ANDdata(indexes)
            orRes = ORdata(indexes)
            for i in range(len(andRes)):
                if andRes[i] == "1" or orRes[i] == "1":
                    if dataTable.data[i] not in data:
                        data.append(dataTable.data[i])

        else:
            # Ako treba pojedinacna operacija
            if searchOP[0] == "AND":
                andRes = ANDdata(indexes)
                for i in range(len(andRes)):
                    if andRes[i] == "1":
                        data.append(dataTable.data[i])
                # print(data)
                return data


            elif searchOP[0] == "OR":
                orRes = ORdata(indexes)
                for i in range(len(orRes)):
                    if orRes[i] == "1":
                        data.append(dataTable.data[i])
                # print(data)
                return data
    else:
        if searchOP[0] == "AND":
            flag = True
            for d in dataTable.data:
                for index in indexedColumns:
                    if index[1] not in d:
                        flag = False
                if flag:
                    data.append(d)
                else:
                    flag = True
            print(data)
            return data


        elif searchOP[0] == "OR":
            for d in dataTable.data:
                for index in indexedColumns:
                    if index[1] in d:
                        data.append(d)
                        break
            print(data)
            return data

# Funkcija treba da uradi nesto sa datim informacijama


def agreagate(operation, data):
    # Formatiranje neindeksiranih kolona
    print(data)

    factColumns = []
    for i in range(dataTable.fCount):
        fCol = []
        for d in data:
            fCol.append(d[1+dataTable.dCount+i])
        factColumns.append(fCol)
    print(factColumns)

    if operation == "min":
        for fact in factColumns:
            print(min(fact))
    elif operation == "max":
        for fact in factColumns:
            print(max(fact))
    elif operation == "avg":
        for fact in factColumns:
            sum = 0
            for f in fact:
                sum += int(f)
            print(sum/len(fact))
    elif operation == "sum":
        for fact in factColumns:
            sum = 0
            for f in fact:
                sum += int(f)
            print(sum)
    elif operation == "count":
        for fact in factColumns:
            cnt = 0
            for f in fact:
                cnt += 1
            print(cnt)
    else:
        print("Uneta nepostojeca agregatna funckija!")
        return None


# ===========================Main================================
if __name__ == '__main__':
    dataTable = createDataTable("SchemaAndData.csv")
    indexDict = createIndexDict(dataTable)

    for x, y in indexDict.items():
        print(x)
        print(y.data)
        print(y.indexes)

    # Parametri pretraga
    indexedColumns = [[indexDict["D1"], "A"], [indexDict["D2"], "X"]]
    searchOP = ["OR"]

    print("DALJE")
    searchData = search(indexedColumns, searchOP, False)

    agreagate("avg", searchData)
