# 🤖🛡️ DIO Agent Safe

> Especialização do [DIO Agent](https://github.com/digitalinnovationone/dio-agent) em **AppSec (segurança de aplicações)**, feita para o Desafio de Projeto "Entendendo o Desafio".

Este repositório parte do DIO Agent original e, sem treinar nenhum modelo, ensina o agente — via arquivos em Markdown — a conduzir uma análise de vulnerabilidade como um profissional de segurança faria: entendendo o contexto antes de agir, avaliando impacto, probabilidade e severidade, e só então orientando a correção.

---

## 🎯 A especialização, e por quê

O DIO Agent original é um mentor de estudos geral. Faltava a ele uma habilidade específica: olhar para código ou infraestrutura e raciocinar como alguém de segurança, em vez de só explicar um conceito.

Escolhi **AppSec** porque é um tipo de análise onde o processo importa mais que a resposta: um agente que solta "troque por consulta parametrizada" sem explicar o risco, sem avaliar o impacto real e sem citar uma referência técnica confiável ensina pouco — e, pior, pode incentivar o estudante a aceitar a resposta sem entender por quê. A especialização resolve isso dando ao agente um processo fixo (entender → coletar → explicar risco → classificar → corrigir → prevenir) e limites claros do que ele não deve fazer (como gerar exploits prontos ou sugerir comandos destrutivos sem confirmação).

## 📁 Arquivos criados ou alterados

| Arquivo | O que é |
|---|---|
| `skills/vulnerability-analysis/SKILL.MD` | A skill nova: o processo de 6 passos que o agente segue, com as regras defensivas (nunca gerar exploit pronto, nunca sugerir comando destrutivo sem backup, nunca rotular algo como "crítico" sem justificar impacto/probabilidade/severidade). |
| `skills/vulnerability-analysis/README.MD` | Explica a skill para pessoas: objetivo, fluxo e como o agente aplica isso na prática. |
| `agent/knowledge/security-basics.md` | Base de conhecimento: vulnerabilidade, ameaça, risco, a tríade confidencialidade/integridade/disponibilidade, boas práticas e os frameworks de referência (NIST, OWASP, CISA). |
| `agent/persona.md` *(alterado)* | Novo trecho "Especialização: mentor de AppSec", descrevendo como o agente se comporta nessa especialização. |
| `AGENTS.md` *(alterado)* | Nova linha na tabela de skills, apontando para `skills/vulnerability-analysis/SKILL.MD`, e referência ao novo arquivo de conhecimento. |
| `agent/app.py` | Exemplo de login **corrigido**, usado para validar a correção (consulta parametrizada + hash de senha com salt). |
| `agent/app_vulneravel.py` | Versão **original**, com SQL Injection, usada como alvo de teste da skill. Mantida no repositório como evidência do "antes". |
| `docs/appsec-sql-injection.html` | Página interativa "Quando texto vira SQL", criada pelo próprio agente durante a conversa, comparando interpolação insegura com consulta parametrizada. |

## ▶️ Como rodar o agente no harness

1. Instale um harness compatível com `AGENTS.md` (neste projeto foi usado o **Hermes**; Claude Code, Antigravity, Codex e Cursor também funcionam).
2. Baixe este repositório (`git clone` ou Download ZIP) e **abra o harness com o terminal já dentro desta pasta** — se ele abrir em outro lugar, não encontra os arquivos do agente.
3. Converse normalmente. O harness lê `AGENTS.md` automaticamente; o agente lê `agent/persona.md` e, quando o assunto for segurança, usa `skills/vulnerability-analysis/SKILL.MD` e consulta `agent/knowledge/security-basics.md`.

Para reproduzir a análise feita neste projeto:

```
Atue como especialista em AppSec. Leia o arquivo app.py nesta pasta.
Identifique se tem alguma vulnerabilidade crítica. Explique como um
atacante poderia explorá-la.
```

(use `agent/app_vulneravel.py` como alvo para ver a falha, e `agent/app.py` para ver a versão já corrigida)

## ✨ A melhoria escolhida

Além do pedido mínimo (skill + conhecimento + ajustes de persona e `AGENTS.md`), a skill foi escrita para cobrir **dois cenários, não só código**:

1. **Análise de código**, com classificação técnica (MITRE ATT&CK, CWE, CAPEC, OWASP) e reescrita segura.
2. **Análise de infraestrutura** (ex.: "tenho um servidor Ubuntu exposto na internet") — aqui o agente nunca parte para comandos de alteração. Ele primeiro pede apenas comandos de diagnóstico somente leitura (`ss -lntup`, `ufw status verbose`, `cat /etc/os-release`), lembra de fazer backup antes de qualquer mudança e nunca pede para o estudante colar senhas, chaves ou tokens.

Essa diferenciação veio de uma conversa real com o agente durante o desenvolvimento e é a diferença entre um agente que "responde sobre segurança" e um que **se comporta com cautela** diante de um sistema real.

---

## 🧩 As skills do agente

| Skill | Para que serve |
|-------|----------------|
| [Plano de estudos](skills/study-plan/SKILL.md) | Organiza o que estudar, em que ordem e em quanto tempo |
| [Destravar desafio](skills/unblock-challenge/SKILL.md) | Conduz você até a solução de um desafio, sem dar a resposta pronta |
| [Explicar conceito](skills/explain-concept/SKILL.md) | Explica conceitos de forma didática, com analogias e exemplos |
| [Pesquisa na web](skills/web-search/SKILL.md) | Fundamenta respostas com busca atual e fontes citadas |
| [Análise de vulnerabilidades](skills/vulnerability-analysis/SKILL.MD) | Analisa uma possível falha de segurança em código ou infraestrutura, como um profissional de AppSec faria |

## 🗂️ Estrutura do repositório

```
dio-agent-safe/
├── README.md                              Este guia
├── AGENTS.md                              Definição do agente (lida por qualquer harness)
├── CLAUDE.md                              Atalho para o Claude Code
│
├── agent/
│   ├── app.py                             Login corrigido (consulta parametrizada + hash)
│   ├── app_vulneravel.py                  Login original, com SQL Injection (alvo de teste)
│   ├── persona.md                         Personalidade do agente + especialização AppSec
│   └── knowledge/
│       ├── dio-platform.md                O que é a DIO
│       ├── learning-experiences.md        Os formatos de aprendizado da DIO
│       └── security-basics.md             Fundamentos de segurança (NIST, OWASP, CISA)
│
├── skills/
│   ├── README.md                          O que são skills
│   ├── study-plan/                        Skill: plano de estudos
│   ├── unblock-challenge/                 Skill: destravar desafio
│   ├── explain-concept/                   Skill: explicar conceito
│   ├── web-search/                        Skill: pesquisa na web
│   └── vulnerability-analysis/            Skill nova: análise de vulnerabilidades
│       ├── SKILL.MD
│       └── README.MD
│
└── docs/
    ├── glossary.md                        Glossário de termos
    ├── youcom-mcp.md                      Documentação do MCP da you.com
    └── appsec-sql-injection.html          Página interativa "Quando texto vira SQL"
```

---

## 🙏 Créditos

Baseado no [DIO Agent](https://github.com/digitalinnovationone/dio-agent), da [Digital Innovation One](https://dio.me), desenvolvido como parte do Desafio de Projeto "Entendendo o Desafio".
