import re
import csv
from collections import Counter

def main():
    with open('covidTrain.csv') as input:
        reader = csv.reader(input)
        next(reader)
        dash = r'-'
        longs = {}
        lats = {}
        cities = {}
        symps = {}
        for row in reader:
            if row[6]!='NaN':
                if row[4] in lats.keys():
                    sum = lats[row[4]][0] + float(row[6])
                    count = lats[row[4]][1] + 1
                    lats[row[4]] = (sum,count)
                else:
                    lats[row[4]] = (float(row[6]),1)
            
            if row[7]!='NaN':
                if row[4] in longs.keys():
                    sum = longs[row[4]][0] + float(row[7])
                    count = longs[row[4]][1] + 1
                    longs[row[4]] = (sum,count)
                else:
                    longs[row[4]] = (float(row[7]),1)


            if row[3]!='NaN':
                if row[4] in cities.keys():
                    cities[row[4]].append(row[3])
                else:
                    cities[row[4]] = [row[3]]

            if row[11]!='NaN':
                symptoms = row[11].strip().split(';')
                if row[4] in symps.keys():
                    symps[row[4]] += (symptoms)
                else:
                    symps[row[4]] = symptoms

        input.seek(0)
        reader = csv.reader(input)
        header = next(reader)
        with open('covidResult.csv', 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(header)
            for row in reader:
                match = re.search(dash,row[1])
                if match:
                    age = row[1].split('-')
                    row[1]=round((int(age[0])+int(age[1]))/2)
                
                for i in range(8,11):
                    date = row[i].split('.')
                    temp = date[0]
                    date[0] = date[1]
                    date[1] = temp
                    fixed = '.'.join(date)
                    row[i]=fixed

                if row[6]=='NaN':
                    row[6] = round(lats[row[4]][0]/lats[row[4]][1], 2)
                
                if row[7]=='NaN':                    
                    row[7] = round(longs[row[4]][0]/longs[row[4]][1], 2)

                if row[3] == 'NaN':
                    count = Counter(cities[row[4]])
                    row[3]=count.most_common(1)[0][0]

                if row[11] == 'NaN':
                    count = Counter(symps[row[4]])
                    row[11]=count.most_common(1)[0][0]

                writer.writerow(row)

main()