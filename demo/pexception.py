
def initException():
    try:
        i = 1
        print(1/i)
    except:
        print('error occured')
    print("After exception")

if __name__ == "__main__":
    initException()