# Prompt: Análise e Simplificação do Ecossistema de Skills e Agentes

> **Objetivo**: Avaliar, analisar e simplificar o ecossistema de skills e agents através de análise de domínio, identificação de duplicações, invasão de funções e propostas de consolidação para tornar o sistema mais enxuto, conciso e objetivo.

---

## 🎯 Contexto e Escopo

### Estrutura do Ecossistema

O ecossistema está distribuído em **3 plataformas isoladas**:

```
/workspace/
├── .agent/          # Plataforma Antigravity (Gemini/Windsurf)
│   ├── agents/      # 20 agentes especialistas
│   ├── skills/      # ~75 skills (SKILL.md)
│   ├── workflows/   # 17 workflows
│   └── rules/       # 4 regras globais
│
├── .claude/         # Plataforma Claude
│   ├── agents/      # 20 agentes especialistas
│   ├── skills/      # ~75 skills (SKILL.md)
│   └── commands/    # 17 comandos
│
└── .cursor/         # Plataforma Cursor
    ├── agents/      # 20 agentes especialistas
    ├── skills/      # ~75 skills (SKILL.mdc)
    ├── commands/    # 17 comandos
    └── rules/       # 4 regras globais
```

### Princípios Fundamentais

1. **Isolamento de Plataformas**: As 3 plataformas devem permanecer isoladas e independentes
2. **Conteúdo Espelhado**: Apesar de metadatas diferentes, o conteúdo é similar entre plataformas
3. **Modificação Sincronizada**: Alterações em uma skill/agent devem ser replicadas nas equivalentes
4. **Links Auto-contidos**: Todos os links devem referenciar apenas a própria plataforma
5. **Sem Documentos Órfãos**: Nenhum documento deve ficar sem referências após simplificações

---

## 📊 Fase 1: Análise de Domínio e Inventário

### 1.1 Mapeamento de Agentes

**Objetivo**: Identificar sobreposições de responsabilidade entre agentes

**Análise Requerida**:

| Análise | Descrição | Métrica |
|---------|-----------|---------|
| **Cobertura de Domínio** | Identificar domínios cobertos por cada agente | Lista de domínios por agente |
| **Sobreposição de Expertise** | Detectar agentes com áreas de expertise idênticas ou muito similares | % de overlap entre pares |
| **Ambiguidade de Ativação** | Verificar se triggers de ativação são únicos | Score de ambiguidade (0-100) |
| **Utilização Real** | Analisar frequência de uso (se dados disponíveis) | Ranking de uso |
| **Dependências de Skills** | Mapear quais skills cada agente utiliza | Grafo de dependências |

**Perguntas Críticas**:
- [ ] Existem agentes com descrições muito similares que confundem a LLM?
- [ ] Há agentes que nunca são ativados por falta de clareza de escopo?
- [ ] Existem pares de agentes que poderiam ser mesclados sem perda de funcionalidade?
- [ ] Algum agente tem escopo tão amplo que invade território de outros?
- [ ] Existem agentes com escopo tão estreito que poderiam ser skills ao invés?

**Candidatos para Análise de Merge**:
```
Analisar especialmente:
- backend-specialist vs database-architect
- test-engineer vs qa-automation-engineer
- product-manager vs product-owner
- documentation-writer vs code-archaeologist (se houver overlap)
- performance-optimizer vs devops-engineer (na área de performance)
```

### 1.2 Mapeamento de Skills

**Objetivo**: Identificar duplicação de conteúdo e invasão funcional entre skills

**Análise Requerida**:

| Análise | Descrição | Métrica |
|---------|-----------|---------|
| **Taxonomia de Domínios** | Classificar skills por domínio técnico | Árvore de categorização |
| **Similaridade de Conteúdo** | Comparar conteúdo normalizado entre skills | Score de similaridade (0-100%) |
| **Overlap Funcional** | Identificar skills que ensinam as mesmas práticas | Lista de overlaps |
| **Completude Individual** | Verificar se cada skill é auto-suficiente | % de completude |
| **Referências Cruzadas** | Mapear skills que referenciam outras | Grafo de dependências |
| **Scripts e Automações** | Inventariar scripts por skill | Lista de scripts ativos |
| **Tamanho e Complexidade** | Medir linhas de código/documentação | Métricas de tamanho |

**Perguntas Críticas**:
- [ ] Existem skills com conteúdo >80% idêntico que deveriam ser mescladas?
- [ ] Há skills muito genéricas que deveriam ser divididas?
- [ ] Existem skills muito específicas que deveriam ser seções de outras?
- [ ] Alguma skill tem escopo tão amplo que deveria ser um agente?
- [ ] Existem skills órfãs (nunca referenciadas por agentes)?
- [ ] Há duplicação de scripts entre skills diferentes?

**Categorias para Análise Específica**:

**Frontend (5-7 skills)**:
```
Analisar duplicação entre:
- nextjs-react-expert vs frontend-development
- web-design-guidelines vs frontend-design
- ui-ux-pro-max vs frontend-design
- tailwind-patterns vs ui-styling
```

**Backend (4-6 skills)**:
```
Analisar duplicação entre:
- api-patterns vs backend-development
- nodejs-best-practices vs backend-development
- python-patterns (se backend-related)
```

**Database (2-3 skills)**:
```
Analisar se database-design é suficiente ou se há overlap
```

**Testing (5-6 skills)**:
```
Analisar duplicação entre:
- testing-patterns vs test-driven-development
- tdd-workflow vs test-driven-development
- webapp-testing (específico) vs testing-patterns (genérico)
```

**Game Development (7-8 skills)**:
```
Analisar se todas são necessárias:
- game-development (genérico)
- game-design, game-audio, game-art (específicos)
- 2d-games, 3d-games, pc-games, web-games, mobile-games (plataformas)
- multiplayer (feature-specific)

Possível consolidação: game-development como core + especializações
```

**Architecture & Planning (4+ skills)**:
```
Analisar duplicação entre:
- app-builder vs architecture
- plan-writing vs brainstorming
- problem-solving vs sequential-thinking
```

**Meta-Skills (criar/migrar)**:
```
Analisar necessidade de todas:
- create-skill, create-rule, create-subagent
- migrate-to-skills
- using-superpowers

Podem ser consolidadas em uma única "meta-development" skill?
```

### 1.3 Análise de Rules e Commands

**Rules (4)**:
```
- coding-style
- gemini (orquestração master)
- git
- toc (navegação)
```

**Perguntas**:
- [ ] Há overlap entre coding-style e clean-code (que é skill)?
- [ ] A rule "toc" poderia ser um script ao invés de rule?

**Commands/Workflows (17)**:
```
Analisar duplicação funcional entre:
- brainstorm vs plan
- create vs implement
- enhance vs refactor
- debug vs fix
```

---

## 🔍 Fase 2: Detecção de Problemas Específicos

### 2.1 Invasão de Funções

**Definição**: Quando um agente/skill executa funções que são responsabilidade primária de outro

**Como Detectar**:

```python
# Algoritmo de Detecção de Invasão
Para cada par (A, B) de agentes/skills:
  1. Extrair domínios de A e B
  2. Calcular overlap: intersection(domains_A, domains_B)
  3. Se overlap > 40%:
     - Se A é mais específico que B: OK (especialização)
     - Se A e B estão no mesmo nível: INVASÃO DETECTADA
  4. Analisar descrições e conteúdo com NLP/embedding similarity
  5. Gerar relatório de invasão com score
```

**Output Esperado**:
```markdown
## Relatório de Invasão de Funções

### Alta Severidade (>60% overlap)
- **backend-specialist** invade **database-architect** em: schema design, migrations
- **frontend-design** invade **ui-ux-pro-max** em: color systems, typography

### Média Severidade (40-60% overlap)
- **testing-patterns** invade **tdd-workflow** em: test structure, AAA pattern

### Baixa Severidade (20-40% overlap)
- ...
```

### 2.2 Duplicação de Conteúdo

**Definição**: Quando 2+ skills/agents contêm conteúdo idêntico ou muito similar

**Como Detectar**:

```python
# Algoritmo de Detecção de Duplicação
Para cada par (SkillA, SkillB):
  1. Normalizar conteúdo (remover metadata, whitespace, platform refs)
  2. Calcular hash similarity ou embedding distance
  3. Se similarity > 80%:
     - DUPLICAÇÃO COMPLETA → Merge obrigatório
  4. Se similarity > 60%:
     - DUPLICAÇÃO PARCIAL → Analisar seções específicas
  5. Extrair seções duplicadas específicas
  6. Gerar relatório de duplicação
```

**Output Esperado**:
```markdown
## Relatório de Duplicação de Conteúdo

### Duplicação Completa (>80% similar)
- **test-driven-development** e **tdd-workflow**: 95% idênticos
  - Proposta: Manter test-driven-development, deprecar tdd-workflow

### Duplicação Parcial (60-80% similar)
- **frontend-design** e **ui-ux-pro-max**: 72% similar
  - Seções duplicadas: Color Systems, Typography Rules
  - Proposta: Consolidar seções comuns, especializar diferenças

### Duplicação de Scripts
- `mobile-design/scripts/mobile_audit.py` vs `ui-ux-pro-max/scripts/design_system.py`
  - Overlap: Funções de análise de contraste
  - Proposta: Extrair para biblioteca comum
```

### 2.3 Documentos Órfãos (Dangling Documents)

**Definição**: Skills/agents que não são referenciados por nenhum outro documento

**Como Detectar**:

```python
# Algoritmo de Detecção de Órfãos
1. Construir grafo de referências:
   - Nós: Todos os documentos (agents, skills, rules, commands)
   - Arestas: Links/referências entre documentos

2. Identificar nós com in-degree = 0:
   - Skills sem referências de agents
   - Agents sem referências de commands/rules
   - Referencias internas que não apontam para nada

3. Verificar se são entry points válidos:
   - Rules sempre são entry points
   - Commands sempre são entry points
   - Agents referenciados em gemini.md são entry points
   - Skills referenciadas em agent frontmatter são entry points

4. Documentos órfãos = nós sem in-degree E não são entry points
```

**Output Esperado**:
```markdown
## Relatório de Documentos Órfãos

### Skills Órfãs (não referenciadas por nenhum agent)
- **rust-pro**: Nenhum agent lista essa skill
  - Ação: Adicionar ao backend-specialist ou deprecar

### Referencias Quebradas
- `.agent/agents/frontend-specialist.md` referencia `ui-framework-chooser`
  - Skill não existe em nenhuma plataforma
  - Ação: Remover referência ou criar skill

### Scripts Órfãos
- `.cursor/skills/performance-profiling/scripts/unused_analyzer.py`
  - Não é mencionado no SKILL.mdc
  - Ação: Documentar uso ou remover
```

---

## 💡 Fase 3: Propostas de Simplificação

### 3.1 Estratégias de Merge

**Estratégia 1: Merge Vertical (Especialização → Genérico)**

```
Quando: Skill específica pode ser seção de skill genérica

Exemplo:
  ANTES: 
    - testing-patterns (genérico)
    - tdd-workflow (específico)
    - test-driven-development (específico)
  
  DEPOIS:
    - testing-patterns (único)
      - Seção: TDD Workflow
      - Seção: BDD Patterns
      - Seção: Integration Testing
```

**Estratégia 2: Merge Horizontal (Similar Nivel → Consolidado)**

```
Quando: 2+ skills/agents de mesmo nível com overlap alto

Exemplo:
  ANTES:
    - product-manager
    - product-owner
  
  DEPOIS:
    - product-specialist
      - Perfis: Manager Mode vs Owner Mode
      - Seção: Product Strategy (PM)
      - Seção: Backlog Management (PO)
```

**Estratégia 3: Extração de Common Core**

```
Quando: Múltiplas skills compartilham conteúdo comum

Exemplo:
  ANTES:
    - frontend-design (com color system, typography)
    - mobile-design (com color system, typography)
    - ui-ux-pro-max (com color system, typography)
  
  DEPOIS:
    - design-fundamentals (novo - core common)
    - frontend-design (específico web)
    - mobile-design (específico mobile)
    - ui-ux-pro-max (avançado/tools)
```

**Estratégia 4: Deprecation (Remover sem Substituir)**

```
Quando: Skill/agent raramente usado e funcionalidade não é crítica

Exemplo:
  - using-superpowers → Conteúdo pode ir para README.md
  - update-cursor-settings → Específico demais, pode ser script
```

### 3.2 Matriz de Decisão para Merge

Para cada par de candidatos a merge, avaliar:

| Critério | Peso | Score (0-10) | Comentário |
|----------|------|--------------|------------|
| **Similaridade de Conteúdo** | 30% | ? | >8 = forte candidato |
| **Overlap de Domínio** | 25% | ? | >7 = forte candidato |
| **Ambiguidade de Ativação** | 20% | ? | >6 = confusão de LLM |
| **Baixo Uso Individual** | 15% | ? | >5 = pouco impacto |
| **Facilidade de Merge** | 10% | ? | >7 = merge simples |
| **SCORE TOTAL** | 100% | **?** | >7.0 = MERGE RECOMENDADO |

### 3.3 Template de Proposta de Simplificação

Para cada merge/simplificação proposta:

```markdown
## Proposta: Merge de [A] e [B]

### Análise
- **Overlap de Conteúdo**: X%
- **Overlap de Domínio**: Y%
- **Score de Decisão**: Z/10
- **Severidade**: Alta/Média/Baixa

### Justificativa
[Explicar por que o merge faz sentido]

### Estratégia
- Tipo: Merge Vertical / Horizontal / Extração / Deprecation
- Documento Resultante: [nome]
- Plataformas Afetadas: .agent, .claude, .cursor

### Conteúdo Resultante
**Estrutura Proposta**:
```
# [Nome da Skill/Agent Consolidado]

## Seção 1: [de A]
...

## Seção 2: [de B]
...

## Seção 3: [novo - unificação]
...
```

### Impacto em Referências

**Agents que referenciam A**:
- frontend-specialist.md → Atualizar para novo nome
- backend-specialist.md → Atualizar para novo nome

**Skills que referenciam A**:
- app-builder/SKILL.md linha 45 → Atualizar link
- architecture/SKILL.md linha 120 → Atualizar link

**Agents que referenciam B**:
- [lista]

**Skills que referenciam B**:
- [lista]

### Plano de Migração

**Fase 1: Preparação**
1. Criar nova skill consolidada em `.agent/skills/[novo-nome]/`
2. Migrar conteúdo consolidado de A e B
3. Reconciliar links internos

**Fase 2: Atualização de Referências**
1. Atualizar frontmatter de agents que usam A ou B
2. Atualizar links em outras skills
3. Verificar dangling documents

**Fase 3: Sincronização Cross-Platform**
1. Replicar para `.claude/skills/[novo-nome]/SKILL.md`
2. Replicar para `.cursor/skills/[novo-nome]/SKILL.mdc`
3. Ajustar platform-specific paths

**Fase 4: Deprecation**
1. Mover A e B para `.deprecated/` (não deletar ainda)
2. Adicionar warning em A e B apontando para novo
3. Validar sem erros de referências

**Fase 5: Cleanup**
1. Após período de validação, deletar A e B
2. Atualizar documentação (toc.md, ARCHITECTURE.md)

### Validação
- [ ] Script de links não retorna erros
- [ ] Nenhum documento órfão criado
- [ ] Conteúdo sincronizado nas 3 plataformas
- [ ] Metadata corretas por plataforma
- [ ] Tests e scripts migrados

### Risco
- **Baixo**: Merge simples, poucas referências
- **Médio**: Merge com reestruturação, múltiplas referências
- **Alto**: Merge de componentes core, muitas dependências
```

---

## 🛠️ Fase 4: Execução e Reconciliação

### 4.1 Reconciliação de Links

**Algoritmo**:

```python
# Reconciliação de Links Durante Merge
def reconcile_links_on_merge(old_skill_A, old_skill_B, new_skill):
    """
    Reconcilia todos os links quando A e B são mesclados em new_skill
    """
    all_platforms = ['.agent', '.claude', '.cursor']
    
    for platform in all_platforms:
        # 1. Encontrar todos os arquivos que referenciam A ou B
        referencing_files = find_files_referencing(
            platform, 
            [old_skill_A, old_skill_B]
        )
        
        for file_path in referencing_files:
            # 2. Substituir referências
            content = read_file(file_path)
            
            # Substituir referências em frontmatter (skills: list)
            content = replace_in_frontmatter(
                content,
                old_values=[old_skill_A, old_skill_B],
                new_value=new_skill
            )
            
            # Substituir links markdown
            content = replace_markdown_links(
                content,
                old_paths=[
                    f'{platform}/skills/{old_skill_A}',
                    f'{platform}/skills/{old_skill_B}'
                ],
                new_path=f'{platform}/skills/{new_skill}'
            )
            
            # Substituir referências textuais
            content = replace_text_references(
                content,
                old_names=[old_skill_A, old_skill_B],
                new_name=new_skill
            )
            
            write_file(file_path, content)
        
        # 3. Verificar órfãos
        check_for_orphans(platform)
        
        # 4. Validar links
        validate_all_links(platform)
```

### 4.2 Detecção de Órfãos Pós-Merge

```python
def detect_dangling_docs_after_merge(deleted_docs, platform):
    """
    Após deletar/mover docs A e B, verificar se criamos órfãos
    """
    all_docs = get_all_documents(platform)
    reference_graph = build_reference_graph(all_docs)
    
    # Entry points: rules, commands, agents listados em gemini.md
    entry_points = get_entry_points(platform)
    
    # Busca em largura a partir de entry points
    reachable = breadth_first_search(reference_graph, entry_points)
    
    # Documentos não alcançáveis = órfãos
    orphans = set(all_docs) - reachable
    
    # Filtrar false positives (assets, scripts internos, etc)
    true_orphans = filter_true_orphans(orphans)
    
    return true_orphans
```

### 4.3 Sincronização Cross-Platform

**Protocolo de Sincronização**:

```markdown
Para cada modificação em Platform A:

1. **Extrair Conteúdo Core**
   - Ler arquivo modificado em Platform A
   - Separar metadata de conteúdo
   - Normalizar conteúdo (remover refs específicas de A)

2. **Encontrar Equivalente nas Outras Plataformas**
   - Platform B: mesmo nome, extensão B-specific
   - Platform C: mesmo nome, extensão C-specific
   - Se não existir: criar

3. **Aplicar Conteúdo**
   - Preservar metadata específica de B e C
   - Aplicar conteúdo normalizado
   - Ajustar platform-specific paths:
     - `.agent/` → `.claude/` ou `.cursor/`
     - `SKILL.md` → `SKILL.mdc` (se .cursor)

4. **Validar**
   - Content hash deve ser similar (após normalização)
   - Links devem apontar para mesma estrutura relativa
   - Metadata deve seguir specs da plataforma

5. **Commit Atômico**
   - Commitar as 3 plataformas juntas
   - Mensagem: "sync: [descrição] across platforms"
```

---

## 📋 Fase 5: Relatórios e Métricas

### 5.1 Relatório de Simplificação

```markdown
# Relatório de Simplificação do Ecossistema

## Executive Summary

**Objetivo**: Reduzir complexidade mantendo qualidade e funcionalidade

**Resultados**:
- Skills: 75 → 52 (31% redução)
- Agents: 20 → 17 (15% redução)
- Linhas de documentação: ~45,000 → ~32,000 (29% redução)
- Duplicação de conteúdo: 35% → 8%
- Documentos órfãos: 12 → 0

## Detalhamento

### Skills Mescladas (23)

| Antes | Depois | Estratégia | Impacto |
|-------|--------|------------|---------|
| test-driven-development + tdd-workflow | testing-patterns (expandido) | Merge Vertical | 15 referências atualizadas |
| product-manager + product-owner | product-specialist | Merge Horizontal | 8 referências atualizadas |
| ... | ... | ... | ... |

### Agents Mesclados (3)

| Antes | Depois | Estratégia | Impacto |
|-------|--------|------------|---------|
| test-engineer + qa-automation-engineer | qa-specialist | Merge Horizontal | 12 referências atualizadas |
| ... | ... | ... | ... |

### Skills Deprecadas (5)

| Skill | Razão | Conteúdo Migrado Para |
|-------|-------|----------------------|
| using-superpowers | Muito específico | README.md |
| update-cursor-settings | Operacional | Script utilitário |
| ... | ... | ... |

## Melhorias de Qualidade

### Ambiguidade de Ativação
- Antes: Score médio 6.2/10 (alto = ruim)
- Depois: Score médio 2.8/10 (baixo = bom)

### Clareza de Domínio
- Overlaps >40%: 18 pares → 3 pares
- Overlaps >60%: 5 pares → 0 pares

### Manutenibilidade
- Documentos com duplicação: 42 → 9
- Scripts duplicados: 8 pares → 0 pares
- Links quebrados: 23 → 0

## Impacto Cross-Platform

- Arquivos modificados: 180 (60 por plataforma)
- Commits de sincronização: 35
- Content hash accuracy: 98.5%
- Links reconciliados: 456
- Zero documentos órfãos criados

## Validação

- ✅ `ecosystem_audit.py --fail-on=high`: PASS
- ✅ Todos os links válidos em todas as plataformas
- ✅ Metadata specs respeitadas por plataforma
- ✅ Conteúdo sincronizado (hash similarity >95%)
- ✅ Nenhum documento órfão
- ✅ Testes de ativação de LLM: 100% sucesso

## Recomendações Futuras

1. **Revisão Trimestral**: Auditar overlaps a cada 3 meses
2. **Freeze de Novos Skills**: Avaliar necessidade antes de criar novos
3. **Monitoramento de Uso**: Implementar telemetria para identificar skills pouco usadas
4. **Automação**: Script de detecção de duplicação em CI/CD
```

### 5.2 Métricas de Sucesso

| Métrica | Baseline | Meta | Resultado | Status |
|---------|----------|------|-----------|--------|
| **Duplicação de Conteúdo** | 35% | <10% | 8% | ✅ |
| **Overlaps de Domínio >40%** | 18 pares | <5 pares | 3 pares | ✅ |
| **Documentos Órfãos** | 12 | 0 | 0 | ✅ |
| **Ambiguidade Média** | 6.2/10 | <3.5/10 | 2.8/10 | ✅ |
| **Redução de Skills** | 75 | 60 | 52 | ✅ |
| **Redução de Agents** | 20 | 18 | 17 | ✅ |
| **Sincronização Cross-Platform** | 87% | 95% | 98.5% | ✅ |
| **Links Quebrados** | 23 | 0 | 0 | ✅ |

---

## 🚀 Plano de Execução Sugerido

### Sprint 1: Análise e Inventário (3-5 dias)
- [ ] Executar análise de domínio completa
- [ ] Gerar relatórios de invasão e duplicação
- [ ] Identificar candidatos para merge (top 20)
- [ ] Calcular matriz de decisão para cada candidato

### Sprint 2: Propostas Detalhadas (2-3 dias)
- [ ] Criar proposta detalhada para cada merge
- [ ] Validar propostas (revisão por humano ou LLM experiente)
- [ ] Priorizar por impacto e risco
- [ ] Criar plano de migração por merge

### Sprint 3-4: Execução de Merges (5-7 dias)
- [ ] Executar merges de baixo risco primeiro
- [ ] Reconciliar links em cada merge
- [ ] Sincronizar cross-platform após cada merge
- [ ] Validar ausência de órfãos após cada merge
- [ ] Commit atômico por merge

### Sprint 5: Validação e Ajustes (2-3 dias)
- [ ] Executar ecosystem_audit.py
- [ ] Testar ativação de LLM em cenários reais
- [ ] Ajustar descrições se houver ambiguidade
- [ ] Validar links em todas as plataformas
- [ ] Gerar relatório final

### Sprint 6: Documentação (1-2 dias)
- [ ] Atualizar ARCHITECTURE.md
- [ ] Atualizar toc.md / toc skill
- [ ] Criar CHANGELOG.md detalhado
- [ ] Documentar decisões de merge
- [ ] Criar guia de manutenção

---

## 🎯 Outputs Esperados

Ao final da execução deste prompt, devem ser gerados:

1. **Relatórios de Análise**:
   - `DOMAIN_ANALYSIS_REPORT.md` - Mapeamento de domínios e overlaps
   - `DUPLICATION_REPORT.md` - Lista de duplicações detectadas
   - `INVASION_REPORT.md` - Casos de invasão de funções
   - `ORPHAN_DOCUMENTS_REPORT.md` - Documentos sem referências

2. **Propostas de Simplificação**:
   - `MERGE_PROPOSALS.md` - Lista de merges propostos com justificativas
   - `DEPRECATION_PROPOSALS.md` - Skills/agents a deprecar
   - `EXTRACTION_PROPOSALS.md` - Common cores a extrair

3. **Planos de Migração**:
   - `MIGRATION_PLAN_[MERGE_NAME].md` (um por merge)
   - `CROSS_PLATFORM_SYNC_PLAN.md`

4. **Scripts de Automação**:
   - `detect_domain_overlap.py` - Detectar overlaps automaticamente
   - `detect_content_duplication.py` - Detectar duplicações
   - `detect_orphans.py` - Detectar órfãos
   - `reconcile_links.py` - Reconciliar links durante merges
   - `sync_cross_platform.py` - Sincronizar entre plataformas

5. **Relatório Final**:
   - `SIMPLIFICATION_REPORT.md` - Relatório executivo completo
   - `METRICS_BEFORE_AFTER.json` - Métricas comparativas

---

## 🔧 Scripts de Apoio Recomendados

### Script 1: Análise de Overlap de Domínio

```python
#!/usr/bin/env python3
"""
detect_domain_overlap.py - Detecta overlap de domínios entre agentes/skills
"""

import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import difflib

def extract_domains_from_description(description: str) -> Set[str]:
    """
    Extrai domínios de uma descrição usando keywords
    """
    keywords = {
        'frontend': ['react', 'vue', 'ui', 'css', 'html', 'component', 'styling', 'responsive'],
        'backend': ['api', 'server', 'nodejs', 'python', 'endpoint', 'middleware'],
        'database': ['sql', 'nosql', 'schema', 'migration', 'query', 'orm'],
        'testing': ['test', 'tdd', 'bdd', 'unit', 'integration', 'e2e', 'playwright'],
        'security': ['auth', 'security', 'vulnerability', 'owasp', 'encryption'],
        'devops': ['deploy', 'ci/cd', 'docker', 'kubernetes', 'pipeline'],
        'mobile': ['ios', 'android', 'react native', 'flutter', 'mobile'],
        'design': ['ux', 'ui', 'design', 'typography', 'color', 'layout'],
        'performance': ['performance', 'optimization', 'profiling', 'metrics'],
    }
    
    desc_lower = description.lower()
    detected_domains = set()
    
    for domain, terms in keywords.items():
        if any(term in desc_lower for term in terms):
            detected_domains.add(domain)
    
    return detected_domains

def calculate_overlap(domains_a: Set[str], domains_b: Set[str]) -> float:
    """
    Calcula % de overlap entre dois conjuntos de domínios
    """
    if not domains_a or not domains_b:
        return 0.0
    
    intersection = domains_a & domains_b
    union = domains_a | domains_b
    
    return (len(intersection) / len(union)) * 100 if union else 0.0

def analyze_domain_overlaps(workspace: Path, category: str) -> Dict:
    """
    Analisa overlaps para uma categoria (agents ou skills)
    """
    platforms = ['.agent', '.claude', '.cursor']
    items = {}
    
    # Coletar de uma plataforma (assume .agent como source of truth)
    if category == 'agents':
        items_dir = workspace / '.agent' / 'agents'
        for file_path in items_dir.glob('*.md'):
            with open(file_path, 'r') as f:
                content = f.read()
                # Extrair descrição (assumindo format padrão)
                # Você pode melhorar isso parseando YAML frontmatter
                items[file_path.stem] = extract_domains_from_description(content)
    
    elif category == 'skills':
        items_dir = workspace / '.agent' / 'skills'
        for skill_dir in items_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / 'SKILL.md'
                if skill_file.exists():
                    with open(skill_file, 'r') as f:
                        content = f.read()
                        items[skill_dir.name] = extract_domains_from_description(content)
    
    # Calcular overlaps entre todos os pares
    overlaps = []
    item_names = list(items.keys())
    
    for i in range(len(item_names)):
        for j in range(i + 1, len(item_names)):
            name_a = item_names[i]
            name_b = item_names[j]
            overlap_pct = calculate_overlap(items[name_a], items[name_b])
            
            if overlap_pct > 20:  # Threshold: 20%
                overlaps.append({
                    'pair': (name_a, name_b),
                    'overlap_pct': overlap_pct,
                    'domains_a': items[name_a],
                    'domains_b': items[name_b],
                    'common_domains': items[name_a] & items[name_b]
                })
    
    # Ordenar por overlap descendente
    overlaps.sort(key=lambda x: x['overlap_pct'], reverse=True)
    
    return overlaps

def generate_overlap_report(overlaps: List[Dict], category: str) -> str:
    """
    Gera relatório markdown de overlaps
    """
    lines = [f"# Relatório de Overlap de Domínios - {category.title()}\n"]
    lines.append(f"Total de pares com overlap >20%: {len(overlaps)}\n")
    lines.append("---\n")
    
    # Severidade
    high = [o for o in overlaps if o['overlap_pct'] >= 60]
    medium = [o for o in overlaps if 40 <= o['overlap_pct'] < 60]
    low = [o for o in overlaps if 20 <= o['overlap_pct'] < 40]
    
    for severity, items in [('Alta (≥60%)', high), ('Média (40-59%)', medium), ('Baixa (20-39%)', low)]:
        lines.append(f"## {severity} - {len(items)} pares\n")
        
        for item in items:
            name_a, name_b = item['pair']
            lines.append(f"### {name_a} ↔ {name_b}\n")
            lines.append(f"- **Overlap**: {item['overlap_pct']:.1f}%\n")
            lines.append(f"- **Domínios Comuns**: {', '.join(item['common_domains'])}\n")
            lines.append(f"- **Proposta**: ANALISAR PARA MERGE\n")
            lines.append("\n")
    
    return ''.join(lines)

if __name__ == '__main__':
    workspace = Path('/workspace')
    
    print("Analisando overlaps de AGENTS...")
    agent_overlaps = analyze_domain_overlaps(workspace, 'agents')
    report_agents = generate_overlap_report(agent_overlaps, 'agents')
    
    with open(workspace / 'docs/refactoring/reports/AGENT_DOMAIN_OVERLAPS.md', 'w') as f:
        f.write(report_agents)
    
    print(f"✓ Relatório de agents gerado: {len(agent_overlaps)} overlaps detectados")
    
    print("Analisando overlaps de SKILLS...")
    skill_overlaps = analyze_domain_overlaps(workspace, 'skills')
    report_skills = generate_overlap_report(skill_overlaps, 'skills')
    
    with open(workspace / 'docs/refactoring/reports/SKILL_DOMAIN_OVERLAPS.md', 'w') as f:
        f.write(report_skills)
    
    print(f"✓ Relatório de skills gerado: {len(skill_overlaps)} overlaps detectados")
```

### Script 2: Detecção de Conteúdo Duplicado

```python
#!/usr/bin/env python3
"""
detect_content_duplication.py - Detecta duplicação de conteúdo entre skills
"""

import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple
from difflib import SequenceMatcher

def normalize_content(content: str) -> str:
    """
    Normaliza conteúdo removendo metadata e refs específicas
    """
    # Remover frontmatter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Remover platform-specific paths
    content = re.sub(r'\.agent/', '{platform}/', content)
    content = re.sub(r'\.claude/', '{platform}/', content)
    content = re.sub(r'\.cursor/', '{platform}/', content)
    
    # Normalizar whitespace
    content = re.sub(r'\s+', ' ', content)
    
    return content.strip()

def calculate_similarity(content_a: str, content_b: str) -> float:
    """
    Calcula similaridade entre dois conteúdos (0-100%)
    """
    return SequenceMatcher(None, content_a, content_b).ratio() * 100

def detect_duplications(workspace: Path) -> List[Dict]:
    """
    Detecta duplicações entre skills
    """
    skills_data = {}
    
    # Ler todas as skills de .agent
    skills_dir = workspace / '.agent' / 'skills'
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir():
            skill_file = skill_dir / 'SKILL.md'
            if skill_file.exists():
                content = skill_file.read_text()
                normalized = normalize_content(content)
                skills_data[skill_dir.name] = {
                    'content': normalized,
                    'size': len(normalized)
                }
    
    # Comparar todos os pares
    duplications = []
    skill_names = list(skills_data.keys())
    
    for i in range(len(skill_names)):
        for j in range(i + 1, len(skill_names)):
            name_a = skill_names[i]
            name_b = skill_names[j]
            
            similarity = calculate_similarity(
                skills_data[name_a]['content'],
                skills_data[name_b]['content']
            )
            
            if similarity > 60:  # Threshold
                duplications.append({
                    'pair': (name_a, name_b),
                    'similarity_pct': similarity,
                    'size_a': skills_data[name_a]['size'],
                    'size_b': skills_data[name_b]['size']
                })
    
    duplications.sort(key=lambda x: x['similarity_pct'], reverse=True)
    return duplications

def generate_duplication_report(duplications: List[Dict]) -> str:
    """
    Gera relatório de duplicações
    """
    lines = ["# Relatório de Duplicação de Conteúdo\n\n"]
    lines.append(f"Total de pares com similaridade >60%: {len(duplications)}\n\n")
    lines.append("---\n\n")
    
    complete = [d for d in duplications if d['similarity_pct'] >= 80]
    partial = [d for d in duplications if 60 <= d['similarity_pct'] < 80]
    
    lines.append(f"## Duplicação Completa (≥80%) - {len(complete)} pares\n\n")
    for dup in complete:
        name_a, name_b = dup['pair']
        lines.append(f"### {name_a} ↔ {name_b}\n")
        lines.append(f"- **Similaridade**: {dup['similarity_pct']:.1f}%\n")
        lines.append(f"- **Tamanhos**: {dup['size_a']} vs {dup['size_b']} chars\n")
        lines.append(f"- **Proposta**: MERGE OBRIGATÓRIO\n\n")
    
    lines.append(f"## Duplicação Parcial (60-79%) - {len(partial)} pares\n\n")
    for dup in partial:
        name_a, name_b = dup['pair']
        lines.append(f"### {name_a} ↔ {name_b}\n")
        lines.append(f"- **Similaridade**: {dup['similarity_pct']:.1f}%\n")
        lines.append(f"- **Tamanhos**: {dup['size_a']} vs {dup['size_b']} chars\n")
        lines.append(f"- **Proposta**: ANALISAR SEÇÕES DUPLICADAS\n\n")
    
    return ''.join(lines)

if __name__ == '__main__':
    workspace = Path('/workspace')
    
    print("Detectando duplicações de conteúdo...")
    duplications = detect_duplications(workspace)
    
    report = generate_duplication_report(duplications)
    
    output_path = workspace / 'docs/refactoring/reports/CONTENT_DUPLICATION_REPORT.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"✓ Relatório gerado: {len(duplications)} duplicações detectadas")
    print(f"✓ Salvo em: {output_path}")
```

### Script 3: Detecção de Documentos Órfãos

```python
#!/usr/bin/env python3
"""
detect_orphans.py - Detecta documentos órfãos (sem referências)
"""

import re
from pathlib import Path
from typing import Dict, Set, List
from collections import defaultdict

def build_reference_graph(workspace: Path, platform: str) -> Dict[str, Set[str]]:
    """
    Constrói grafo de referências para uma plataforma
    Returns: {documento: set(documentos_que_referencia)}
    """
    graph = defaultdict(set)
    platform_dir = workspace / platform
    
    # Padrões de referência
    skill_ref_pattern = re.compile(r'skills:\s*([^\n]+)', re.MULTILINE)
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    
    # Percorrer todos os .md/.mdc files
    for file_path in platform_dir.rglob('*'):
        if file_path.suffix not in ['.md', '.mdc']:
            continue
        
        try:
            content = file_path.read_text()
        except:
            continue
        
        doc_id = str(file_path.relative_to(platform_dir))
        
        # Referências em frontmatter (skills:)
        for match in skill_ref_pattern.finditer(content):
            skills_str = match.group(1)
            skills = [s.strip() for s in skills_str.split(',')]
            for skill in skills:
                if skill:
                    graph[doc_id].add(f'skills/{skill}/SKILL')
        
        # Referências em links markdown
        for match in link_pattern.finditer(content):
            link_target = match.group(2)
            
            # Ignorar links externos e âncoras
            if link_target.startswith(('http', '#')):
                continue
            
            # Normalizar path
            if link_target.startswith('./'):
                link_target = link_target[2:]
            
            # Resolver relativo ao arquivo atual
            target_path = (file_path.parent / link_target).resolve()
            
            try:
                target_rel = target_path.relative_to(platform_dir)
                graph[doc_id].add(str(target_rel))
            except:
                pass
    
    return graph

def find_entry_points(workspace: Path, platform: str) -> Set[str]:
    """
    Identifica entry points (documentos que são pontos de entrada válidos)
    """
    entry_points = set()
    
    # Rules são sempre entry points
    rules_dir = workspace / platform / 'rules'
    if rules_dir.exists():
        for rule_file in rules_dir.glob('*'):
            entry_points.add(str(rule_file.relative_to(workspace / platform)))
    
    # Commands/workflows são entry points
    if platform == '.agent':
        cmd_dir = workspace / platform / 'workflows'
    else:
        cmd_dir = workspace / platform / 'commands'
    
    if cmd_dir.exists():
        for cmd_file in cmd_dir.glob('*.md'):
            entry_points.add(str(cmd_file.relative_to(workspace / platform)))
    
    # Agents são entry points
    agents_dir = workspace / platform / 'agents'
    if agents_dir.exists():
        for agent_file in agents_dir.glob('*.md'):
            entry_points.add(str(agent_file.relative_to(workspace / platform)))
    
    return entry_points

def find_reachable(graph: Dict[str, Set[str]], entry_points: Set[str]) -> Set[str]:
    """
    BFS para encontrar todos os documentos alcançáveis a partir dos entry points
    """
    reachable = set(entry_points)
    queue = list(entry_points)
    
    while queue:
        current = queue.pop(0)
        
        if current in graph:
            for neighbor in graph[current]:
                if neighbor not in reachable:
                    reachable.add(neighbor)
                    queue.append(neighbor)
    
    return reachable

def detect_orphans(workspace: Path, platform: str) -> List[str]:
    """
    Detecta documentos órfãos em uma plataforma
    """
    # Todos os documentos
    platform_dir = workspace / platform
    all_docs = set()
    
    for category in ['agents', 'skills', 'rules', 'commands', 'workflows']:
        cat_dir = platform_dir / category
        if cat_dir.exists():
            for file_path in cat_dir.rglob('*'):
                if file_path.suffix in ['.md', '.mdc']:
                    all_docs.add(str(file_path.relative_to(platform_dir)))
    
    # Grafo e entry points
    graph = build_reference_graph(workspace, platform)
    entry_points = find_entry_points(workspace, platform)
    
    # Documentos alcançáveis
    reachable = find_reachable(graph, entry_points)
    
    # Órfãos = não alcançáveis
    orphans = sorted(all_docs - reachable)
    
    return orphans

def generate_orphans_report(workspace: Path) -> str:
    """
    Gera relatório de órfãos para todas as plataformas
    """
    lines = ["# Relatório de Documentos Órfãos\n\n"]
    
    platforms = ['.agent', '.claude', '.cursor']
    
    for platform in platforms:
        orphans = detect_orphans(workspace, platform)
        
        lines.append(f"## {platform}\n\n")
        
        if not orphans:
            lines.append("✅ Nenhum documento órfão detectado.\n\n")
        else:
            lines.append(f"❌ **{len(orphans)} documentos órfãos detectados:**\n\n")
            
            for orphan in orphans:
                lines.append(f"- `{orphan}`\n")
                
                # Ação sugerida
                if 'skills/' in orphan:
                    lines.append(f"  - **Ação**: Adicionar à lista `skills:` de algum agent\n")
                elif 'agents/' in orphan:
                    lines.append(f"  - **Ação**: Referenciar em command ou gemini.md\n")
                else:
                    lines.append(f"  - **Ação**: Analisar se ainda é necessário\n")
            
            lines.append("\n")
    
    return ''.join(lines)

if __name__ == '__main__':
    workspace = Path('/workspace')
    
    print("Detectando documentos órfãos...")
    report = generate_orphans_report(workspace)
    
    output_path = workspace / 'docs/refactoring/reports/ORPHAN_DOCUMENTS_REPORT.md'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"✓ Relatório gerado: {output_path}")
```

---

## 📚 Referências

- Audit Script Existente: `/workspace/scripts/ecosystem/ecosystem_audit.py`
- Documentação Anterior: `/workspace/docs/refactoring/ECOSYSTEM_REVIEW_PROMPT.md`
- Arquitetura: `/workspace/.cursor/ARCHITECTURE.md` (e equivalentes)

---

## ✅ Checklist de Completude

Ao executar este prompt, verifique se todos os itens foram cobertos:

- [ ] Análise de domínio completa (agents e skills)
- [ ] Relatórios de invasão de funções gerados
- [ ] Relatórios de duplicação de conteúdo gerados
- [ ] Relatórios de documentos órfãos gerados
- [ ] Matriz de decisão calculada para candidatos a merge
- [ ] Propostas detalhadas criadas para cada simplificação
- [ ] Planos de migração documentados
- [ ] Scripts de automação desenvolvidos
- [ ] Execução de merges com reconciliação de links
- [ ] Sincronização cross-platform validada
- [ ] Ausência de documentos órfãos pós-merge confirmada
- [ ] Ecosystem audit script executado com sucesso
- [ ] Relatório final de simplificação gerado
- [ ] Métricas before/after documentadas
- [ ] Documentação atualizada (ARCHITECTURE.md, toc, etc)

---

**Versão**: 1.0  
**Data**: 2026-02-10  
**Autor**: Sistema de Simplificação de Ecossistema  
**Status**: Pronto para Execução
