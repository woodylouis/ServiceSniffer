import getThreddsURL








try:
    f = open(input("Please enter the path for the files that contains address: "), "r")
    network = f.read()
except:
    print("Please enter a valid file path")

