x = ()

x += ("x", "y")
x += (("a"), ("b"))

print(x)
with open("coords.txt", "w") as f:
    f.write(str(x))
f.close()
