"""
This script defines rules for proceedings.
"""
from typing import Literal
import bibtexparser as btp
from . import core
import pydantic
import re as regex
from .generic_rules import GenericFieldExistenceCheck


class ProceedingsFieldExistenceCheck(core.Rule):
    """
    Every proceedings entry must have these fields:

    - title
    - author
    - booktitle
    - year

    Proceedings entry may have these fields. 

    - volume
    - pages


    Optionally, the consistency can be required so that if one entry has a type
    of field, all entries must have the same type of field.
    """
    RULE_ID = {"ProceedingsFieldExistenceCheck", "PROC001"}
    MUST_HAVE_FIELDS = {
        "title",
        "author",
        "booktitle",
        "year",
    }
    MAY_HAVE_FIELDS = {
        "volume",
        "pages",
    }


    def __init__(
        self,
        consistency_requirement: Literal["ignore", "warn", "error"] = "warn",
    ):
        self.consistency_requirement = consistency_requirement
        self._checker = GenericFieldExistenceCheck(
            consistency_requirement=consistency_requirement,
            consistency_violation_message_head="Proceedings entries have inconsistent fields.",
            must_have_fields=self.MUST_HAVE_FIELDS,
            may_have_fields=self.MAY_HAVE_FIELDS,
            entry_filter=lambda e: e.entry_type == "inproceedings",
            subclass=ProceedingsFieldExistenceCheck,
        )


    def check(self, lib: btp.Library, result: core.CheckResult) -> None:
        self._checker.check(lib, result)


class ConfNamePublPair(pydantic.BaseModel):
    name: str # Conference name
    publ: str # Publisher abbreviation


_CPP = ConfNamePublPair
CONF_NAME_PUBL_PAIRS = [
    # CCF/Computer Network/A
    _CPP(name="SIGCOMM", publ="ACM"),
    _CPP(name="MobiCom", publ="ACM"),
    _CPP(name="INFOCOM", publ="IEEE"),
    _CPP(name="NSDI", publ="USENIX"),
    # CCF/Computer Network/B
    _CPP(name="SenSys", publ="ACM"),
    _CPP(name="CoNEXT", publ="ACM"),
    _CPP(name="SECON", publ="IEEE"),
    _CPP(name="IPSN", publ="IEEE/ACM"),
    _CPP(name="MobiSys", publ="ACM"),
    _CPP(name="ICNP", publ="IEEE"),
    _CPP(name="MobiHoc", publ="ACM/IEEE"),
    _CPP(name="NOSSDAV", publ="IEEE"),
    _CPP(name="IWQoS", publ="IEEE"),
    _CPP(name="IMC", publ="ACM/USENIX"),
    # CCF/Computer Network/C
    _CPP(name="ANCS", publ="ACM/IEEE"),
    _CPP(name="APNOMS", publ="IFIP/IEEE"),
    _CPP(name="FORTE", publ="Springer"),
    _CPP(name="LCN", publ="IEEE"),
    _CPP(name="GLOBECOM", publ="IEEE"),
    _CPP(name="ICC", publ="IEEE"),
    _CPP(name="ICCCN", publ="IEEE"),
    _CPP(name="MASS", publ="IEEE"),
    _CPP(name="P2P", publ="IEEE"),
    _CPP(name="IPCCC", publ="IEEE"),
    _CPP(name="WoWMoM", publ="IEEE"),
    _CPP(name="ISCC", publ="IEEE"),
    _CPP(name="WCNC", publ="IEEE"),
    # CCF/Arch&Distri&Storage/A
    _CPP(name="PPoPP", publ="ACM"),
    _CPP(name="FAST", publ="USENIX"),
    _CPP(name="DAC", publ="ACM"),
    _CPP(name="HPCA", publ="IEEE"),
    _CPP(name="MICRO", publ="IEEE/ACM"),
    _CPP(name="SC", publ="IEEE"),
    _CPP(name="ASPLOS", publ="ACM"),
    _CPP(name="ISCA", publ="ACM/IEEE"),
    _CPP(name="ATC", publ="USENIX"),
    _CPP(name="EuroSys", publ="ACM"),
    # CCF/Arch&Distri&Storage/B
    _CPP(name="SoCC", publ="ACM"),
    _CPP(name="SPAA", publ="ACM"),
    _CPP(name="PODC", publ="ACM"),
    _CPP(name="FPGA", publ="ACM"),
    _CPP(name="CGO", publ="IEEE/ACM"),
    _CPP(name="DATE", publ="IEEE/ACM"),
    _CPP(name="HOT CHIPS", publ="IEEE"),
    _CPP(name="CLUSTER", publ="IEEE"),
    _CPP(name="ICCD", publ="IEEE"),
    _CPP(name="ICCAD", publ="IEEE/ACM"),
    _CPP(name="ICDCS", publ="IEEE"),
    _CPP(name="CODES+ISSS", publ="ACM/IEEE"),
    _CPP(name="HiPEAC", publ="ACM"),
    _CPP(name="SIGMETRICS", publ="ACM"),
    _CPP(name="PACT", publ="IEEE/ACM"),
    _CPP(name="ICPP", publ="ACM"),
    _CPP(name="ICS", publ="ACM"),
    _CPP(name="VEE", publ="ACM"),
    _CPP(name="IPDPS", publ="IEEE"),
    _CPP(name="Performance", publ="ACM"),
    _CPP(name="HPDC", publ="IEEE"),
    _CPP(name="ITC", publ="IEEE"),
    _CPP(name="LISA", publ="USENIX"),
    _CPP(name="MSST", publ="IEEE"),
    _CPP(name="RTAS", publ="IEEE"),
    _CPP(name="Euro-Par", publ="Springer"),
    # CCF/Network&Security/A
    _CPP(name="CCS", publ="ACM"),
    _CPP(name="EUROCRYPT", publ="Springer"),
    _CPP(name="S&P", publ="IEEE"),
    _CPP(name="CRYPTO", publ="Springer"),
    _CPP(name="Security", publ="USENIX"),
    _CPP(name="NDSS", publ="ISOC"),
    # CCF/Network&Security/B
    _CPP(name="ACSAC", publ="IEEE"),
    _CPP(name="ASIACRYPT", publ="Springer"),
    _CPP(name="ESORICS", publ="Springer"),
    _CPP(name="FSE", publ="Springer"),
    _CPP(name="CSFW", publ="IEEE"),
    _CPP(name="SRDS", publ="IEEE"),
    _CPP(name="CHES", publ="Springer"),
    _CPP(name="DSN", publ="IEEE/IFIP"),
    _CPP(name="RAID", publ="Springer"),
    _CPP(name="PKC", publ="Springer"),
    _CPP(name="TCC", publ="Springer"),
    # CCF/SoftwareEngineering&Sys&Language/A
    _CPP(name="PLDI", publ="ACM"),
    _CPP(name="POPL", publ="ACM"),
    _CPP(name="FSE", publ="ACM"),
    _CPP(name="SOSP", publ="ACM"),
    _CPP(name="OOPSLA", publ="ACM"),
    _CPP(name="ASE", publ="IEEE/ACM"),
    _CPP(name="ICSE", publ="ACM/IEEE"),
    _CPP(name="ISSTA", publ="ACM"),
    _CPP(name="OSDI", publ="USENIX"),
    _CPP(name="FM", publ="FME"),
    # CCF/Database&Mining&Indexing/A
    _CPP(name="SIGMOD", publ="ACM"),
    _CPP(name="SIGKDD", publ="ACM"),
    _CPP(name="ICDE", publ="IEEE"),
    _CPP(name="SIGIR", publ="ACM"),
    _CPP(name="VLDB", publ="Morgan Kaufmann/ACM"),
    # CCF/ComputerScienceTheory/A
    _CPP(name="STOC", publ="ACM"),
    _CPP(name="SODA", publ="SIAM"),
    _CPP(name="CAV", publ="Springer"),
    _CPP(name="FOCS", publ="IEEE"),
    _CPP(name="LICS", publ="IEEE"),
    # CCF/CG&Multimdeia/A
    _CPP(name="MM", publ="ACM"),
    _CPP(name="SIGGRAPH", publ="ACM"),
    _CPP(name="VR", publ="IEEE"),
    _CPP(name="VIS", publ="IEEE"),
    # CCF/AI/A
    _CPP(name="AAAI", publ=""), # the publisher of AAAI is AAAI, so make it empty to avoid duplication
    _CPP(name="NeurIPS", publ="MIT Press"),
    _CPP(name="ACL", publ=""),  # the publisher of ACL is ACL, so make it empty to avoid duplication
    _CPP(name="CVPR", publ="IEEE"),
    _CPP(name="ICCV", publ="IEEE"),
    _CPP(name="ICML", publ="ACM"),
    _CPP(name="IJCAI", publ="Morgan Kaufmann"),
    # CCF/HumanComputerInteraction&UbiquitousComputing/A
    _CPP(name="CSCW", publ="ACM"),
    _CPP(name="CHI", publ="ACM"),
    # _CPP(name="UbiComp", publ="ACM"), # It is now a journal called "IMWUT"
    _CPP(name="UIST", publ="ACM"),
    # CCF/CrossingField/A
    _CPP(name="WWW", publ="ACM"),
    _CPP(name="RTSS", publ="IEEE"),
    _CPP(name="WINE", publ="Springer"),
]

class ProceedingsBooktitleCheck(core.Rule):
    """
    The purpose of this rule is to normalize the booktitles of proceedings
    entries by imposing a specific format. Such format is designed by the
    authors' experience.

    The `booktitle` field of a proceedings entry must follow the format: 
        `<head> <publ> <conference>`,
    where:
        - `<head>` is one of the following, and should be used CONSISTENTLY:
            - "In proceedings of the"
            - "Proceedings of the"
            - "Proc. of the"
        - `<publ>` is the publisher name or its abbreviation. Common
          abbreviations are:
            - "IEEE"
            - "ACM"
            - "Springer"
        - `<conference>` is the abbreviation of the conference name. For
          example: `MobiCom`, `SenSys`, etc.

    For example, the following booktitle is valid:
        - Proceedings of the ACM CCS
        - In proceedings of the ACM CCS
        - Proc. of the ACM CCS

    The following booktitle is invalid:
        - "Proceedings of the 27th Annual International Conference on Mobile
          Computing and Networking". Too long, should be shortened to
          "Proceedings of the ACM MobiCom"
    """

    RULE_ID = {"ProceedingsBooktitleCheck", "PROC002"}

    def __init__(
            self, 
            head: Literal["In proceedings of the", "Proceedings of the", "Proc. of the"] = "Proceedings of the",
            conf_pairs: list[ConfNamePublPair] = None,
            ):
        self.head = head

        if conf_pairs is None:
            conf_pairs = CONF_NAME_PUBL_PAIRS
        self.conf_pairs = conf_pairs
        self._validate_conf_pairs()

        # "ending" = "<publ> <conference>"
        self._valid_endings = [p.publ + " " + p.name for p in conf_pairs]
        self._endings_pattern = regex.compile(
            r"^(" + "|".join(self._valid_endings) + r")$"
        )


    def check(self, lib: btp.Library, result: core.CheckResult) -> None:
        proceeding_entries = [e for e in lib.entries if e.entry_type == "inproceedings"]

        for entry in proceeding_entries:
            if self.entry_request_bypass(entry):
                continue

            if "booktitle" not in entry:
                result.errors.append(
                    core.FieldNotFound(
                        field_name="booktitle",
                        related_entry=entry,
                        created_by=self.__class__,
                    )
                )
                continue

            booktitle = entry["booktitle"]
            field = entry.fields_dict["booktitle"]
            if not booktitle.startswith(self.head):
                result.errors.append(
                    core.InvalidFieldValue(
                        related_field=field,
                        related_entry=entry,
                        created_by=self.__class__,
                        reason=(
                            f"Booktitle of a proceedings entry should start with \"{self.head}\". Got \"{booktitle}\". "
                        )
                    )
                )
                continue

            ending = booktitle[len(self.head):].strip()
            if not self._endings_pattern.match(ending):
                result.errors.append(
                    core.InvalidFieldValue(
                        related_field=field,
                        related_entry=entry,
                        created_by=self.__class__,
                        reason=(
                            f"\"{booktitle}\" contains \"{ending}\", which is an invalid <publ> <conf> pair."
                        )
                    )
                )
                continue



    def _validate_conf_pairs(self):
        conf_pairs = self.conf_pairs

        abbr2pair = {}
        for pair in conf_pairs:
            if pair.name in abbr2pair:
                abbr2pair[pair.name].append(pair)
            else:
                abbr2pair[pair.name] = [pair]

        dup_abbr = []
        for abbr, pairs in abbr2pair.items():
            if len(pairs) > 1:
                dup_abbr.append((abbr, pairs))
    
        if dup_abbr:
            error_msg = (
                "Duplicate conference abbreviation found in conf_pairs: "
                + ", ".join([e[0] for e in dup_abbr])
                + ". Please ensure that each conference abbreviation is unique."
            )
            raise ValueError(error_msg)

