"""Interface de linha de comando do Radar de Licitações."""

from __future__ import annotations

import argparse
import json

from radar import documentos
from radar.entidade import classificar_entidade
from radar.tc_analise import analise_critica


def cmd_docs() -> str:
    """Lista os documentos geráveis pelo radar."""
    return "\n".join(documentos.DOCUMENTOS)


def cmd_gerar(documento: str, dados_path: str) -> str:
    """Gera o documento pedido a partir do JSON de dados do processo."""
    with open(dados_path, encoding="utf-8") as f:
        dados = json.load(f)
    nome = documento.replace("-", "_")
    gen = getattr(documentos, f"gerar_{nome}", None)
    if gen is None:
        raise SystemExit(f"Documento desconhecido: {documento}")
    if documento == "analise-recurso-contraposicoes":
        entidade = classificar_entidade(dados.get("orgao"))
        return gen(dados, analise_critica(entidade, dados))
    return gen(dados)


def cmd_tc_analise(
    orgao: str | None, entidade: str | None, dados_path: str | None
) -> str:
    """Análise crítica do Tribunal de Contas aplicável ao órgão."""
    dados: dict = {}
    if dados_path:
        with open(dados_path, encoding="utf-8") as f:
            dados = json.load(f)
    orgao_ref = orgao or dados.get("orgao", "[PREENCHER]")
    t = classificar_entidade(orgao_ref, entidade)
    a = analise_critica(t, dados)
    linhas = [
        "# Análise Crítica do TC aplicável",
        "",
        f"**Órgão:** {orgao_ref}",
        f"**Tribunal de Contas:** {a.tribunal_de_contas}",
        "",
        "## Pontos que seriam apontados:",
        "",
    ]
    linhas += [f"- {p.id}: {p.descricao} ({p.fundamento})" for p in a.pontos]
    if a.observacoes:
        linhas += ["", "## Observações", ""]
        linhas += [f"- {obs}" for obs in a.observacoes]
    return "\n".join(linhas) + "\n"


def main(argv: list | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="radar",
        description="Radar de Licitações: elabora documentos do processo e aponta o TC aplicável.",
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    sub.add_parser("docs", help="Lista os documentos geráveis")

    p_gerar = sub.add_parser("gerar", help="Gera um documento")
    p_gerar.add_argument("documento", choices=documentos.DOCUMENTOS)
    p_gerar.add_argument("--dados", required=True, help="JSON com os dados do processo")

    p_tc = sub.add_parser(
        "tc-analise", help="Análise crítica do Tribunal de Contas aplicável"
    )
    p_tc.add_argument("--orgao")
    p_tc.add_argument("--entidade")
    p_tc.add_argument("--dados")

    args = parser.parse_args(argv)

    if args.comando == "docs":
        print(cmd_docs())
    elif args.comando == "gerar":
        print(cmd_gerar(args.documento, args.dados))
    elif args.comando == "tc-analise":
        print(cmd_tc_analise(args.orgao, args.entidade, args.dados))
    return 0


if __name__ == "__main__":
    main()
