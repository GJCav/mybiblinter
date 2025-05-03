"""
This script defines rules for articles.
"""
from typing import Literal
import bibtexparser as btp
from .generic_rules import GenericFieldExistenceCheck
from . import core

class ArticleFieldExistenceCheck(core.Rule):
    """
    Every article entry must have these fields:
      - title
      - author
      - journal
      - year

    They may have these fields:
      - volume
      - number
      - pages
    
    Optionally, the consistency can be required so that if one entry has a type
    of field, all entries must have the same type of field.
    """

    RULE_ID = {"ArticleFieldExistenceCheck", "ART001"}
    MUST_HAVE_FIELDS = {
        "title",
        "author",
        "journal",
        "year",
    }
    MAY_HAVE_FIELDS = {
        "volume",
        "number",
        "pages",
    }

    def __init__(
            self,
            consistency_requirement: Literal["ignore", "warn", "error"] = "warn",
    ):
        self.consistency_requirement = consistency_requirement
        self._checker = GenericFieldExistenceCheck(
            consistency_requirement=consistency_requirement,
            consistency_violation_message_head="Article entries have inconsistent fields.",
            must_have_fields=self.MUST_HAVE_FIELDS,
            may_have_fields=self.MAY_HAVE_FIELDS,
            entry_filter=lambda e: e.entry_type == "article",
            subclass=ArticleFieldExistenceCheck,
        )

    
    def check(self, lib: btp.Library, result: core.CheckResult) -> None:
        self._checker.check(lib, result)
