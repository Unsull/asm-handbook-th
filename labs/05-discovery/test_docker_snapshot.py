import unittest
from docker_snapshot import parse_docker_lines, differences


class DiscoveryTests(unittest.TestCase):
    def test_parse(self):
        rows = parse_docker_lines('{"ID":"abc", "Names":"web", "Ports":"80/tcp"}\n')
        self.assertEqual(rows[0]["names"], "web")

    def test_differences(self):
        before = [{"id":"a","names":"web"}]
        after = [{"id":"b","names":"web"}]
        diff = differences(before, after)
        self.assertEqual(len(diff["new_instances"]), 1)
        self.assertEqual(len(diff["missing_instances"]), 1)
