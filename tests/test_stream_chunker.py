import io
import unittest

from sprocketry.stream_chunker import *


class TestCanSplitTextStream(unittest.TestCase):
    def test_can_split_stream(self):
        self.assertEqual(['1', '2', '3'], list(chunk_stream_by_regex(r'\s', io.StringIO("1 2 3"), 1024)))

    def test_can_split_stream_longer_than_read_size(self):
        self.assertEqual(['one', 'two', 'three'], list(chunk_stream_by_regex(r'\s', io.StringIO("one two three"), 4)))

    def test_can_split_with_chunk_longer_than_read_size(self):
        self.assertEqual(['one', 'sixteentonsandwhatdoyouget', 'three'], list(chunk_stream_by_regex(r'\s', io.StringIO("one sixteentonsandwhatdoyouget three"), 4)))


if __name__ == '__main__':
    unittest.main()