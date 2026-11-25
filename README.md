# licitacao-14133 — Open-source Brazilian public procurement document generator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)

> **EN** — Open-source CLI that generates the full document set of a Brazilian public procurement process (DFD, ETP, TR, Edital, contract minutes, registration minutes, opinion, impugnation reply, resource/counter-appeal analysis) under **Law 14.133/2021**, and runs a critical analysis of the applicable Court of Accounts (TCE) jurisprudence for the contracting body. Maintained by [LEANDRO2025-OFICIAL](https://github.com/LEANDRO2025-OFICIAL).

> **PT-BR** — CLI open-source que gera o conjunto completo de documentos do processo licitatório brasileiro (DFD, ETP, TR, Edital, minuta de contrato, minuta de ata, sugestão de parecer, resposta de impugnação, análise de recurso e contraposições) conforme a **Lei 14.133/2021**, e executa análise crítica da jurisprudência do Tribunal de Contas aplicável ao órgão contratante. Mantido por [LEANDRO2025-OFICIAL](https://github.com/LEANDRO2025-OFICIAL).

## Why this matters / Por que importa

Brazilian public procurement (licitações) is governed by Law 14.133/2021 and supervised by three tiers of Courts of Accounts (TCM, TCE, TCU). Every contracting body — from small municipalities to federal agencies — must produce a large, highly standardized set of documents (DFD, ETP, TR, Edital, contract minutes, …) and survive external audit. Most of this work is still done by hand, inconsistently, which is a major source of irregularities flagged by the Courts of Accounts.

This tool automates the generation of those documents from a small JSON input and produces a critical review aligned with the jurisprudence of the **applicable** Court of Accounts for the contracting body, reducing errors, audit findings and rework for public managers, procurement agents and bidding companies.

## Features / Funcionalidades

- Generates 9 document types: DFD, ETP, TR, Edital, Minuta de Contrato, Minuta de Ata de Registro, Sugestão de Parecer, Resposta de Impugnação, Análise e Decisão de Recurso e Contraposições.
- Detects the applicable Court of Accounts (TCM / TCE / TCU) for the contracting body.
- Produces a critical TC-style analysis pointing out typical irregularities.
- Pure Python 3.10+, no external runtime dependencies.
- Fully tested (pytest).

## Quick start / Início rápido

```sh
git clone https://github.com/LEANDRO2025-OFICIAL/licitacao-14133.git
cd licitacao-14133
python -m pip install -e .
```

Generate a document:

```sh
licitacao-14133 gerar etp --dados dados.json
# or
radar gerar etp --dados dados.json
```

Example `dados.json`:

```json
{
  "orgao": "Município de Antônio João/MS",
  "objeto": "Suprimentos",
  "modalidade": "Pregão",
  "valor": "R$ 1.000.000,00",
  "prazo": "90 dias",
  "numero_processo": "000/2026"
}
```

Critical Court of Accounts analysis:

```sh
licitacao-14133 tc-analise --orgao "Município de Antônio João/MS"
```

Tests:

```sh
python -m pytest tests -q
```

## Document generation / Geração de documentos

Generators live in `radar/documentos.py`; `radar/tc_analise.py` produces the critical Court of Accounts analysis. The companion Claude skills (`licitacao-14133`, `auditoria-licitacao-14133`, `revisao-estilistica-formal`) extend these generators with full LLM-assisted drafting.

## Contributing / Contribuindo

Pull requests are welcome. Please open an issue first to discuss what you would like to change. This project follows a TDD-first workflow.

## License

MIT — see [LICENSE](./LICENSE).

## Maintainer / Mantenedor

Leandro Santos — [LEANDRO2025-OFICIAL](https://github.com/LEANDRO2025-OFICIAL) — leowizz70@gmail.com

Part of the **LS AGI BRASIL** GovTech initiative (open-sourcing Brazilian public-procurement tooling).