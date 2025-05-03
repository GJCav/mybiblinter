import bibtexparser
from .rules4article import ArticleFieldExistenceCheck
from .rules4proc import ProceedingsBooktitleCheck, ProceedingsFieldExistenceCheck
from .rules4other import MiscFieldExistenceCheck, BookFieldExistenceCheck
from .core import RuleSet
import argparse

def main():
    parser = argparse.ArgumentParser(description="Check .bib files for common issues.")
    parser.add_argument("bibfile", help="Path to the .bib file to check")

    args = parser.parse_args()
    bibfile = args.bibfile

    with open(bibfile, "r") as f:
        bib_str = f.read()
    library = bibtexparser.parse_string(bib_str)
    
    rule_set = RuleSet(rules=[
        ProceedingsFieldExistenceCheck(),
        ProceedingsBooktitleCheck(),
        ArticleFieldExistenceCheck(),
        MiscFieldExistenceCheck(),
        BookFieldExistenceCheck(),
    ])

    result = rule_set.check(library)
    print(str(result))


if __name__ == "__main__":
    main()
