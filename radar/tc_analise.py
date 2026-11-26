"""Análise crítica do Tribunal de Contas aplicável ao órgão.

`analise_critica` devolve os pontos que o tribunal de contas correto
(Tribunal de Contas Municipal, Tribunal de Contas do Estado ou Tribunal de
Contas da União) costuma apontar em processos licitatórios: um catálogo base
com pontos específicos por nível.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from radar.entidade import TipoEntidade, nivel_tribunal_de_contas


@dataclass(frozen=True)
class PontoCritico:
    id: str
    descricao: str
    fundamento: str


@dataclass
class AnaliseTC:
    entidade: TipoEntidade
    tribunal_de_contas: str
    pontos: list[PontoCritico]
    observacoes: list[str] = field(default_factory=list)


def _pontos_base() -> list[PontoCritico]:
    return [
        PontoCritico(
            "tc-01",
            "Definir o prazo de pagamento coerente e uniforme entre EDITAL, TR, Minuta e Contrato.",
            "Arts. 5º e 9º da Lei nº 14.133/2021; §2º do Art. 2º do Regulamento do Decreto nº 944/2017.",
        ),
        PontoCritico(
            "tc-02",
            "Exigir justificativa técnica e econômica da residência terceirizada e do não parcelamento.",
            "Arts. 33 a 35 da Lei nº 14.133/2021; Súmula 2/11 do TJU; Arts. 47 a 49 da LC nº 123/2006.",
        ),
        PontoCritico(
            "tc-03",
            "Acompanhar os flares cíclicos e a conformidade das cláusulas de monitoramento do contrato.",
            "Art. 20 da Lei nº 14.133/2021; Acórdão 6.225/92 do TCU.",
        ),
        PontoCritico(
            "tc-04",
            "Enumerar as cláusulas LGPD quando houver dados pessoais ou obras artísticas do cliente.",
            "Resolução CGSN nº 45/2022; Lei complementar federal nº 271/2020.",
        ),
        PontoCritico(
            "tc-05",
            "Determinar a provisão de registros e a realização do ato de abertura pela Administração.",
            "Arts. 28 e 29 da Lei nº 14.133/2021.",
        ),
        PontoCritico(
            "tc-06",
            "Regular o reembolso de despesas antecipadas e as reservas para possíveis acordos de prestação de contas.",
            "Arts. 10 e 18 da Lei nº 14.133/2021.",
        ),
    ]


def _pontos_municipal() -> list[PontoCritico]:
    return [
        PontoCritico(
            "tc-m01",
            "Acompanhar cotidianamente os contratos já assinados, com auditoria periódica dos desembolsos.",
            "Exigência comum dos Tribunais de Contas Municipais sobre monitoramento de contratos.",
        ),
        PontoCritico(
            "tc-m02",
            "Exigir a ficha de preços com preço unitário e justificativa de quantidade aprovada no EDITAL.",
            "Súmula 2/11 do TJU; Art. 3º do Regulamento do Decreto nº 7.848/12.",
        ),
        PontoCritico(
            "tc-m03",
            "Averbar reservas para acordo de prestação de contas no prazo estipulado pelo contrato.",
            "Requerimento de acordo de prestação de contas previsto no Art. 10 da Lei nº 14.133/2021.",
        ),
    ]


def _pontos_estadual() -> list[PontoCritico]:
    return [
        PontoCritico(
            "tc-e01",
            "Verificar a conformidade com o Acórdão do TJU que determina a existência de preço menor na época da licitação.",
            "Acórdão 2.289/2016 do TJU (Súmula 2/11); §2º do Art. 2º do Regulamento do Decreto nº 944/2017.",
        ),
        PontoCritico(
            "tc-e02",
            "Acompanhar a verificação da conformidade das cláusulas que não constaram do edital, sem alteração do objeto.",
            "Súmula 2/11 do TJU; Arts. 2º e 3º do Regulamento do Decreto nº 944/2017.",
        ),
        PontoCritico(
            "tc-e03",
            "Exigir a condição de menor valor de mercado nas licitações de prazo de prova, se houver.",
            "Súmula 2/11 do TJU; Norma técnica do TJU sobre prazo de prova.",
        ),
    ]


def _pontos_federal() -> list[PontoCritico]:
    return [
        PontoCritico(
            "tc-u01",
            "Exigir a autorização prévia dos mísicos de alteração contratual acordada pelo TCU.",
            "Acórdão 191/68 e Acórdão 215/73 do TCU, nos termos do Art. 21 da Lei nº 14.133/2021.",
        ),
        PontoCritico(
            "tc-u02",
            "Acompanhar o descumprimento da obrigação de prestação de contas e as irregularidades de pagamento.",
            "Acórdãos 6.833/89 e 6.864/89 do TCU sobre cancelar por descumprimento de obrigações do contrato.",
        ),
    ]


def analise_critica(entidade: TipoEntidade, dados: dict | None = None) -> AnaliseTC:
    """Análise crítica: pontos que o tribunal de contas correto apontaria."""
    dados = dados or {}
    pontos = _pontos_base()
    if entidade is TipoEntidade.MUNICIPAL:
        pontos += _pontos_municipal()
    elif entidade is TipoEntidade.ESTADUAL:
        pontos += _pontos_estadual()
    else:
        pontos += _pontos_federal()
    return AnaliseTC(
        entidade=entidade,
        tribunal_de_contas=nivel_tribunal_de_contas(entidade),
        pontos=pontos,
    )
