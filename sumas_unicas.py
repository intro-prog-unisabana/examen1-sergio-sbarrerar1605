nums = [0, 2, 4, 6]  

# Tu código:

sumas = set()

for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
        suma = nums[i] + nums[j]
        sumas.add(suma)

resultado = list(sumas)

print(resultado)