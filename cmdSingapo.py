
index = 0
while True:
    if index == 5:
        break
    print("index", index)
    if index == 3:
        index -= 1
        continue
    index += 1