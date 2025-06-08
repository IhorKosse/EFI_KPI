import unittest

from core.stringutils import escape_markdown_v2


class TestFormattingTestCase(unittest.TestCase):
    def test_escape_markdown_v2(self):
        expected_results = {
            "Hello, world!": "Hello, world\\!",
            "Hello, _world_!": "Hello, \\_world\\_\\!",
            "Hello, *world*!": "Hello, \\*world\\*\\!",
            "Hello, [world]!": "Hello, \\[world\\]\\!",
            "Hello, (world)!": "Hello, \\(world\\)\\!",
            "Hello, ~world~!": "Hello, \\~world\\~\\!",
            "Hello, `world`!": "Hello, \\`world\\`\\!",
            "Hello, >world<!": "Hello, \\>world\\<\\!",
            "Hello, #world#!": "Hello, \\#world\\#\\!",
            "Hello, +world+!": "Hello, \\+world\\+\\!",
            "Hello, -world-!": "Hello, \\-world\\-\\!",
            "Hello, =world=!": "Hello, \\=world\\=\\!",
            "Hello, |world|!": "Hello, \\|world\\|\\!",
            "Hello, {.}!": "Hello, \\{\\.\\}\\!",
            "Hello, !world!": "Hello, \\!world\\!",

            # Don't escape already escaped characters.
            "Hello, world\\!": "Hello, world\\!",
        }

        for input, expected_result in expected_results.items():
            with self.subTest(input=input, expected_result=expected_result):
                result = escape_markdown_v2(input)
                self.assertEqual(result, expected_result)

