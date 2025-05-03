from io import StringIO
import bibtexparser as btp
import bibtexparser.model as bib_model


class CheckResult:
    def __init__(self):
        self.errors : list[Violation] = []
        self.warnings : list[Violation]= []

    
    def __str__(self) -> str:
        buf = StringIO()
        buf.write("=== Errors ===\n")
        for error in self.errors:
            buf.write(f"- {error.message} ({error.get_creator_shortest_id()})\n")
            
        buf.write("\n=== Warnings ===\n")
        for warning in self.warnings:
            buf.write(f"- {warning.message} ({warning.get_creator_shortest_id()})\n")
        return buf.getvalue()


class Rule:
    # This is a placeholder for the Rule class. RULE_ID is the unique identifier
    # for the rule. It can be a string or a set of strings, as it would be
    # convenient to have a human readable ID and a machine readable ID.
    RULE_ID: str | set[str] = {"RULE_BASE_CLASS", "RULE000"}


    def check(self, library: btp.Library, result: CheckResult) -> None:
        raise NotImplementedError("Subclasses must implement this method.")
    

    def entry_request_bypass(self, entry: bib_model.Entry) -> bool:
        """Check if the rule should be bypassed for this entry."""
        bypass_str = entry.get('_bypass_rule', None)
        bypass_str = bypass_str.value if bypass_str else ""
        bypass_list = bypass_str.split(",")
        bypass_list = [b.strip() for b in bypass_list if b.strip()]
        for id in self.RULE_ID:
            if id in bypass_list:
                return True
        return False


class RuleSet:
    def __init__(self, rules: list[Rule]):
        self.rules = rules


    def check(self, lib: btp.Library) -> CheckResult:
        result = CheckResult()
        for rule in self.rules:
                rule.check(lib, result)
        return result



class Violation:
    """Base class for all BibTeX errors."""
    def __init__(self, message: str, created_by: type[Rule]):
        self.message = message
        self.created_by = created_by
        # self.suggestions = []


    def get_creator_shortest_id(self) -> str:
        """Get the shortest ID of the rule that created this violation."""
        if isinstance(self.created_by.RULE_ID, set):
            return min(self.created_by.RULE_ID, key=len)
        return self.created_by.RULE_ID

class FieldNotFound(Violation):
    def __init__(
            self, 
            field_name: str, 
            related_entry: bib_model.Entry,
            created_by: type[Rule],
        ):
        self.field_name = field_name
        self.related_entry = related_entry
        super().__init__(f"Field '{field_name}' not found in entry '{related_entry.key}'", created_by)


class InvalidFieldType(Violation):
    def __init__(
            self, 
            related_field: bib_model.Field,
            related_entry: bib_model.Entry,
            created_by: type[Rule],
            reason: str = "",
        ):
        self.related_field = related_field
        self.related_entry = related_entry
        self.reason = reason
        super().__init__(
            f"Invalid field '{related_field.key}' in '{related_entry.key}'. {reason}", 
            created_by
        )


class InvalidFieldValue(Violation):
    def __init__(
            self,
            related_field: bib_model.Field,
            related_entry: bib_model.Entry,
            reason: str,
            created_by: type[Rule],
        ):
        self.related_field = related_field
        self.related_entry = related_entry
        self.reason = reason
        super().__init__(
            f"Invalid value for field '{related_field.key}' in entry '{related_entry.key}': {reason}", 
            created_by
        )


class InconsistentField(Violation):
    def __init__(
            self,
            message: str,
            inconsistent_entries: list[bib_model.Entry],
            required_fields: set[str],
            created_by: type[Rule],
        ):
        self.inconsistent_entries = inconsistent_entries
        self.required_fields = required_fields
        super().__init__(
            message=message,
            created_by=created_by,
        )