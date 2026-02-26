# Tu código:
PA = float(input())
horas = int(input())
Saber_Pro = int(input())
BI = int(input())

if BI == 1:
    print(True)
elif PA >= 3.5 and horas >= 100 and Saber_Pro >= 260:
    print(True)
else:
    print(False)