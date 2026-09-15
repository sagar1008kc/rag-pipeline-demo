Synthetic knowledge for Northline Trust Company (fictional private bank).

| Folder | Formats | What it is |
| ------ | ------- | ---------- |
| `policies/` | `.md` | Classification, PII, AI use, MNPI wall, withdrawn policy |
| `runbooks/` | `.pdf` | Incident severity, break-glass |
| `tables/` | `.csv` | Severity matrix, retention, watch book |
| `apps/` | `.tsx` | Internal UI source that mentions controls and synthetic PII |
| `wiki/` | `.html` | Desk FAQ plus a prompt-injection fixture |
| `structured/` | `.json` `.yaml` | Org directory and control catalog |

`manifest.yaml` is the source of classification, status, and doc_id for every file.

All people, accounts, phones, and watch-book issuers are invented.

## Why the Corpus Is Mixed

Real internal knowledge is rarely one clean wiki. The notebooks show how each
format creates a different RAG problem:

- Markdown policies have headings and status metadata.
- PDFs require extraction before chunking.
- CSV matrices should preserve row and column context.
- TSX source can contain policy hints and synthetic client fixtures.
- HTML wiki pages can contain prompt-injection text.
- JSON and YAML are structured records that still need searchable text.

The RAG pipeline normalizes them into one document shape, then keeps the
original source type and classification on every chunk.
