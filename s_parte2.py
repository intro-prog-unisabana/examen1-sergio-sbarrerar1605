# Tu código:
contador = 0

for _ in range(10):
    mensaje = input()
    if "s" in mensaje.lower():
        print(True)
        contador += 1
    else:
        print(False)

print(f"{contador}/10 mensajes contenían la letra \"s\"")