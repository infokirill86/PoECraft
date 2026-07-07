from p2c_engine.domain.evidence import LegalityReport

def legal_report(*evidence: object) -> LegalityReport:
    return LegalityReport(True, (), tuple(evidence))
