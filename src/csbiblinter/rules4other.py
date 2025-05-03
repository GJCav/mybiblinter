import bibtexparser as btp
from .generic_rules import GenericFieldExistenceCheck
from . import core

class BookFieldExistenceCheck(core.Rule):
    """
    Every book entry must have and only have these fields:
      - title
      - author
      - year
      - publisher
    """

    RULE_ID = {"BookFieldExistenceCheck", "BOOK001"}
    MUST_HAVE_FIELDS = {
        "title",
        "author",
        "year",
        "publisher",
    }
    MAY_HAVE_FIELDS = set()

    def __init__(self):
        self._checker = GenericFieldExistenceCheck(
            consistency_requirement="error",
            consistency_violation_message_head="Book entries have inconsistent fields.",
            must_have_fields=self.MUST_HAVE_FIELDS,
            may_have_fields=self.MAY_HAVE_FIELDS,
            entry_filter=lambda e: e.entry_type == "book",
            subclass=BookFieldExistenceCheck,
        )


    def check(self, lib: btp.Library, result: core.CheckResult) -> None:
        self._checker.check(lib, result)


class MiscFieldExistenceCheck(core.Rule):
    """
    Every misc entry must have and only have these fields:
      - title
      - url
    """

    RULE_ID = {"MiscFieldExistenceCheck", "MISC001"}
    MUST_HAVE_FIELDS = {
        "title",
        "url"
    }
    MAY_HAVE_FIELDS = set()

    def __init__(self):
        self._checker = GenericFieldExistenceCheck(
            consistency_requirement="error",
            consistency_violation_message_head="Misc entries have inconsistent fields.",
            must_have_fields=self.MUST_HAVE_FIELDS,
            may_have_fields=self.MAY_HAVE_FIELDS,
            entry_filter=lambda e: e.entry_type == "misc",
            subclass=MiscFieldExistenceCheck,
        )


    def check(self, lib: btp.Library, result: core.CheckResult) -> None:
        self._checker.check(lib, result)