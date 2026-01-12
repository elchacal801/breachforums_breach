# Ethics & Handling Policy

## Core Principle: Do No Harm

This project analyzes a dataset obtained from a malicious context (a breach forum). While the data is public/leaked, the individuals listed in it (whether threat actors or innocent users) have privacy rights. We adhere to strict data minimization.

## Redaction Rules

1. **No Identifiers**: We never publish usernames, email addresses, IP addresses, or password hashes.
2. **Aggregates Only**: Outputs are limited to counts, timestamps (bucketed), and boolean flags.
3. **Synthetic Data**: If a visualization requires example rows, strictly synthetic data (mock users) will be used.

## Artifact Handling

- **PGP Keys**: The dataset contained a private PGP key `breachedforum-pgp-key.txt.asc`. This file is **NEVER** to be imported, used, or retained. It is excluded from all analysis.
- **Malware**: The source archives are treated as potentially containing malware. Do not execute binaries or scripts found within the dump.
- **Cleanup**: Ephemeral Docker containers are destroyed after analysis.

## Defense vs Offense

This work is strictly defensive. It aims to understand:

- Forum growth dynamics (Incident Response intelligence).
- Password security hygiene (OpSec research).
- Platform configuration (MyBB defaults vs custom).

It does **NOT** support:

- Deanonymization of users.
- Credential stuffing or password cracking.
- Attribution (law enforcement/intel function, not this project's scope).
