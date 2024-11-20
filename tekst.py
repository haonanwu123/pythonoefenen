numbers = {"int1": 1, "int2": 2, "int3": 3}

x = numbers.get("int2", 0) + 5
y = numbers.get("int1",7) - 1
z = numbers.get("int4", 5) - 1 
print(x,y,z)