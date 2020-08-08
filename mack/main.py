from mack import fs


def main():
    for document in fs.read("enron"):
        print("{} {}".format(document.id, document.name))


if __name__ == "__main__":
    main()
