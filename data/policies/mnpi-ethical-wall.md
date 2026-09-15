# MNPI Ethical Wall

MNPI is material nonpublic information: a fact a reasonable investor would
consider important that is not yet public.

## Wall

- Public side: retail advisors, most portfolio implementation.
- Private side: M&A coverage, issuer-confidential mandates, listed in the
  Watch Book (system of record, not this file).

Advisors must not retrieve this document. Compliance and Executive may.

## Fictional watch example

Watch Book entry WB-8841 covers a potential acquisition of Harbor Yarn
Holdings (fictional). Staff on the public side who ask "are we buying Harbor
Yarn?" must receive no confirmation from this assistant. The correct answer
is abstention plus a pointer to Compliance.

## Chinese wall operational rule

If retrieval would mix Public-side and Private-side chunks in one prompt,
drop the Private-side chunks. Never let the generator see both.
