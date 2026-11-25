"""Testes do radar/cli.py."""

from radar.cli import main


def test_cli_docs(capsys):
    assert main(["docs"]) == 0
    out = capsys.readouterr().out
    assert "edital" in out
    assert "minuta-contrato" in out
    assert "analise-recurso-contraposicoes" in out


def test_cli_tc_analise(capsys):
    assert main(["tc-analise", "--orgao", "Município de Antônio João/MS"]) == 0
    out = capsys.readouterr().out
    assert "Tribunal de Contas Municipal" in out
