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

## Correção adicional — aderência ao anexo STN de Upload de Restrições

- Corrigido o tratamento dos campos Motivo e Providência, que passaram a ser opcionais conforme o layout STN.
- Corrigida a regra do Valor: campo numérico de até 17 posições, sem pontos ou vírgulas, com as duas últimas posições correspondentes aos centavos.
- Corrigida a coluna visual Valor em R$ para interpretar o valor bruto como centavos.
- Ajustado o CSV final para Header, Detalhe e Trailer com 7 colunas, campos vazios reais e pipe na coluna G.
- Alterada a codificação do download para UTF-8.
- Preservado o conteúdo de Motivo e Providência até a validação, evitando truncamento silencioso antes da conferência do usuário.
