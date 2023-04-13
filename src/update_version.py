def main():
    with open("../version.txt") as file:
        version = int(file.readline())

    with open("../version.txt", "w") as file:
        print(version+1, file=file)


if __name__ == "__main__":
    main()