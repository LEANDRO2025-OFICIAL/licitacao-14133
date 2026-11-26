"""Classificação do órgão que aplica:

- Município/Prefeitura → **Tribunal de Contas Municipal**
- Estado/Tribunal de Contas do Estado → **Tribunal de Contas do Estado**
- Federal → **Tribunal de Contas da União**

O classificador também aceita o valor explícito `entidade` quando o `orgao`
não traz pista do nível (padrão: municipal).
"""

from __future__ import annotations

import unicodedata
from enum import Enum


def _norm(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if ord(c) < 128).lower()


class TipoEntidade(Enum):
    MUNICIPAL = "municipal"
    ESTADUAL = "estadual"
    FEDERAL = "federal"

    def __str__(self) -> str:
        return self.value


_VALORES = {
    "municipal": TipoEntidade.MUNICIPAL,
    "municipio": TipoEntidade.MUNICIPAL,
    "prefeitura": TipoEntidade.MUNICIPAL,
    "estadual": TipoEntidade.ESTADUAL,
    "estado": TipoEntidade.ESTADUAL,
    "tribunal de contas do estado": TipoEntidade.ESTADUAL,
    "federal": TipoEntidade.FEDERAL,
    "uniao": TipoEntidade.FEDERAL,
    "tcu": TipoEntidade.FEDERAL,
    "tribunal de contas da uniao": TipoEntidade.FEDERAL,
}


def classificar_entidade(
    orgao: str | None = None, entidade: str | None = None
) -> TipoEntidade:
    """Classifica o nível do órgão: municipal, estadual ou federal."""
    if entidade:
        chave = _norm(entidade)
        if chave in _VALORES:
            return _VALORES[chave]
        raise ValueError(f"Entidade não reconhecida: {entidade!r}")
    org = _norm(orgao or "")
    if any(k in org for k in ("federal", "nacional", "republica", "governo federal")):
        return TipoEntidade.FEDERAL
    if any(k in org for k in ("municipio", "municipal", "prefeitura")):
        return TipoEntidade.MUNICIPAL
    if any(k in org for k in ("estado", "governo do estado")):
        return TipoEntidade.ESTADUAL
    return TipoEntidade.MUNICIPAL


def nivel_tribunal_de_contas(entidade: TipoEntidade) -> str:
    """Nome do tribunal de contas aplicável ao nível do órgão."""
    return {
        TipoEntidade.MUNICIPAL: "Tribunal de Contas Municipal",
        TipoEntidade.ESTADUAL: "Tribunal de Contas do Estado",
        TipoEntidade.FEDERAL: "Tribunal de Contas da União",
    }[entidade]
