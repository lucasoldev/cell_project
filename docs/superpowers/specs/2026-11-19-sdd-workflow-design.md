# Workflow SDD para o Cell Project

## Contexto

O projeto começou sem um processo consistente de requisitos e planejamento. O
repositório tem aplicações Django para vários domínios, Pytest e Ruff, mas não
tem documentação de desenvolvimento além do README. O objetivo é tornar o
desenvolvimento com Codex previsível e revisável, sem introduzir um framework
externo ou exigir documentação retroativa de todo o sistema.

## Objetivos

- Registrar requisitos e critérios de aceitação antes de implementar
  funcionalidades novas.
- Manter decisões técnicas e tarefas de implementação ligadas aos requisitos.
- Dar ao Codex instruções persistentes para seguir o processo no repositório.
- Aplicar um fluxo proporcional para correções pequenas e bugs.
- Atualizar o README para apontar para instruções válidas de desenvolvimento e
  testes.

## Fora de escopo

- Instalar Spec Kit ou outra ferramenta/dependência de SDD.
- Reescrever ou documentar retroativamente as funcionalidades existentes.
- Alterar comportamento da aplicação, modelos, endpoints ou configuração de
  execução.
- Exigir documentos extensos para bugs e mudanças pequenas.

## Artefatos

Cada funcionalidade nova terá uma pasta `docs/specs/<id>-<nome>/` com:

- `spec.md`: problema, usuários afetados, objetivos, escopo, exclusões e
  critérios de aceitação observáveis.
- `plan.md`: abordagem técnica, componentes afetados, dados/interfaces,
  tratamento de erros e estratégia de validação.
- `tasks.md`: etapas pequenas e verificáveis, ligadas aos critérios de
  aceitação.

Os templates ficam em `docs/specs/_templates/`. IDs são sequenciais, em formato
`NNN`, e nomes usam kebab-case. Pastas de funcionalidades que não começaram
ficam como rascunhos; a spec deve ser revisada antes de planejar e implementar.

## Fluxo de trabalho

1. Identificar o problema e esclarecer resultado esperado e restrições.
2. Criar/revisar `spec.md`; obter concordância dos critérios de aceitação antes
   de seguir.
3. Criar `plan.md` depois da spec aprovada; revisar o plano técnico antes da
   implementação.
4. Criar `tasks.md` com tarefas pequenas e mapear cada uma para critérios de
   aceitação.
5. Implementar seguindo as tarefas e escrever testes para os comportamentos
   definidos.
6. Executar verificações relevantes (testes, Ruff e checks Django conforme a
   mudança), registrar resultados e marcar tarefas concluídas.
7. Atualizar a spec/plano se a implementação revelar uma mudança de escopo ou
   decisão; não deixar os documentos contradizerem o código entregue.

Para bugs e alterações locais, usar uma nota curta com comportamento atual,
comportamento esperado, critério de verificação e arquivos afetados. A nota
pode ficar na descrição da tarefa/issue ou em `docs/specs/` quando precisar ser
versionada; não exigir os três documentos por padrão. Funcionalidades existentes
não ganham specs retroativas, mas uma mudança significativa nelas segue o fluxo
completo.

## Instruções para o Codex

O `AGENTS.md` da raiz deve instruir o agente a:

- Ler `docs/DEVELOPMENT.md` e os documentos da funcionalidade antes de editar.
- Para funcionalidade nova, não começar código sem spec e plano revisados pelo
  usuário.
- Manter escopo e critérios de aceitação; sinalizar lacunas antes de inventar
  regras de produto.
- Implementar e verificar por tarefas, reportando verificações executadas e
  pendentes.
- Usar o fluxo curto para bugs e mudanças pequenas.
- Evitar alterar documentos não relacionados e não criar specs retrospectivas.

## README e guia de desenvolvimento

Adicionar `docs/DEVELOPMENT.md` como fonte principal do processo e ligar o
README a ele. O README deve resumir o SDD e manter instruções de setup
consistentes. Corrigir o exemplo de testes para apontar para a pasta `tests/`
existente e remover instruções obsoletas de Qwen CLI, preservando os comandos
reais do Poetry, pytest e Ruff.

## Critérios de aceitação

1. O repositório contém instruções claras para o fluxo completo de
   especificação, planejamento, tarefas, implementação e validação.
2. Templates cobrem spec, plano e tarefas com campos para critérios de
   aceitação e verificação.
3. `AGENTS.md` orienta o Codex a usar os documentos e a respeitar os pontos de
   revisão humana.
4. Bugs e alterações pequenas têm um caminho curto documentado.
5. O README aponta para o guia SDD, não recomenda comandos/ferramentas removidos
   e cita o caminho correto para testes.
6. Nenhuma dependência de runtime ou comportamento da aplicação muda.
7. Links internos e exemplos de comando dos documentos são revisados.

## Verificação

- Revisar consistência entre `AGENTS.md`, `docs/DEVELOPMENT.md`, templates e
  README.
- Executar os comandos documentados relevantes, incluindo a suíte `pytest` e
  `ruff check` nos arquivos alterados quando aplicável.
- Confirmar que a mudança contém apenas documentação de processo e instruções.
