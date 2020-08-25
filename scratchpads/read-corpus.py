from io import TextIOWrapper
import stanza
import tarfile
import time

stanza.download('es')
nlp = stanza.Pipeline('es')

start_time = time.time()


def print_with_time(message):
    current_time = time.time() - start_time;
    seconds = current_time % 60
    minutes = int(((current_time - seconds) / 60) % 60)
    hours = int((current_time - seconds - (minutes * 60)) / 3600)
    result = ""
    if hours > 0:
        result += str(hours) + ":"
    result += str(minutes).zfill(2) + ":"
    result += str(int(seconds)).zfill(2)
    print("{0} {1}".format(result, message))


file_name = "../data/josecannete-spanish-corpora-raw.tar.bz2"
print_with_time("Enumerating " + file_name)
tar = tarfile.open(file_name, "r|bz2")

tarInfo = tar.next()

while tarInfo is not None:
    if tarInfo.isfile():
        print_with_time("{0} - {1} bytes".format(tarInfo.name, tarInfo.size))

        if (tarInfo.size < 1000):
            tar.extract(tarInfo)
        else:
            file = tar.extractfile(tarInfo)
            text = file.read().decode()
            doc = nlp(text)
            print_with_time("resulting string size was {0} with {1} sentences".format(len(text), len(doc.sentences)))
            file.close()

    tarInfo = tar.next()

tar.close()
