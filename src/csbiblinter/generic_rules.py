from typing import Callable, Literal
import bibtexparser as btp
import bibtexparser.model as bib_model
from . import core


class GenericFieldExistenceCheck(core.Rule):
    """
    The generic field existence rule checks that, for a type of entries
    (specified by `entry_filter`), if all the entries have the set of fields
    specified in `must_have_fields`, and rejects the entries that have fields
    that are not in `must_have_fields` and `may_have_fields`.

    Optionally, the consistency can be required so that if one entry has a type
    of field, all entries must have the same type of field.

    The rule class is generic and should not be used directly. Instead, use the
    `ProceedingsFieldExistenceCheck` and `ArticleFieldExistenceCheck`.
    """

    RULE_ID = {"GenericFieldExistenceCheck", "GEN001"}

    def __init__(
        self,
        consistency_requirement: Literal["ignore", "warn", "error"] = "warn",
        consistency_violation_message_head: str = "Inconsistent fields found.",
        must_have_fields: set[str] = set(),
        may_have_fields: set[str] = set(),
        entry_filter: Callable[[bib_model.Entry], bool] = lambda x: True,
        subclass: type[core.Rule] = None,
    ):
        self.consistency_requirement = consistency_requirement
        self.consistency_violation_head = consistency_violation_message_head
        self.must_have_fields = must_have_fields
        self.may_have_fields = may_have_fields
        self.entry_filter = entry_filter
        self.subclass = subclass

        self.valid_fields = must_have_fields | may_have_fields | {"_bypass_rule"}

        self.subclass = subclass if subclass else GenericFieldExistenceCheck

    def check(self, lib: btp.Library, result: core.CheckResult) -> None:
        entries = [e for e in lib.entries if self.entry_filter(e)]

        # MUST HAVE and MAY HAVE fields check
        for entry in entries:
            for field in self.must_have_fields:
                if field not in entry:
                    result.errors.append(
                        core.FieldNotFound(
                            field_name=field,
                            related_entry=entry,
                            created_by=self.subclass,
                        )
                    )

            for field in entry.fields:
                if field.key not in self.valid_fields:
                    result.errors.append(
                        core.InvalidFieldType(
                            related_field=field,
                            related_entry=entry,
                            created_by=self.subclass,
                            reason=(
                                "Only the following fields are allowed: "
                                + ", ".join(self.valid_fields)
                                + ". "
                            ),
                        )
                    )

        # Consistency check
        if self.consistency_requirement != "ignore":
            occurred_fields = {f.key for entry in entries for f in entry.fields}
            if '_bypass_rule' in occurred_fields:
                occurred_fields.remove('_bypass_rule')

            inconsistent_entries = []
            for entry in entries:
                entry_fields = {f.key for f in entry.fields}
                if '_bypass_rule' in entry_fields:
                    entry_fields.remove('_bypass_rule')
                    
                if entry_fields != occurred_fields:
                    inconsistent_entries.append(entry)

            if inconsistent_entries:
                violation = core.InconsistentField(
                    message=(
                        self.consistency_violation_head
                        + " The following fields are required: " + ", ".join(occurred_fields) + ". "
                        + "But these entries lack them: " + ", ".join([e.key for e in inconsistent_entries]) + ". "
                    ),
                    required_fields=occurred_fields,
                    inconsistent_entries=inconsistent_entries,
                    created_by=self.subclass,
                )
                if self.consistency_requirement == "warn":
                    result.warnings.append(violation)
                elif self.consistency_requirement == "error":
                    result.errors.append(violation)
