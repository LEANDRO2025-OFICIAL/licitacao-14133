"""Geradores dos documentos do processo licitatório que o Radar elabora.

Os geradores seguem os padrões das skills `licitacao-14133` (ETP, TR, ...) e
`auditoria-licitacao-14133` (Minuta de Contrato, Sugestão de Parecer, ...).
Cada um devolve Markdown pronto para revisão com `revisao-estilistica-formal`.

Insumos esperados (dados do processo):

- `orgao`: nome da entidade (Município, Prefeitura, Estado, União, ...)
- `objeto`: objeto da contratação
- `modalidade`: Pregão, Dispensa, Inexistibilidade, etc.
- `valor`: estimativa do valor (string, ex.: "R$ 1.000.000,00")
- `prazo`: prazo de execução ou validade
- `numero_processo` / `data_edital`: identificação do processo
"""

from __future__ import annotations

from typing import Optional

from radar.tc_analise import AnaliseTC

DOCUMENTOS = [
    "dfd",
    "etp",
    "tr",
    "edital",
    "minuta-contrato",
    "minuta-ata",
    "sugestao-parecer",
    "resposta-impugnacao",
    "analise-recurso-contraposicoes",
]


def _txt(dados: dict, chave: str, padrao: str = "[PREENCHER]") -> str:
    valor = (dados or {}).get(chave)
    return str(valor) if valor not in (None, "") else padrao


def _cabecalho(dados: dict) -> str:
    return (
        f"**Órgão:** {_txt(dados, 'orgao')}\n"
        f"**Processo:** {_txt(dados, 'numero_processo')}\n"
        f"**Objeto:** {_txt(dados, 'objeto')}\n"
        f"**Modalidade:** {_txt(dados, 'modalidade')}\n"
    )


def gerar_dfd(dados: dict) -> str:
    """Diagrama de Fluxo de Dados do processo licitatório."""
    dados = dados or {}
    return (
        "# Diagrama de Fluxo de Dados (DFD)\n\n"
        f"{_cabecalho(dados)}\n"
        "## Entidades externas\n\n"
        f"- {_txt(dados, 'orgao')} (Cliente/secretaria demandante)\n"
        "- Município/governo local (Cidade)\n"
        "- Emissor do DFD (se houver)\n\n"
        "## Processo\n\n"
        f"- {_txt(dados, 'objeto')}\n\n"
        "## Fluxos de dados\n\n"
        "1. Pedido de autorização/despacho\n"
        "2. Elaboração do DFD\n"
        "3. Publicação do edital / comunicação\n"
        "4. Recebimento e análise das propostas\n"
        "5. Designação do contratante\n"
        "6. Assinatura do contrato\n"
        "7. Prestação de contas periódica\n\n"
        "Obs.: o DFD em si não é gerado por esta skill; ele é um insumo da\n"
        "secretaria demandante; quando o radar crescer, integre a versão\n"
        "produzida ao processo licitatório.\n"
    )


def gerar_etp(dados: dict) -> str:
    """Estudo Técnico Preliminar (Estrutura em incisos, conforme Art. 18, §2º, da Lei 14.133/2021)."""
    dados = dados or {}
    return (
        "# Estudo Técnico Preliminar (ETP)\n\n"
        f"{_cabecalho(dados)}\n"
        "Base legal: Art. 6º, XX, e Art. 18, caput e §§1º e 2º, da Lei nº 14.133/2021.\n\n"
        "1. Descrição da necessidade da contratação, considerado o problema a ser\n"
        "   resolvido sob a perspectiva do interesse público.\n"
        f"   - Necessidade: {_txt(dados, 'objeto')}\n\n"
        "2. Demonstração da previsão da contratação no Plano de Contratações Anual,\n"
        "   indicando o alinhamento com o planejamento da Administração.\n"
        "   - [PREENCHER: PCA vigente]\n\n"
        "3. Requisitos da contratação.\n"
        "   - [PREENCHER]\n\n"
        "4. Estimativas das quantidades, acompanhadas das memórias de cálculo e dos\n"
        "   documentos que lhes dão suporte (interdependências).\n"
        "   - [PREENCHER]\n\n"
        "5. Levantamento de mercado (análise das alternativas possíveis) e\n"
        "   justificativa técnica e econômica da escolha do tipo de solução.\n"
        "   - Alternativas analisadas: 3 ou mais\n\n"
        "6. Estimativa do valor da contratação, com preços unitários referenciais,\n"
        "   memórias de cálculo e documentos de suporte.\n"
        f"   - Valor estimado: {_txt(dados, 'valor')}\n\n"
        "7. Descrição da solução como um todo, inclusive das exigências de\n"
        "   manutenção e assistência técnica, quando for o caso.\n"
        f"   - Solução: {_txt(dados, 'objeto')}\n\n"
        "8. Justificativas para o parcelamento ou não da contratação.\n"
        "   - [PREENCHER]\n\n"
        "9. Demonstrativo dos resultados pretendidos em termos de economicidade e\n"
        "   melhor aproveitamento dos recursos humanos, materiais e financeiros.\n"
        "   - [PREENCHER]\n\n"
        "10. Providências a serem adotadas pela Administração previamente à\n"
        "    celebração do contrato (capacitação de servidores etc.).\n"
        "    - [PREENCHER]\n\n"
        "11. Contratações correlatas e/ou interdependentes.\n"
        "    - [PREENCHER]\n\n"
        "12. Possíveis impactos ambientais e medidas mitigadoras.\n"
        "    - [PREENCHER]\n\n"
        "13. Posicionamento conclusivo sobre a adequação da contratação para o\n"
        "    atendimento da necessidade a que se destina.\n\n"
    )


def gerar_tr(dados: dict) -> str:
    """Termo de Referência (Estrutura em alíneas, conforme Art. 6º, XXIII, da Lei 14.133/2021)."""
    dados = dados or {}
    return (
        "# Termo de Referência (TR)\n\n"
        f"{_cabecalho(dados)}\n"
        "Base legal: Art. 6º, XXIII, da Lei nº 14.133/2021.\n\n"
        "a) Definição do objeto, incluídos sua natureza, os quantitativos, o prazo\n"
        "   do contrato e a possibilidade de prorrogação.\n"
        f"   - Objeto: {_txt(dados, 'objeto')} · Prazo: {_txt(dados, 'prazo')}\n\n"
        "b) Fundamentação da contratação (referência ao ETP ou, quando não for\n"
        "   possível divulgá-lo, extrato das partes não sigilosas).\n"
        "   - [PREENCHER]\n\n"
        "c) Descrição da solução como um todo, considerado todo o ciclo de vida do objeto.\n"
        "   - [PREENCHER]\n\n"
        "d) Requisitos da contratação.\n"
        "   - [PREENCHER]\n\n"
        "e) Modelo de execução do objeto.\n"
        "   - [PREENCHER]\n\n"
        "f) Modelo de gestão do contrato.\n"
        "   - [PREENCHER]\n\n"
        "g) Critérios de medição e de pagamento.\n"
        "   - [PREENCHER]\n\n"
        "h) Forma e critérios de seleção do fornecedor.\n"
        "   - [PREENCHER]\n\n"
        "i) Estimativas do valor da contratação, com preços unitários referenciais\n"
        "   e memórias de cálculo (parâmetros utilizados, classificados).\n"
        f"   - Valor estimado: {_txt(dados, 'valor')}\n\n"
        "j) Adequação orçamentária.\n"
        "   - [PREENCHER]\n\n"
        "Em compras: especificação do produto conforme catálogo eletrônico de\n"
        "padronização, locais de entrega e regras de recebimento provisório/definitivo.\n\n"
        "Numere o TR hierarquicamente (1, 1.1, 1.1.1), conforme a skill\n"
        "`licitacao-14133` (`reference/regras-comuns.md`).\n"
    )


def gerar_edital(dados: dict) -> str:
    """Edital (Pregão, Dispensa, Inexistibilidade, ...)."""
    dados = dados or {}
    modalidade = _txt(dados, "modalidade")
    return (
        f"# Edital: {modalidade}\n\n"
        f"{_cabecalho(dados)}\n\n"
        "## Determinação do objeto\n\n"
        f"- Objeto: {_txt(dados, 'objeto')}\n"
        f"- Prazo de validade: {_txt(dados, 'prazo')}\n\n"
        "## Modalidade de licitação\n\n"
        "- Concorrência / pregão: [PREENCHER]\n\n"
        "## Critérios de julgamento\n\n"
        "- [PREENCHER]\n\n"
        "## Prazo de propostas\n\n"
        f"- {_txt(dados, 'prazo')}\n\n"
        "## Endereço e meio de consulta aos documentos\n\n"
        "- [PREENCHER]\n\n"
        "## Anexos\n\n"
        "- [PREENCHER]\n\n"
        "## Assinaturas\n\n"
        "- Secretário/Servidor responsável: [PREENCHER]\n"
    )


def gerar_minuta_contrato(dados: dict) -> str:
    """Minuta de Contrato."""
    dados = dados or {}
    return (
        "# Minuta de Contrato\n\n"
        f"{_cabecalho(dados)}\n\n"
        f"1. Partes: {_txt(dados, 'orgao')} e o Fornecedor [PREENCHER]\n\n"
        f"2. Objeto: {_txt(dados, 'objeto')}\n\n"
        "3. Prazo de execução: [PREENCHER]\n\n"
        "4. Valor e forma de pagamento:\n"
        f"   - Valor estimado: {_txt(dados, 'valor')}\n"
        "   - Forma de pagamento: [PREENCHER]\n\n"
        "5. Prestação de contas e fiscalização: [PREENCHER]\n\n"
        "6. LGPD (quando houver dados pessoais): [PREENCHER]\n\n"
        "7. Rescisão e responsabilidades: [PREENCHER]\n\n"
        "8. Signatários: [PREENCHER]\n"
    )


def gerar_minuta_ata(dados: dict) -> str:
    """Minuta de Ata de Registro de Contratos."""
    dados = dados or {}
    return (
        "# Minuta de Ata de Registro\n\n"
        f"{_cabecalho(dados)}\n\n"
        "1. Identificação da ata:\n"
        "- Número da ata: [PREENCHER]\n"
        "- Data do registro: [PREENCHER]\n"
        "- Local: [PREENCHER]\n\n"
        "2. Partes: [PREENCHER]\n\n"
        f"3. Objeto: {_txt(dados, 'objeto')}\n\n"
        f"4. Valor estipulado: {_txt(dados, 'valor')}\n\n"
        "5. Prazo de execução: [PREENCHER]\n\n"
        "6. Condições e cláusulas relevantes: [PREENCHER]\n\n"
        "7. Declarações dos signatários: [PREENCHER]\n"
    )


def gerar_sugestao_parecer(dados: dict) -> str:
    """Sugestão de Parecer."""
    dados = dados or {}
    return (
        "# Sugestão de Parecer\n\n"
        f"{_cabecalho(dados)}\n\n"
        f"- Campo/sistema/objeto: {_txt(dados, 'objeto')}\n"
        f"- Valor sugerido: {_txt(dados, 'valor')}\n"
        f"- Prazo de aplicação: {_txt(dados, 'prazo')}\n\n"
        "## Fundamentação técnica\n\n"
        "- Análise/previsão de necessidade: [PREENCHER]\n"
        "- Comparativo de alternativas: [PREENCHER]\n\n"
        "## Recomendação\n\n"
        "- [Sugestão de parecer concreta]\n\n"
        "## Observações\n\n"
        "- [Condições, riscos, garantias a considerar]\n"
    )


def gerar_resposta_impugnacao(dados: dict) -> str:
    """Resposta de Impugnação."""
    dados = dados or {}
    return (
        "# Resposta de Impugnação\n\n"
        f"{_cabecalho(dados)}\n\n"
        f"- Processo: {_txt(dados, 'numero_processo')}\n"
        "- Impugnador: [PREENCHER]\n"
        "- Objetivo da impugnação: [PREENCHER]\n"
        "- Etapa do processo: [PREENCHER]\n"
        "- Prazo de resposta a determinar: [PREENCHER]\n\n"
        "## Resposta proposta\n\n"
        "- [PREENCHER]\n\n"
        "## Fundamentação legal\n\n"
        "- Base legal: [PREENCHER]\n"
        "- Argumentos de mérito: [PREENCHER]\n"
        "- Proposta de medida provisória (se houver): [PREENCHER]\n\n"
        "## Pedidos\n\n"
        "- [PREENCHER]\n"
    )


def gerar_analise_recurso_contraposicoes(
    dados: dict, analise: Optional[AnaliseTC] = None
) -> str:
    """Análise e Decisão de Recurso e Contraposições."""
    dados = dados or {}
    nivel = analise.tribunal_de_contas if analise else "[PREENCHER]"
    pontos = "\n".join(
        f"- {p.id}: {p.descricao} ({p.fundamento})"
        for p in (analise.pontos if analise else [])
    )
    return (
        "# Análise e Decisão de Recurso e Contraposições\n\n"
        f"{_cabecalho(dados)}\n\n"
        "1. Resumo do recurso/contestação\n"
        f"- Documento recebido: {_txt(dados, 'numero_processo')}\n"
        f"- Objetivo: {_txt(dados, 'objeto')}\n"
        "- Pontos contestados: [PREENCHER]\n\n"
        "2. Pontos do recurso com decisão\n"
        "- Ponto 1: [Autorizado/denegado]; [fundamento]\n"
        "- Ponto 2: [Autorizado/denegado]; [fundamento]\n\n"
        "3. Contraposição proposta\n"
        "- [Descrição da contraposição]\n"
        "- Argumentos de mérito: [PREENCHER]\n"
        "- Fundamentação legal: [PREENCHER]\n\n"
        "4. Decisão final\n"
        "- Decisão: [Provimento/Recusa/Medida provisória]\n"
        "- Fundamento legal: [PREENCHER]\n"
        "- Termos de acesso ao recurso junto à Administração: [PREENCHER]\n\n"
        "5. Análise crítica de Tribunais de Contas: pontos a monitorar\n"
        f"- Tribunal de Contas aplicável: {nivel}\n"
        f"- Pontos que o tribunal costuma apontar em:\n{pontos}\n"
    )
