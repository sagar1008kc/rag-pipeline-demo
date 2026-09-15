# Information Classification Standard

Northline Trust Company labels every record before it is stored, shared, or
retrieved by an assistant. Classification is need-to-know, not job title alone.

## Labels

| Label | Meaning | Who may retrieve it |
| ----- | ------- | ------------------- |
| Public | Marketing, published rates | Anyone |
| Internal | How we work, not client-identifying | Employees |
| Confidential | Client, account, or control data | Advisor, compliance, security, executive |
| Restricted | Privileged access, crypto material | Security, executive |
| MNPI | Material nonpublic information | Compliance, executive only |

A lower-cleared role must not receive a higher-labeled chunk, even if semantic
search ranks it first. Retrieval enforces this; the model is not trusted to
keep secrets.

## Handling rules

- Do not paste Confidential or above into unsanctioned chat tools.
- Assistants that answer staff questions must log role, doc_id, and chunk_id
  for every retrieval.
- When a document is superseded, keep it for reconstruction but mark
  status=superseded so live answers prefer the current version.
