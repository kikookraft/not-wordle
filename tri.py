
l=[]

with open("res/fr.txt", 'r') as f:
    l.append(f.readline().rstrip())

with open("res/fr.txt", 'w') as f:
    for i in l:
        if len(i)<10:
            f.write(i+"\n")
            print(i)