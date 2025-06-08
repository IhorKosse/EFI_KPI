import unittest

from core.replies_filters.regexp_tasks_delete_common import match as match_common
from core.replies_filters.regexp_tasks_delete_en import match as match_en
from core.replies_filters.regexp_tasks_delete_ua import match as match_ua


class TestTaskClosingCommands(unittest.TestCase):
    def test_common_short_commands_matching(self):
        matching_candidates = [
            #
            # Minus signs.
            # ... (multiple pluses are supported)
            #
            "-",
            "--",
            "---",
            #
            # Thumb up
            #
            "❌",
            "❌.",
            " ❌ ",
            "❌❌"     
            "🚫",
            "🚫🚫",    
            "🗑️",
            "🗑️.",
            " 🗑️ ",
            "✖️",
            "✖️.",
            " ✖️ ",
            "➖",
            "➖ ",
            "➖.",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_common(0, input.lower()))
    
    def test_ua_phrases_matching(self):
        matching_candidates = [
            #
            # Видали і варіації
            "видалити",
            "видалити.",
            " видалити ",
            "цю задачу видалити"
            "видалено",
            "видали",
            "видалити цю",
            "цю можна видалити",
            "цю видали",
            "цю вже видали і закрий",
            "цю задачу вже видали",
            "видалена",
            "ця вже видалена",
            "ця задача видалена насправді",
            #
            # удали (суржик)
            "удали",
            "удали.",
            " удали ",
            "удалено",
            "удалено.",
            " удалено ",
            "удали цю",
            "цю можна удалити",
            "цю удалити",
            "цю вже удали",
            "цю задачу удали",
            #
            # Закрий і варіації
            "закрий",
            "закрий.",
            " закрий ",
            "закрито",
            "закрито.",
            " закрито ",
            "закрий цю",
            "цю можна закрити",
            "цю закрий",
            "цю вже закрий і відміни",
            "цю задачу вже закрий",
            "закрита",
            "ця вже закрита",
            "ця задача закрита насправді",
            #
            # Заверши і варіації
            "заверши",
            "заверши.",
            " заверши ",
            "завершено",
            "завершено.",
            " завершено ",
            "заверши цю",
            "цю можна завершити",
            "цю заверши",
            "цю вже заверши і закрий",
            "цю задачу вже заверши",
            "завершена",
            "ця вже завершена",
            "ця задача завершена насправді",
            #
            # Виконано і варіації
            "виконай",
            "виконай.",
            " виконай ",
            "виконано",
            "виконано.",
            " виконано ",
            "виконай цю",
            "цю можна виконати",
            "цю виконай",
            "цю вже виконай і закрий",
            "цю задачу вже виконай",
            "виконана",
            "ця вже виконана",
            "ця задача виконана насправді",
            #
            # "все" і варіації
            "ця все",
            "все з цим",
            "тут вже все",
            "все",
            "все, закривай",
            #
            # "Не важлива" і варіації
            "не важлива",
            "не дуже важлива",
            "зовсім не важлива",
            "ця насправді зовсім не важлива",
            "не важливо",
            #
            # "Забудь" і варіації
            "забудь",
            "забудь про цю",
            "про цю задачу забудь",
            "забудь і закрий",
            "про цю забудь",
            # 
            # "Не суттєво" і варіації
            "не суттєво",
            "ця не суттєва",
            "ця задача не суттєва",
            "задача не суттєва",
            "несуттєво", # поширена помилка — пропустити пробіл.
            # 
            # Скасуй / Скасувати / Скасовано
            "скасуй",
            "скасуй.",
            " скасуй ",
            "скасовано",
            "скасовано.",
            " скасовано ",
            "скасуй цю",
            "цю можна скасувати",
            "цю скасуй",
            "цю вже скасуй і закрий",
            "цю задачу вже скасуй",
            "скасована",
            "ця вже скасована",
            "ця задача скасована насправді",
            # 
            # Відмінено / Відмінити / Відмінено
            "відмінено",
            "відмінено.",
            " відмінено ",
            "відміни",
            "відміни.",
            " відміни ",
            "відмінити",
            "відмінити.",
            " відмінити ",
            "відмінено цю",
            "цю можна відмінити",
            "цю відмінено",
            "цю вже відмінено і закрий",
            "цю задачу вже відмінено",
            "відмінена",
            "ця вже відмінена",
            "ця задача відмінена насправді",
            #
            # Не потрібно, не потрібна, не потрібно, не потрібні, не потрібен
            # непотрібно, непотрібна, непотрібно, непотрібні, непотрібен
            "не потрібно",
            "не потрібно.",
            " не потрібно ",
            "не потрібна",
            "не потрібна.",
            " не потрібна ",
            "не потрібно цю",
            "ця не потрібна",
            "ця задача не потрібна",
            "не потрібні",
            "не потрібні.",
            " не потрібні ",
            "не потрібен",
            "не потрібен.",
            " не потрібен ",
            "не потрібно цю",
            "непотрібна",
            "непотрібен",
            "непотріб" # :)
            # 
            # Не треба
            "не треба",
            "не треба.",
            " не треба ",
            "не треба цю",
            "ця не треба",
            "ця задача не треба",
            "не треба цю",
            "нетреба",
            "нетреба.",
            " нетреба ",
            "нетреба цю",
            "ця нетреба",
            "ця задача вже нетреба",
            #
            # Не актуально і варації
            "не актуально",
            "не актуально.",
            " не актуально ",
            "неактуально",
            "неактуально.",
            " неактуально ",
            "ця неактуально",
            "неактуальна",
            "неактуальна.",
            " неактуальна ",
            "ця задача неактуальна",
            "ця задача не актуальна",
            "ця задача вже не актуальна",
            "ця задача вже більше не актуальна",
            # 
            # Не має сенсу / немає сенсу
            "не має сенсу",
            "не має сенсу.",
            " не має сенсу ",
            "немає сенсу",
            "немає сенсу.",
            " немає сенсу ",
            # 
            # Втратила сенс / Втратив (дзвінок) сенс
            "втратила сенс",
            "втратив сенс",
            "втратив сенс.",
            " втратив сенс ",
            "задача втратила сенс.",
            "задачі втратили сенс.",
            #
            # "Дропни" і варіації
            "дропни",
            "дропни.",
            " дропни ",
            "дропнуто",
            "дропнуто.",
            " дропнуто ",
            "дропни цю",
            "цю можна дропнути",
            "цю дропни",
            "цю вже дропни і закрий",
            "цю задачу вже дропнуто",
            "дропни задачу",
            "дропни цю задачу",
            "дропнув цей дзвінок"
            #
            # Скасовано
            "скасовано",
            "скасовано.",
            " скасовано ",
            "скасовано цю",
            # 
            # Скасувати, скасувава, скасувала
            "цю можна скасувати",
            "цю скасувати",
            "цю скасувала",
            "цю скасував",
            "цю скасували",
            "цю скасував.",
            "цю скасувала.",
            "цю скасували."
            "цю задачу скасував"
            "задачу скасував"
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_ua(0, input.lower()))

    def test_en_phrases_commands_matching(self):
        matching_candidates = [
            #
            # "del" and variations.
            #
            "del",
            "del.",
            "del..",
            " del ",
            "this del",
            "this.del",
            "this.del.",
            "del this",
            "del.this",
            "del.this.",
            "del this one",
            "del.this.one",
            "del.this one",
            "del.this one..",
            "this one del",
            "this one del.",
            "this.one.del.",
            #
            # "del" in non-formal speaking with punctuation.
            #
            "dell",
            "dell.",
            "dell..",
            " dell ",
            "dell this one",
            "this dell",
            "dell this",
            "this one dell",
            "this one dell.",
            # 
            # "delete" and variations.
            "delete",
            "delete.",
            " delete ",
            "deleted",
            "deleted.",
            " deleted ",
            "this one deleted",
            "this one is deleted",
            "this one has been deleted",
            "this one was deleted,",
              "delete this one",
              "deleted this one",
              "deleted this one..",
            "this one delete",
            "delete this",
            "this one must be deleted",
            # 
            # "remove" and variations.
            "remove",
            "remove.",
            " remove ",
            "removed",
            "removed.",
            " removed ",
            "this one was removed",
            "this one has been removed",
            "this one must be removed",
            "remove this one",
            "removed this one",
            "removed this one..",
            "this one remove",
            "remove this",
            "this one must be removed",
            #
            # "Not needed" and variations.
            "not needed",
            "not needed.",
            " not needed ",
            "no need",
            "no need.",
            " no need ",
            "not necessary",
            "not necessary.",
            " not necessary ",
            "not required",
            "not required.",
            " not required ",
            "not essential",
            "not essential.",
            " not essential ",
            # 
            # "Cancel" and variations
            "cancel",
            "cancel.",
            " cancel ",
            "canceled",
            "canceled.",
            " canceled ",
            "this one canceled",
            "this one is canceled",
            "this one has been canceled",
            "this one was canceled,",
            "cancel this one",
            "canceled this one",
            "canceled this one..",
            "this one cancel",
            "cancel this",
            "this one must be canceled",
            #
            # "Discontinue" and variations.
            "discontinue",
            "discontinue.",
            " discontinue ",
            "discontinued",
            "discontinued.",
            " discontinued ",
            "this one discontinued",
            "this one is discontinued",
            "this one has been discontinued",
            "this one was discontinued,",
            "discontinue this one",
            "discontinued this one",
            "discontinued this one..",
            "this one discontinue",
            "discontinue this",
            "this one must be discontinued",
            #
            # "Erase" and variations.
            "erase",
            "erase.",
            " erase ",
            "erased",
            "erased.",
            " erased ",
            "this one erased",
            "this one is erased",
            "this one has been erased",
            "this one was erased,",
            "erase this one",
            "erased this one",
            "erased this one..",
            "this one erase",
            "erase this",
            "this one must be erased",
            # 
            # "changed my mind" and variations.
            "changed my mind",
            "changed my mind.",
            " changed my mind ",
            "changed my mind!",
            "changed my mind?",
            " changed my mind? ",
            "changed my mind,",
            "changed my mind...",
            " changed my mind...",
            "changed my mind!",
            "changed my mind?!",
            " changed my mind?! ",
            "changed my mind, oops",
            "changed my mind, oops!",
            " changed my mind, oops! ",
            "i have changed my mind",
            "i have changed my mind.",
            "changed mind, sorry"
            #
            # "Abandon" and variations.
            "abandon",
            "abandon.",
            " abandon ",
            "abandoned",
            "abandoned.",
            " abandoned ",
            "this one abandoned",
            "this one is abandoned",
            "this one has been abandoned",
            "this one was abandoned,",
            "abandon this one",
            "abandoned this one",
            "abandoned this one..",
            "this one abandon",
            "abandon this",
            "this one must be abandoned",
            #
            # "Unnecessary" and variations.
            "unnecessary",
            "unnecessary.",
            " unnecessary ",
            "not necessary",
            "not necessary.",
            " not necessary ",
            "not required",
            "not required.",
            " not required ",
            "not essential",
            "not essential.",
            " not essential ",
            "no need",
            "no need.",
            " no need ",
            "this one is unnecessary",
            # 
            # "Retract" and variations.
            "retract",
            "retract.",
            " retract ",
            "retracted",
            "retracted.",
            " retracted ",
            "this one retracted",
            "this one is retracted",
            "this one has been retracted",
            "this one was retracted,",
            "retract this one",
            "retracted this one",
            "retracted this one..",
            "this one retract",
            "retract this",
            "this one must be retracted",
            # 
            # "Deactivate" and variations.
            "deactivate",
            "deactivate.",
            " deactivate ",
            "deactivated",
            "deactivated.",
            " deactivated ",
            "this one deactivated",
            "this one is deactivated",
            "this one has been deactivated",
            "this one was deactivated,",
            "deactivate this one",
            "deactivated this one",
            "deactivated this one..",
            "this one deactivate",
            "deactivate this",
            "this one must be deactivated",
            "deactiv this one"  # short form

            #
            # "Revoke" and variations.
            "revoke",
            "revoke.",
            " revoke ",
            "revoked",
            "revoked.",
            " revoked ",
            "this one revoked",
            "this one is revoked",
            "this one has been revoked",
            "this one was revoked,",
            "revoke this one",
            "revoked this one",
            "revoked this one..",
            "this one revoke",
            "revoke this",
            "this one must be revoked",
            #
            # "Expunge" and variations.
            "expunge",
            "expunge.",
            " expunge ",
            "expunged",
            "expunged.",
            " expunged ",
            "this one expunged",
            "this one is expunged",
            "this one has been expunged",
            "this one was expunged,",
            "expunge this one",
            "expunged this one",
            "expunged this one..",
            "this one expunge",
            "expunge this",
            "this one must be expunged",
            #
            # Terminate and variations.
            "terminate",
            "terminate.",
            " terminate ",
            "terminated",
            "terminated.",
            " terminated ",
            "this one terminated",
            "this one is terminated",
            "this one has been terminated",
            "this one was terminated,",
            "terminate this one",
            "terminated this one",
            "terminated this one..",
            "this one terminate",
            "terminate this",
            "this one must be terminated",
            # 
            # Drop and variations.
            # "Drop" and variations.
            "drop",
            "drop.",
            " drop ",
            "dropped",
            "dropped.",
            " dropped ",
            "this one dropped",
            "this one is dropped",
            "this one has been dropped",
            "this one was dropped,",
            "drop this one",
            "dropped this one",
            "dropped this one..",
            "this one drop",
            "drop this",
            "this one must be dropped",
        ]

        for input in matching_candidates:
            with self.subTest(input=input):
                self.assertTrue(match_en(0, input.lower()))
