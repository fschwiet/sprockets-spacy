import re


def chunk_stream_by_regex(regex, text_reader, read_size):
    # iterators over parts of text stream separated by a regular expression without allocating the whole string

    # We'll iterate reads of read_size, splitting by the regular expression regex.  The list
    # element in the split result doesn't end with the regular expression, so we carry it over
    # to the next read as leftover_block.
    leftover_block = ""

    while True:
        next_read = text_reader.read(read_size);
        saw_eof = len(next_read) == 0
        next_substring = leftover_block + next_read

        if len(next_substring) == 0:
            break;

        splits = re.split(regex, next_substring)

        leftover_block = splits.pop() if not saw_eof else ""

        for block in splits:
            yield block

