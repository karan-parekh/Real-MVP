

def read_file(path: str) -> str:
    """
    Reads text from file and returns string
    """

    with open(path, 'r') as file:

        return file.read()


def write_to_file(path: str, data: str):
    """
    Writes the data to file
    """

    with open(path, 'w') as file:

        file.write(data)
