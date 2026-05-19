# Changelog — v3 corrigida

## Entrada manual
- Mantida a estrutura original da versão v3, com ajuste pontual na grade de digitação manual.
- A coluna visual `Valor em R$` é removida antes da conversão da grade para `RegistroRestricao`, evitando interferência no CSV final.
- Os registros manuais passam a ser reordenados após a aplicação, sem alterar os campos lógicos do modelo.

## Motivo e Providência
- Preservação explícita dos campos `motivo` e `providencia` durante a leitura da grade manual, salvamento da grade filtrada e geração do CSV.
- O CSV continua usando o layout esperado: `D;UG;restrição;motivo;providência;valor;|`.

## Valor em R$
- Inclusão da coluna `Valor em R$` nas grades de edição e conferência, imediatamente após `valor`.
- A coluna aceita leitura visual de valores em formatos como `1234567.8`, `1234567,80` e `1.234.567,80`.
- A coluna é desabilitada para edição e não compõe a base final nem o CSV.

## Ordenação
- Inclusão de ordenação por UG crescente e restrição crescente nas visualizações e na exportação.
- A ordenação foi aplicada sem criação de colunas auxiliares permanentes.

## Correção adicional – importação Excel/CSV e alteração em lote

- Revisada a leitura robusta de arquivos CSV para preservar campos textuais entre aspas, inclusive quando contêm vírgulas, ponto e vírgula, barras verticais, tabulações ou quebras de linha.
- Removido o uso de leitura CSV com descarte silencioso de linhas inconsistentes, evitando que deslocamentos de coluna passem despercebidos.
- Ajustada a seleção automática de delimitador com pontuação por cabeçalhos reconhecidos e penalização de leituras que fragmentem textos em colunas artificiais.
- Corrigido o fallback de arquivos H/D/T para usar `csv.reader`, preservando corretamente Motivo e Providência quando contêm separadores internos.
- Mantida a preservação da coluna Providência na importação por Excel e CSV, sem deslocamento indevido para a coluna Valor.
- Ajustada a alteração em lote para disponibilizar somente os campos UG, Restrição, Motivo, Providência e Valor, com rótulos compatíveis com a tabela de edição.
- Incluída normalização específica por campo na alteração em lote: UG, Restrição, Valor e textos de Motivo/Providência.
