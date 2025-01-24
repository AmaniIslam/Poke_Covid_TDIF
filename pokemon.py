import csv
from collections import Counter

def one():
    with open('pokemonTrain.csv') as file:
        reader = csv.reader(file)
        next(reader)                              # skip first line of column (field) names
    
        fire = 0
        forty = 0
        for row in reader:         # row will be a list of all column (field) values
            if row[4]=='fire':
                fire+=1
                if (float(row[2])>=40):
                    forty+=1

        with open('pokemon1.txt', 'w') as output:
            output.write("Percentage of fire type Pokemons at or above level 40 = " + str(round(100*(forty/fire))))

def two_three():
    with open('pokemonTrain.csv') as input:
        reader = csv.reader(input)
        next(reader)
    
        atk1 = 0
        aCount1 = 0
        defense1 = 0
        dCount1 = 0
        hp1 = 0
        hCount1 = 0
        atk2 = 0
        aCount2 = 0
        defense2 = 0
        dCount2 = 0
        hp2 = 0
        hCount2 = 0
        weaknesses = {}

        for row in reader:
            if row[4]!='NaN':
                if row[5] in weaknesses.keys():
                    weaknesses[row[5]].append(row[4])
                else:
                    weaknesses[row[5]]=[row[4]]

            if float(row[2]) <= 40:
                if row[6]!='NaN':
                    atk1 += float(row[6])
                    aCount1+=1
                
                if row[7]!='NaN':
                    defense1 += float(row[7])
                    dCount1+=1
                
                if row[8]!='NaN':
                    hp1 += float(row[8])
                    hCount1 +=1

            
            else:
                if row[6]!='NaN':
                    atk2 += float(row[6])
                    aCount2+=1
                
                if row[7]!='NaN':
                    defense2 += float(row[7])
                    dCount2+=1
                
                if row[8]!='NaN':
                    hp2 += float(row[8])
                    hCount2 +=1

        input.seek(0)
        reader = csv.reader(input)
        header = next(reader)
        with open('pokemonResult.csv', 'w', newline='') as output:
            writer = csv.writer(output)
            writer.writerow(header)
            for row in reader:
                if row[4] == 'NaN':
                    count = Counter(weaknesses[row[5]])
                    row[4]=count.most_common(1)[0][0]

                if float(row[2]) <= 40:
                    if row[6]=='NaN':
                        row[6] = round(atk1/aCount1, 1)
                    
                    if row[7]=='NaN':
                        row[7] = round(defense1/dCount1, 1)
                    
                    if row[8]=='NaN':
                        row[8] = round(hp1/hCount1, 1)
                
                else:
                    if row[6]=='NaN':
                        row[6] = round(atk2/aCount2, 1)
                    
                    if row[7]=='NaN':
                        row[7] = round(defense2/dCount2, 1)

                    if row[8]=='NaN':
                        row[8] = round(hp2/hCount2, 1)

                writer.writerow(row)

def four():
    with open('pokemonResult.csv') as input:
        reader = csv.reader(input)
        next(reader)
        personalities = {}
        for row in reader:
            if row[4] in personalities.keys():
                personalities[row[4]].append(row[3])
            else:
                personalities[row[4]]=[row[3]]

        personalities = dict(sorted(personalities.items()))
        
        with open('pokemon4.txt', 'w') as output:
            output.write("Pokemon type to personality mapping:\n")
            for key, values in personalities.items():
                values = list(sorted(values))
                output.write(f"\t{key}: {', '.join(values)}\n")

def five():
    with open('pokemonResult.csv') as input:
        reader = csv.reader(input)
        next(reader)
        total = 0
        count = 0
        for row in reader:
            if row[9]=='3.0':
                total+=float(row[8])
                count+=1
            
        with open('pokemon5.txt', 'w') as output:
            output.write("Average hit point for Pokemons of stage 3.0 = "+str(round(total/count)))

def main():
    one()
    two_three()
    four()
    five()

main()