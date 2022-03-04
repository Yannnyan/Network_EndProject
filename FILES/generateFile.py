

def generateFile(size: int, name: str): # size in kilobtyes, name
    filename = name + ".txt"
    with open(filename,"w") as file:
        byt = 0
        while byt <= size * 1024:
            file.write("s")
            byt += 1
            if byt == 1023:
                file.write("\n")

generateFile(1000,"baby_shark")
