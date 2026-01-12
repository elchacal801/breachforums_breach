# Methodology & Chain of Custody

## Dataset Origin

- **Source**: Resecurity Blog / Distributed Archive
- **Content**: MyBB `users` table dump (MySQL).
- **Size**: ~323,986 records.
- **Initial Handling**: Processed in isolated Kali VM. Verified via SHA-256.

## Integrity Verification

We maintain a strict chain of custody.

1. **Kali Export**: AES-256 encrypted .7z archive.
2. **Transfer**: Shared folder to Windows Host.
3. **Verification**:
   - `databoose.sql` SHA-256: `790f3595850e4d8c212a35a40eb69fe0431fda6abcfbbf4592126bf636df2088`
   - Archive SHA-256: `186ab1f5d398586ff21c68a48d87d4e4ecafce0fbb30ce21ccf781b1abb86b75`

## Analysis Workflow

1. **Import**: `databoose.sql` is imported into a **disposable** MySQL 8 Docker container.
2. **Sanitization**: MySQL runs in isolation; no volumes mapped to critical host paths.
3. **Querying**: SQL scripts execute read-only `SELECT` queries to generate aggregate CSVs.
4. **Validation**: Row counts verified against known total (323,986).
