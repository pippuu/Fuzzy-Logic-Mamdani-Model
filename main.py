# Inputan : data set berisi 100 data yang memiliki 3 kolom yakni, id, pelayanan, dan makanan
# Outputan : data satu vektor kolom berisi 10 baris angka bernilai integer dari record ID

# Library
import pandas as pd
import numpy as np
import xlsxwriter

class Fuzzy:
    def __init__(self, ling, value):
        self.ling = str(ling)
        self.value = float(value)

class Worthy:
    def __init__(self, idx, value):
        self.idx = idx
        self.value = value

# Imports
def imports():
    # data = pd.read_csv("D:\Alpine\Academic\College\4th Semester\Introduction to AI\Tupros\Tupro 2\default\Tupro-AI-02\restoran.csv")
    # data = pd.read_csv("./default/Tupro-AI-02/restoran.csv")
    data = pd.read_csv("restoran.csv")
    return data

# Insert data
def insertToArray(df):
    arrId = []
    arrServ = []
    arrFood = []
    data = pd.DataFrame(df).to_numpy()
    for i in range(len(data)):
        x = str(data[i])
        a, b, c = x.split(";") 
        a1, a2 = a.split("'")
        arrId.append(int(a2))
        c1, c2 = c.split("'")
        arrServ.append(int(b))
        arrFood.append(int(c1))
    return arrId, arrServ, arrFood

# Fuzzifikasi Service
def fuzzyServ(data):
    temp = []
    if(data < 10):
        a = Fuzzy("Bad", 1)
    elif(data >= 10 and data <= 30):
        b = -(data-30)/(20)
        a = Fuzzy("Bad", b)
        temp.append(a)
        b = (data-10)/(20)
        a = Fuzzy("Average", b)
    elif(data < 40):
        a = Fuzzy("Average", 1)
    elif(data >= 40 and data <= 60):
        b = -(data-60)/(20)
        a = Fuzzy("Average", b)
        temp.append(a)
        b = (data-40)/(20)
        a = Fuzzy("Good", b)
    elif(data < 70):
        a = Fuzzy("Good", 1)
    elif(data >= 70 and data <= 80):
        b = -(data-90)/(20)
        a = Fuzzy("Good", b)
        temp.append(a)
        b = (data-70)/(20)
        a = Fuzzy("Excellent", b)
    elif(data <= 100):
        a = Fuzzy("Excellent", 1)
    temp.append(a)
    return temp

# Fuzzifikasi Food
def fuzzyFood(data):
    temp = []
    if(data < 2):
        a = Fuzzy("Bad", 1)
    elif(data >= 2 and data <= 4):
        b = -(data-4)/(2)
        a = Fuzzy("Bad", b)
        temp.append(a)
        b = (data-2)/(2)
        a = Fuzzy("Average", b)
    elif(data < 6):
        a = Fuzzy("Average", 1)
    elif(data >= 6 and data <= 8):
        b = -(data-8)/(2)
        a = Fuzzy("Average", b)
        temp.append(a)
        b = (data-6)/(2)
        a = Fuzzy("Good", b)
    elif(data <= 10):
        a = Fuzzy("Good", 1)
    temp.append(a)
    return temp

# Inference
def inference(serv, food):
    if((food.ling == "Bad" and serv.ling == "Bad") or
    (food.ling == "Bad" and serv.ling == "Average") or
    (food.ling == "Bad" and serv.ling == "Good") or
    (food.ling == "Bad" and serv.ling == "Excellent") or
    (food.ling == "Average" and serv.ling == "Bad") or
    (food.ling == "Average" and serv.ling == "Average") or
    (food.ling == "Good" and serv.ling == "Bad")
    ):
        eligibility = "Low"
    else:
        eligibility = "High"
    if (food.value < serv.value):
        value = food.value
    else:
        value = serv.value
    a = Fuzzy(eligibility, value)
    return a

# Defuzzificate
def defuzzificate(low, high):
    mid = low
    if (high > mid):
        mid = high
    if (mid >= 0.5):
        mid = 0.5
    sum = ((10+20+30+40)*low + mid*50 + (60+70+80+90+100)*high)/((4*low)+mid+(5*high)) 
    return sum

# Selection Sort
def selectionSort(arr):
    for i in range(len(arr)):
        max = i
        for j in range(i+1, len(arr)):
            if(arr[max].value < arr[j].value):
                max = j
        arr[i], arr[max] = arr[max],  arr[i]
    return arr   

# export to xlsx
def Exports(arr):
    workbook = xlsxwriter.Workbook('peringkat.xlsx')
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    for i in range(10):
        worksheet.write(row, col, arr[i])
        row += 1

    workbook.close()
 
if __name__ == "__main__": 
    df = imports()
    arrId, arrServ, arrFood = insertToArray(df)
    worthArr = []
    finalArr = []
    
    for bruh in range(len(arrId)):
        temp_1 = fuzzyServ(arrServ[bruh])
        for obj in temp_1:
            print(obj.ling, obj.value, sep=' ')

        temp_2 = fuzzyFood(arrFood[bruh])
        for obj in temp_2:
            print(obj.ling, obj.value, sep=' ')

        print("----------------")

        arrLow = []
        arrHigh = []
        for i in range(len(temp_1)):
            for j in range(len(temp_2)):
                valueInf = inference(temp_1[i], temp_2[j])
                if (valueInf.ling == "Low"):
                    arrLow.append(valueInf)
                elif(valueInf.ling == "High"):
                    arrHigh.append(valueInf)

        for obj in arrLow:
            print(obj.ling, obj.value, sep=' ')
        for obj in arrHigh:
            print(obj.ling, obj.value, sep=' ')

        print("----------------")

        max = 0
        if (len(arrLow)>1):
            for i in range(1, len(arrLow)):
                if (arrLow[i].value > arrLow[max].value):
                    max = i
        if (len(arrLow)>0):
            finalLow = arrLow[max]

        max = 0
        if (len(arrHigh)>1):
            for i in range(1, len(arrHigh)):
                if (arrHigh[i].value > arrHigh[max].value):
                    max = i
        if (len(arrHigh)>0):
            finalHigh = arrHigh[max]

        print("----------------")

        if (len(arrLow)>0):
            print(finalLow.ling, finalLow.value, sep=' ')
        if (len(arrHigh)>0):
            print(finalHigh.ling, finalHigh.value, sep=' ')

        if (len(arrLow)<1):
            worthValue = defuzzificate(0, finalHigh.value)
        elif (len(arrHigh)<1):
            worthValue = defuzzificate(finalLow.value, 0)
        else:
            worthValue = defuzzificate(finalLow.value, finalHigh.value)
        print(worthValue)
        worthArr.append(Worthy(bruh, worthValue))
        print("----------------")
    
    finalArr = selectionSort(worthArr)
    for obj in finalArr:
        print(obj.idx, obj.value, sep=' ')

    veryfinalArr = np.array(finalArr)
    arrOfIdx = []
    for obj in veryfinalArr:
        print(obj.idx, obj.value, sep=' ')
        arrOfIdx.append(obj.idx)
    Exports(arrOfIdx)

    