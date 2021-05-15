start = '\033['

for i in range(100):
    print i, start + str(i) + 'm' + "Hello, World!" + '\033[0m]'

