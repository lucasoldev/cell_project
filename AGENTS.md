# Instruções do repositório

Antes de alterar este projeto, leia `docs/DEVELOPMENT.md` e os documentos da
funcionalidade em `docs/specs/`, se existirem.

- Para uma funcionalidade nova ou mudança significativa, siga o SDD completo.
  Não comece a implementação até o usuário revisar/aprovar `spec.md` e
  `plan.md`.
- Preserve o escopo e os critérios de aceitação aprovados. Se requisitos forem
  ambíguos, pergunte antes de definir comportamento de produto.
- Depois da aprovação do plano, crie ou atualize `tasks.md`, implemente por
  tarefas e registre verificações e resultados. Mantenha spec, plano e tarefas
  coerentes com a solução entregue.
- Para bugs e mudanças pequenas e localizadas, use a nota curta descrita em
  `docs/DEVELOPMENT.md`. Converta para o fluxo completo se o escopo crescer ou
  afetar contratos, dados ou mais de um domínio.
- Não crie specs retroativas para funcionalidades existentes sem uma mudança
  significativa em andamento.
- Ao concluir, informe arquivos alterados, verificações executadas e
  verificações pendentes. Não afirme que algo passou sem executar a verificação.
- Evite dependências e alterações fora do escopo aprovado.
