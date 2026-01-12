# BreachForums Data Analysis (MyBB Users)

**Research Metrics & Security Posture Analysis Only**

[![View Dashboard](https://img.shields.io/badge/View-Live_Dashboard-blue?style=for-the-badge&logo=github)](https://elchacal801.github.io/breachforums_breach/dashboard/)

This repository contains code and methodology for analyzing a historical data dump from the "BreachForums" community (MyBB `users` table). The goal is to derive aggregate security insights, community growth patterns, and authentication posture statistics without exposing, processing, or retaining personally identifiable information (PII).

**⚠️ SAFETY & ETHICS NOTICE**

- **NO DATA** is hosted in this repository.
- **NO PII** is extracted or published.
- **NO PASSWORDS** are cracked or distributed.
- All analysis is performed on aggregate statistics (counts, distributions).
- This project is for defensive security research and incident response training purposes.

## Background

**BreachForums** was a notorious English-language cybercrime forum that emerged in 2022 as a successor to RaidForums. It served as a hub for the trade of stolen databases and hacking tools.

In **January 2026**, a significant data breach targeted the forum itself, resulting in the leak of its internal database (MyBB). The leak, analyzing approximately 320,000 user records, was widely reported as a "Doomsday" event for the cybercriminal community due to the exposure of operational security failures among its members.

For more context on the breach, please refer to the Resecurity article:
> [Doomsday for Cybercriminals — Data Breach of Major Dark Web Forum](https://www.resecurity.com/blog/article/doomsday-for-cybercriminals-data-breach-of-major-dark-web-forum)

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
