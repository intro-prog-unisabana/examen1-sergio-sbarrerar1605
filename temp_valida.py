# Tu código:
while True:
    try:
        temp = int(input("Por favor ingresa la temperatura: "))
        if 55 <= temp <= 100:
            print("Entrada válida.")
            break
        else:
            print("Entrada inválida, intenta de nuevo.")
    except:
        print("Entrada inválida, intenta de nuevo.")