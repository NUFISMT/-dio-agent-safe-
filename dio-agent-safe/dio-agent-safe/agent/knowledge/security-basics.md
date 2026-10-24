# Fundamentos de Segurança da Informação

Segurança da informação é o conjunto de práticas, processos e controles que protegem dados, sistemas e pessoas contra acessos indevidos, alterações não autorizadas e indisponibilidade. Este documento é uma base de conhecimento introdutória e segue as orientações de referência do **NIST** (CSF 2.0 e série SP 800), da **OWASP** (Top 10:2025, ASVS e Cheat Sheets) e da **CISA** (Secure by Design, KEV e Cross-Sector Cybersecurity Performance Goals).

Uso educacional: o foco é entender conceitos, riscos e correções.

## Princípios de Segurança

Os três pilares clássicos, conhecidos como **tríade CIA** (Confidentiality, Integrity, Availability), são a base da definição de segurança do NIST (FIPS 199 e SP 800-53).

### Confidencialidade

Garantir que as informações sejam acessadas somente por quem tem autorização.

Controles típicos:

- classificar os dados (públicos, internos, confidenciais, pessoais/sensíveis) e proteger conforme o nível;
- criptografar dados em trânsito (TLS 1.2 ou superior, preferindo TLS 1.3, conforme NIST SP 800-52 Rev. 2) e em repouso;
- gerenciar chaves e segredos em cofres próprios, nunca no código-fonte ou em repositórios (OWASP A04:2025 – Cryptographic Failures);
- coletar e reter apenas os dados necessários (minimização, alinhada à LGPD).

### Integridade

Garantir que as informações não sejam alteradas de forma indevida ou não autorizada.

Controles típicos:

- validar toda entrada e usar consultas parametrizadas para evitar injeção (OWASP A05:2025 – Injection);
- usar hashes, assinaturas digitais e controle de versão para detectar adulterações;
- verificar a origem e a integridade de dependências, pacotes e atualizações (OWASP A03:2025 e A08:2025);
- manter trilhas de auditoria de quem alterou o quê e quando.

Exemplo de consulta insegura e sua correção:

```python
# Inseguro: concatena a entrada do usuário na query (SQL injection)
query = f"SELECT * FROM usuarios WHERE username = '{usuario}'"

# Seguro: query parametrizada
cursor.execute("SELECT * FROM usuarios WHERE username = ?", (usuario,))
```

### Disponibilidade

Garantir que sistemas continuem funcionando.

Controles típicos:

- redundância e tolerância a falhas (múltiplas instâncias, balanceamento de carga, failover);
- proteção contra negação de serviço (limitação de taxa, CDN, filtros de borda);
- planejamento de capacidade e monitoramento de desempenho;
- plano de continuidade e recuperação de desastres, com metas de RTO (tempo de recuperação) e RPO (perda máxima de dados) definidas (NIST SP 800-34 Rev. 1);
- tratar erros e condições excepcionais sem derrubar o sistema e sem expor informações (OWASP A10:2025 – Mishandling of Exceptional Conditions).

## Boas práticas

- manter sistemas atualizados;
- utilizar autenticação forte;
- aplicar menor privilégio;
- monitorar eventos;
- realizar backups;
- corrigir vulnerabilidades conhecidas.

### Manter sistemas atualizados

- Manter inventário de ativos (hardware, software, serviços em nuvem e bibliotecas). Não se protege o que não se conhece (NIST CSF 2.0, função Identify).
- Ter um processo formal de gestão de patches, com priorização por risco, janelas de manutenção e testes antes da produção (NIST SP 800-40 Rev. 4).
- Priorizar vulnerabilidades já exploradas ativamente, consultando o catálogo **KEV (Known Exploited Vulnerabilities)** da CISA, além da pontuação CVSS.
- Remover ou isolar software sem suporte do fabricante (end-of-life).
- Em aplicações, manter lista de componentes (**SBOM**) e verificar dependências diretas e transitivas (OWASP A03:2025 – Software Supply Chain Failures).
- Configurar atualizações automáticas quando for seguro fazê-lo e revisar configurações padrão (OWASP A02:2025 – Security Misconfiguration).

### Utilizar autenticação forte

- **Senhas** (NIST SP 800-63B Rev. 4, publicada em agosto de 2025): exigir no mínimo 15 caracteres quando a senha for o único fator; aceitar pelo menos 64 caracteres, inclusive espaços e Unicode; não impor regras artificiais de composição; não exigir troca periódica, apenas quando houver indício de comprometimento; bloquear senhas comuns ou vazadas; permitir gerenciadores de senha e colar texto no campo.
- **MFA**: habilitar autenticação multifator, em especial para contas administrativas, e-mail e acesso remoto. Preferir métodos **resistentes a phishing** (FIDO2/passkeys), conforme recomendações da CISA e do NIST.
- **Armazenamento**: guardar senhas apenas como hash com salt, usando algoritmos próprios para isso (Argon2id, scrypt ou bcrypt), nunca em texto puro nem com hash rápido como MD5 ou SHA-1 (OWASP Password Storage Cheat Sheet).
- **Proteção contra ataques**: limitar tentativas de login, aplicar atraso progressivo ou bloqueio temporário e evitar mensagens que revelem se o usuário existe (OWASP A07:2025 – Authentication Failures).
- **Sessões**: gerar identificadores aleatórios, expirar sessões inativas e invalidá-las no logout.

### Aplicar menor privilégio

- Conceder a cada pessoa, serviço ou aplicação somente o acesso necessário para a tarefa (NIST SP 800-53, controle AC-6).
- Adotar "negar por padrão": tudo o que não foi explicitamente permitido fica bloqueado (OWASP A01:2025 – Broken Access Control).
- Validar a autorização no servidor em toda requisição, e não apenas esconder botões ou rotas na interface.
- Usar perfis (RBAC) ou atributos (ABAC) e separar funções críticas (segregação de funções).
- Separar contas administrativas das contas de uso diário e usar elevação temporária de privilégio quando possível.
- Revisar acessos periodicamente e revogar imediatamente os de quem mudou de função ou saiu da organização.
- Usar contas de serviço com permissões mínimas e segredos rotacionados.
- Segmentar redes e adotar princípios de **Zero Trust**: nenhuma confiança implícita só por estar dentro da rede (NIST SP 800-207).

### Monitorar eventos

- Registrar eventos relevantes: logins (sucesso e falha), mudanças de privilégio, acessos a dados sensíveis, erros e alterações de configuração (OWASP A09:2025 – Security Logging & Alerting Failures).
- Não registrar senhas, tokens ou dados pessoais em texto claro nos logs.
- Centralizar os logs, protegê-los contra alteração e manter relógios sincronizados (NIST SP 800-92).
- Definir alertas acionáveis, com responsáveis e prazos de resposta. Log sem alerta e sem revisão não protege.
- Ter um plano de resposta a incidentes, testado em exercícios, com papéis, canais de comunicação e critérios de escalonamento (NIST SP 800-61 Rev. 3, alinhada ao CSF 2.0: funções Detect, Respond e Recover).
- Reportar incidentes relevantes às autoridades e partes afetadas, conforme a legislação aplicável (por exemplo, a LGPD).

### Realizar backups

- Seguir a regra **3-2-1**, recomendada pela CISA: 3 cópias dos dados, em 2 tipos diferentes de mídia, com 1 cópia fora do local (offsite).
- Manter ao menos uma cópia **offline ou imutável**, para resistir a ransomware (CISA #StopRansomware Guide).
- **Testar a restauração** periodicamente. Backup que nunca foi restaurado não é garantia.
- Criptografar os backups e controlar rigorosamente quem pode acessá-los ou apagá-los.
- Definir RTO e RPO por sistema e alinhar a frequência dos backups a esses objetivos (NIST SP 800-34 Rev. 1).
- Documentar o procedimento de recuperação e priorizar os sistemas críticos.

### Corrigir vulnerabilidades conhecidas

- Executar um ciclo contínuo: identificar, avaliar, priorizar, corrigir e verificar (NIST CSF 2.0, função Identify e Protect).
- Combinar ferramentas: análise estática (SAST), dinâmica (DAST), análise de composição de software (SCA) e testes de intrusão periódicos.
- Priorizar por risco real: exposição à internet, exploração ativa (KEV), criticidade do ativo e impacto no negócio, não apenas pelo CVSS.
- Adotar práticas de desenvolvimento seguro desde o início ("Secure by Design", CISA; NIST SP 800-218 – SSDF; OWASP ASVS): modelagem de ameaças, revisão de código e testes de segurança no pipeline de CI/CD (OWASP A06:2025 – Insecure Design).
- Quando a correção imediata não for possível, aplicar mitigação temporária (isolamento, regras de WAF, desativação do recurso) e registrar a exceção com prazo.
- Publicar um canal de divulgação responsável (por exemplo, arquivo `security.txt`) e tratar relatos com prioridade.

## Frameworks de referência

### NIST Cybersecurity Framework 2.0

Organiza a gestão de riscos de segurança em seis funções:

1. **Govern (Governar)**: estratégia, papéis, políticas e supervisão de riscos;
2. **Identify (Identificar)**: ativos, riscos e vulnerabilidades;
3. **Protect (Proteger)**: controles de acesso, treinamento, proteção de dados e manutenção;
4. **Detect (Detectar)**: monitoramento contínuo e análise de eventos;
5. **Respond (Responder)**: gestão, análise, mitigação e comunicação de incidentes;
6. **Recover (Recuperar)**: restauração das operações e lições aprendidas.

### OWASP Top 10:2025 (aplicações web)

Documento de conscientização com os dez principais riscos, publicado em novembro de 2025:

| # | Categoria |
|---|-----------|
| A01 | Broken Access Control |
| A02 | Security Misconfiguration |
| A03 | Software Supply Chain Failures |
| A04 | Cryptographic Failures |
| A05 | Injection |
| A06 | Insecure Design |
| A07 | Authentication Failures |
| A08 | Software or Data Integrity Failures |
| A09 | Security Logging & Alerting Failures |
| A10 | Mishandling of Exceptional Conditions |

O Top 10 não é um checklist completo de testes. Para verificação mais detalhada, usar o **OWASP ASVS** e os **Cheat Sheets**. Para aplicações com IA generativa, consultar também o OWASP Top 10 for LLM Applications.

### CISA

- **Secure by Design**: fabricantes assumem a responsabilidade por entregar produtos seguros por padrão, sem cobrar à parte por recursos básicos de segurança.
- **KEV Catalog**: lista de vulnerabilidades com exploração ativa confirmada, usada para priorizar correções.
- **Cross-Sector Cybersecurity Performance Goals (CPGs)**: conjunto de ações prioritárias de alto impacto para reduzir riscos, como MFA, inventário de ativos, backups, gestão de vulnerabilidades e plano de resposta a incidentes.
- **#StopRansomware**: guias de prevenção e resposta a ransomware.

### Complementos úteis

- **ISO/IEC 27001 e 27002**: sistema de gestão e controles de segurança da informação.
- **LGPD (Lei nº 13.709/2018)**: proteção de dados pessoais no Brasil, que exige medidas técnicas e administrativas de segurança.

## Referências

- NIST. *Cybersecurity Framework (CSF) 2.0*.
- NIST. *SP 800-63B Rev. 4 – Digital Identity Guidelines: Authentication and Authenticator Management* (2025).
- NIST. *SP 800-53 Rev. 5 – Security and Privacy Controls*; *SP 800-40 Rev. 4 – Enterprise Patch Management*; *SP 800-61 Rev. 3 – Incident Response*; *SP 800-34 Rev. 1 – Contingency Planning*; *SP 800-92 – Log Management*; *SP 800-207 – Zero Trust Architecture*; *SP 800-218 – SSDF*; *SP 800-52 Rev. 2 – TLS*.
- OWASP. *Top 10:2025*; *Application Security Verification Standard (ASVS)*; *Cheat Sheet Series* (https://cheatsheetseries.owasp.org).
- CISA. *Secure by Design*; *Known Exploited Vulnerabilities Catalog*; *Cross-Sector Cybersecurity Performance Goals*; *#StopRansomware Guide*.
