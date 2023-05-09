import requests


def main():
    with open("../version.txt", "r") as version_file:
        version = int(version_file.readline()) + 1
    requests.post("http://192.168.0.174:8080/admin/loadModel/" + str(version))


if __name__ == "__main__":
    main()
