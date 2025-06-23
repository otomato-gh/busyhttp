import unittest
from busyhttp import application, memBuf

class BusyHttpMemoryTests(unittest.TestCase):
    def setUp(self):
        memBuf.buffer.clear()
        self.client = application.test_client()

    def test_memory_allocation_creates_unique_strings(self):
        self.client.get('/memory/2')
        self.assertEqual(len(memBuf.buffer), 2)
        self.assertNotEqual(id(memBuf.buffer[0]), id(memBuf.buffer[1]))

    def test_memory_free_releases_specified_amount(self):
        self.client.get('/memory/3')
        self.client.get('/memfree/2')
        self.assertEqual(len(memBuf.buffer), 1)

if __name__ == '__main__':
    unittest.main()
