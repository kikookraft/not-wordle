
l=[]

with open("res/fr.txt", 'r') as f:
    for i in f:
        i.rstrip()
        l.append(i)

with open("res/fr.txt", 'w') as f:
    for i in l:
        if len(i)<10 and len(i)>4:
            f.write(i)
            print(i)