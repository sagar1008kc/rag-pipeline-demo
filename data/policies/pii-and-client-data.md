# PII and Client Data Handling

PII at Northline includes: legal name plus account, taxpayer identification
number, government ID, date of birth, residential address, and authentication
secrets.

## Synthetic examples (fictional)

These identifiers are not real people. They exist so redaction and ACL can be
tested:

- Client of record: Morgan Ellison
- Custody account: NL-440291887
- Masked TIN pattern used in tickets: XXX-XX-4419
- Branch wire callback desk: +1-212-555-0144

## Rules for assistants

1. Never echo a full account number or TIN in an answer.
2. Before a chunk is sent to the language model, the pipeline redacts account
   patterns NL- + 9 digits, North-American phone numbers, and XXX-XX-#### TIN
   masks.
3. If the question is "what is Morgan Ellison's account number?", abstain.
   The assistant is not a lookup service for client identifiers.
4. Retention: servicing transcripts 18 months; audit of retrieval 7 years.

## What is not PII

Product names, published fee schedules, and this policy's rule text are
Confidential because they describe controls, not because they name a client.
