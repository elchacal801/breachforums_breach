# BreachForums Data Analysis (MyBB Users)

**Research Metrics & Security Posture Analysis Only**

This repository contains code and methodology for analyzing a historical data dump from the "BreachForums" community (MyBB `users` table). The goal is to derive aggregate security insights, community growth patterns, and authentication posture statistics without exposing, processing, or retaining personally identifiable information (PII).

**⚠️ SAFETY & ETHICS NOTICE**

- **NO DATA** is hosted in this repository.
- **NO PII** is extracted or published.
- All analysis is performed on aggregate statistics (counts, distributions).
- This project is for defensive security research and incident response training purposes.

## Project Structure

- `docs/`: Methodology, ethics policy, and environment setup.
- `scripts/`: Powershell and SQL scripts for isolated Docker-based import.
- `queries/`: SQL queries designed to return ONLY safe aggregates.
- `outputs/`: (Ignored by git) Destination for generated charts/tables.

## Handling Procedures

The underlying dataset is treated as hostile/radioactive.

1. **Isolation**: Data is processed only within ephemeral Docker containers.
2. **Minimization**: No `SELECT *`; no queries on PII columns (`email`, `username`, `password`).
3. **Integrity**: Input artifacts are verified via SHA-256 chain-of-custody.

## License

MIT License - This applies to the *code* and *methodology* only.
