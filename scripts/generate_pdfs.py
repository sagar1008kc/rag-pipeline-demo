"""Write the two runbook PDFs so the corpus is mixed, not markdown-only."""

from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "runbooks"


def pdf(path: Path, title: str, body: str) -> None:
    doc = FPDF()
    doc.set_auto_page_break(auto=True, margin=18)
    doc.add_page()
    doc.set_font("Helvetica", "B", 16)
    doc.multi_cell(0, 8, title)
    doc.ln(4)
    doc.set_font("Helvetica", size=11)
    for block in body.strip().split("\n\n"):
        doc.multi_cell(0, 6, block.replace("\n", " "))
        doc.ln(3)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.output(str(path))
    print("wrote", path.relative_to(ROOT))


def main() -> None:
    pdf(
        OUT / "incident-response.pdf",
        "Security Incident Severity for Information Events",
        """
Use this matrix for data handling events (not market outages). Full row-level
detail also lives in tables/severity-matrix.csv.

## Levels

SEV-0: Confirmed export of MNPI or a production HSM secret. Page CISO and Bank
Duty Officer immediately. Legal directs external notice. No ad-hoc emails.

SEV-1: Confirmed Confidential PII (full TIN or full account) in an unsanctioned
tool, or ethical-wall breach. CISO on-call within 15 minutes. Privacy office
within 1 hour.

SEV-2: Suspected mis-classification or the assistant returned a Restricted chunk
to an uncleared role. Security lead same business day. Internal only.

SEV-3: Policy question or training gap, no evidence of leakage. Ticket only.

## Handling

War-room number (fictional): +1-212-555-0199.

Do not paste suspected leaked payloads into the assistant to check if it knows
them. Open a ticket with hashes, not raw secrets.
""",
    )
    pdf(
        OUT / "privileged-access.pdf",
        "Privileged Access and Break-Glass",
        """
Production admin paths (core banking, HSM consoles, identity provider) require
dual control.

## Named cubbies

1. CISO
2. Head of Technology
3. Independent control officer (fictional firm: Pine Audit LLP)

Quorum to activate break-glass: 2 of 3. Sessions are recorded. Maximum duration
45 minutes unless the Duty Officer extends.

## Classification

This document is Restricted. Advisors, employees, and compliance generalists
must not retrieve cubby names or quorum math from the assistant.

Emergency alias (fictional, not a password): NTC-BG-2026-Q2 is a ticket queue
name, not a credential. Real secrets never appear in knowledge files.
""",
    )


if __name__ == "__main__":
    main()
