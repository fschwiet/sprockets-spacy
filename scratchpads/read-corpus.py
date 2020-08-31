import io
import itertools
import re
import stanza
import tarfile
import time

from sprocketry.stream_chunker import chunk_stream_by_regex

stanza.download('es')
nlp = stanza.Pipeline('es')
nlp.processors.pop("ner")

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

with tarfile.open(file_name, "r:bz2") as tar:

    tarInfo = tar.next()

    while tarInfo is not None:
        if tarInfo.isfile():
            print_with_time("{0} - {1} bytes".format(tarInfo.name, tarInfo.size))

            if (tarInfo.size > 1000):
                with tar.extractfile(tarInfo) as file:
                    regex = r'\n'
                    chunks = chunk_stream_by_regex(regex, io.TextIOWrapper(file, encoding="utf-8"), 1024)
                    for chunk in itertools.islice(chunks, 20):
                        print_with_time(chunk)

        tarInfo = tar.next()
