import unittest

from core.replies_filters.regexp_tasks_complete_common import match as match_common
from core.replies_filters.regexp_tasks_complete_en import match as match_en
from core.replies_filters.regexp_tasks_complete_ua import match as match_ua


class TestTaskCompletingCommands(unittest.TestCase):
    def test_common_short_commands_matching(self):
        matching_candidates = [
            #
            # Plus signs.
            # ... (multiple pluses are supported)
            #
            "+",
            "++",
            "+++",
            #
            # Thumb up
            #
            "👍",
            "👍👍"      # Multiple emojis in a row.
            "👍🏻",
            "👍🏻👍🏻",     # Multiple emojis in a row.
            "👍🏼",
            "👍🏽",
            "👍🏾",
            "👍🏿",
            # ---
            "👍.",
            "👍🏻.",
            "👍🏼.",
            "👍🏽.",
            "👍🏾.",
            "👍🏿.",
            # ---
            ".👍",
            ".👍🏻",
            ".👍🏼",
            ".👍🏽",
            ".👍🏾",
            ".👍🏿",
            #
            # OK hand
            #
            "👌",
            "👌🏻",
            "👌🏼",
            "👌🏽",
            "👌🏾",
            "👌🏿",
            # ---
            "👌.",
            "👌🏻.",
            "👌🏼.",
            "👌🏽.",
            "👌🏾.",
            "👌🏿.",
            # ---
            ".👌",
            ".👌🏻",
            ".👌🏼",
            ".👌🏽",
            ".👌🏾",
            ".👌🏿",
            #
            # OK (signal)
            #
            "🆗",
            "✅",
            "☑️",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_common(0, input.lower()))

    def test_ua_short_commands_matching(self):
        matching_candidates = [
            #
            # ОК in different forms
            # (UA keyboard layout)
            #
            "ок",
            "ок.",  # + punctuation.
            "ок ",  # + trailing space.
            " ок",  # + leading space.
            "ОК",  # + upper case.
            "Ок",  # + mixed case.
            "к"  # Sometimes users make a typo (к instead of ок).
            "Окей",
            "ОКЕЙ",
            "ОКЕЙ ",
            "ОКЕЙ.",
            "ОКЕЙ!",
            "окей",
            #
            # Зроблено in different forms
            # (UA keyboard layout)
            #
            "Зроблено",
            "Зроблено!",  # + punctuation.
            "Зроблено.",  # + punctuation.
            "Зроблена",  # (задача зроблена)
            "Зроблена!",  # (задача зроблена) + punctuation
            "Зроблений" # (наприклад, дзвінок зроблений)
            "ця вже зроблена",
            "ця насправді вже зроблена",
            "цю вже давно зробив",
            #
            # Зробив/Зробила in different forms
            # (UA keyboard layout)
            #
            "зробив!",
            "зробила!",
            #
            # Готово/Готова in different forms
            # (UA keyboard layout)
            #
            "Готово",
            "готова",
            "ця готова",
            "ця вже готова",
            "ця насправді готова",
            "готова вже",
            "вже готова",
            "готова і закрита",
            "готово і закрито",

            #
            # Done in different forms
            # (UA)
            #
            "Дан",  # En: Done
            "Дан.",  # En: Done + punctuation.
            "Дан ",  # En: Done + punctuation.

            # "Чекни" і варіації
            "Чекни", 
            "Чекни.",
            "Цю чекни",
            "Чекни цю.",
            "Цю можна чекнути" 
            "Цей чекнутий"
            "Ця чекнута"
            "Ця вже чекнута"

            # 
            # "Закрий" і варіації
            "Закрий",
            "Закрий.",
            "Цю закрий",
            "Цю можна закрити",
            "Ця закрита",
            "Ця вже закрита",
            "Ця насправді закрита",
            "Ця закрита вже",
            "Вже закрита",
            "Ця закрита і готова",
            "Ця закрита і вже готова",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_ua(0, input.lower()))

    def test_ua_phrases_matching(self):
        matching_candidates = [
            # "Зроблено" і варіації
            "Познач як зроблено",
            "Ця зроблена",
            "Ця вже зроблена",
            "Цю вже зробив колись",
            "Ця насправді зроблена",
            "Цю задачу зроблено",
            "Зроблена вже",
            "Вже зроблена",
            # "Готово" і варіації
            "Вже готова",
            "Готова вже",
            "Наспрадві готова",
            "Давно готова",
            "Готова і закрита",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_ua(0, input.lower()))

    def test_en_short_commands_matching(self):
        matching_candidates = [
            "done",
            "done.",
            "Done",
            " done",
            "done ",
            "DONE",
            "complete",
            "  complete",
            "complete   ",
            "Complete",
            "COMPLETE",
            "completed",
            "completed   ",
            "completed.",
            "ok",
            "ok,",
            "OK",
            " ok",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_en(0, input.lower()))

    def test_en_phrases_commands_matching(self):
        matching_candidates = [
            #
            # OK and variations.
            "this is ok",
            "this one ok",
            "this one is ok",
            "ok already",
            "ok and done",
            "ok, done",
            "ok, closed",
            "ok close",
            #
            # Done and variations.
            "Mark this as done",
            "Mark this as done.",   # With punctuation. 
            "Mark this one as done",
            "Mark this done",
            "This is done",
            "This is already done",
            "This was done already",
            "This is actually done",
            "This task is done",
            "Done already",
            "Already done",
            "Already done and closed",
            #
            # Close(d) and variations.
            "This one is closed",
            "Closed already",
            "Already closed",
            "This is already closed",
            "close this one",
            "close this task",
            "close and complete",
            #
            # Checked and variations
            #
            "Checked",
            "checked.",
            "Checked!",
            "checked,",
            "Check this",
            "Check this.",
            "Check this!",
            "Check this,",
            "This is checked",
            "This is checked.",
            "This is checked!",
            "This is checked,",
            "This one is checked",
            "This one is checked.",
            "This one is checked!",
            "This one is checked,",
            #
            # Check and variations
            "Check",
            "Check.",
            "Check!",
            "Check,",
            "Check it",
            "Check it.",
            "Check it!",
            "Check it,",
            "Check this",
            "Check this.",
            "Check this!",
            "Check this,",
            "This is check",
            "This is check.",
            "This is check!",
            "This is check,",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_en(0, input.lower()))
