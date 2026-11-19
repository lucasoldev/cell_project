# Processo de desenvolvimento

Este repositório usa **Spec Driven Development (SDD)** para que cada mudança
comece com um resultado esperado claro e tenha uma forma objetiva de validação.
O processo usa Markdown e Git; não exige instalar ferramentas adicionais.

## Quando usar cada fluxo

Use o fluxo completo para funcionalidades novas ou mudanças que alterem regras
de negócio, dados, contratos de API, permissões ou a interação entre partes do
sistema.

Use uma nota curta para bugs e mudanças pequenas, localizadas e de baixo risco.
Se a investigação revelar mudança de escopo, impacto em vários domínios, dados
ou contratos usados por outros componentes, pare e converta o trabalho para o
fluxo completo antes de implementar.

Não crie especificações retroativas para todo o sistema. Uma funcionalidade
existente só precisa de uma spec quando receber uma mudança significativa.

## Fluxo completo

Cada funcionalidade fica em `docs/specs/<NNN>-<nome-kebab-case>/`. Use o
próximo identificador numérico disponível; `_templates/` contém apenas modelos
e não ocupa um identificador.

1. **Entenda o problema.** Registre quem precisa da mudança, o resultado
   esperado, as restrições e as perguntas em aberto.
2. **Escreva `spec.md`.** Descreva problema, objetivos, escopo, exclusões,
   requisitos e critérios de aceitação numerados e observáveis. Marque a spec
   como `Rascunho`.
3. **Revise a spec com o usuário.** Apresente os critérios e aguarde aprovação
   antes de elaborar a solução técnica. Não invente regras de produto para
   preencher lacunas.
4. **Escreva `plan.md`.** Explique a abordagem técnica, arquivos/componentes
   afetados, dados e interfaces, tratamento de erros e estratégia de
   validação. Relacione decisões aos critérios de aceitação.
5. **Revise o plano com o usuário.** Aguarde aprovação antes de implementar.
6. **Escreva `tasks.md`.** Divida o plano em tarefas pequenas e verificáveis;
   cada tarefa deve referenciar os critérios que atende e indicar como será
   verificada.
7. **Implemente e valide.** Siga as tarefas, adicione ou atualize testes para
   os comportamentos acordados e execute as verificações pertinentes ao
   impacto da mudança. Registre resultados e marque tarefas concluídas.
8. **Mantenha os documentos coerentes.** Se surgir uma decisão que mude escopo
   ou critérios, atualize a spec e obtenha aprovação antes de seguir. Atualize
   o plano e as tarefas quando a abordagem mudar.

Copie os arquivos de `docs/specs/_templates/` para a pasta da funcionalidade.
Use `Rascunho`, `Aprovada` e `Concluída` no campo de status; registre quem
revisou/aprovou e quando. Critérios de aceitação recebem IDs estáveis, como
`AC-1`; planos e tarefas referenciam esses IDs para manter rastreabilidade.

## Nota curta para bug ou mudança pequena

Registre na issue/tarefa ou em `docs/specs/` se a decisão precisar ficar
versionada:

```markdown
### Nota de mudança
- Comportamento atual:
- Comportamento esperado:
- Critério de verificação:
- Arquivos/áreas afetadas:
- Escopo reavaliado? (não / sim — explicar)
```

Se houver impacto além da área localizada, critérios de aceitação novos ou
decisões técnicas que afetem outros componentes, use o fluxo completo.

## Validação

Escolha verificações que correspondam aos critérios e à mudança. Para o
backend, os comandos principais são:

```bash
poetry run pytest
poetry run ruff check
poetry run python manage.py check
```

Registre quais comandos foram executados e seus resultados em `tasks.md`. Não
declare uma verificação como aprovada se ela não foi executada; liste o que
ficou pendente.
