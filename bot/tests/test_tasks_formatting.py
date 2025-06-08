import unittest
from unittest.mock import AsyncMock, patch

from core import tasks
from core import stringutils as utils


class TestFormattingTestCase(unittest.IsolatedAsyncioTestCase):
    @patch("core.tasks.__task_id_to_task_description", new_callable=AsyncMock)
    async def test_tasks_formatting(self, mock__task_id_to_task_description):
        mock__task_id_to_task_description.return_value = "T"
        expected_results = {
            # One task must be replace with task's details.
            "#123": ["1\\. T"],

            # If there is some supportive text, it must be preserved.
            # All the tasks IDs must be replaced with sequential numbers.
            # Tasks details must be added to the end of the message. 
            "You have tasks #123 and #456! Have a nice day!": [
                "You have tasks \\#1 and \\#2\\! Have a nice day\\!",
                "1\\. T",
                "2\\. T",
            ],

            # In case when there is only one task per line (like second sentence) 
            # — it must be cur from the line and task details must be added to the end of the message.
            "You have tasks #123 and #456!\n\nAnd there is one more task #555!": [
                "You have tasks \\#1 and \\#2\\!",
                "1\\. T",
                "2\\. T",
                "And there is one more task 3\\. T\\!",
            ],

            "#123 #345 #678": ["1\\. T", "2\\. T", "3\\. T"],
        }

        for input, expected_result in expected_results.items():
            with self.subTest(input=input, expected_result=expected_result):
                result = await tasks.enrich_ai_response_with_tasks_context(
                    0, input, None
                )
                self.assertEqual(result, expected_result)


class TestFormattingWithAbsentTasksTestCase(unittest.IsolatedAsyncioTestCase):
    @patch("core.tasks.__task_id_to_task_description", new_callable=AsyncMock)
    async def test_tasks_formatting(self, mock__task_id_to_task_description):
        mock__task_id_to_task_description.return_value = None
        expected_results = {
            "#123 #345": ["\\#123", "\\#345"],

            "#123": ["\\#123"],
        }

        for input, expected_result in expected_results.items():
            with self.subTest(input=input, expected_result=expected_result):
                result = await tasks.enrich_ai_response_with_tasks_context(
                    0, input, None
                )
                self.assertEqual(result, expected_result)


class TestReqularExpressions(unittest.TestCase):
    def test_matches_one_line_tasks_separeted_by_space_pattern(self):
        expected_results = {
            "#1 #2 #3": True,
            "#1": False,
            "": False,
            "   #1": False,
            "#1 #2, #3": True,
            "#1, #2, #3": True,
            "#1,#2,#3": True,
        }

        for input, expected_result in expected_results.items():
            with self.subTest(input=input, expected_result=expected_result):
                result = utils.matches_one_line_tasks_list_pattern(input)
                self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
