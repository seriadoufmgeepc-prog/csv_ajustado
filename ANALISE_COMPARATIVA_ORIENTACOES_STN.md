# Análise comparativa das orientações STN x código do aplicativo

## Fonte normativa analisada

Arquivo: `MSG-RECEBIDA 150003 - 2024-3174606 ANEXO - Orientacoes STN Upload Restricoes (2)(1).pdf`.

Síntese das regras extraídas do anexo:

1. O arquivo de upload deve possuir 7 colunas, de A até G.
2. A primeira linha deve ser o Header:
   - Coluna A: `H`;
   - Coluna B: nível da conformidade, aceitando `1`, `2`, `3` ou `4`;
   - Coluna C: código do órgão responsável ou da UG responsável;
   - Coluna D: mês da conformidade, de `1` a `12`;
   - Coluna G: `|`.
3. As linhas intermediárias devem ser registros de Detalhe:
   - Coluna A: `D`;
   - Coluna B: código da UG ou órgão vinculado à conformidade;
   - Coluna C: código da restrição, numérico, com 3 posições e válido;
   - Coluna D: Motivo, alfanumérico, até 1024 posições, opcional;
   - Coluna E: Providência, alfanumérico, até 1024 posições, opcional;
   - Coluna F: Valor, numérico, até 17 posições, sem pontos ou vírgulas, com as duas últimas posições correspondentes aos centavos, opcional;
   - Coluna G: `|`.
4. A última linha deve ser o Trailer:
   - Coluna A: `T`;
   - Coluna B: quantidade de detalhes;
   - Coluna G: `|`.
5. O CSV deve ser salvo em Unicode UTF-8, com delimitador de campo `;` e delimitador de texto por aspas duplas.

## Divergências identificadas no código anterior

1. **Motivo e Providência tratados como obrigatórios**  
   O código bloqueava registros com Motivo ou Providência vazios. A orientação STN define ambos como campos opcionais.

2. **Tratamento incorreto da coluna Valor na conferência visual**  
   A coluna auxiliar `Valor em R$` interpretava o valor bruto como unidade monetária inteira. Pela regra STN, as duas últimas posições do campo Valor correspondem aos centavos. Assim, `1002356` deve ser conferido como `10.023,56`, e não como `1.002.356,00`.

3. **Validação incompleta do Valor**  
   O código não validava explicitamente o limite de 17 posições e o padrão estritamente numérico, sem pontos e vírgulas, exigido para o upload.

4. **Header com espaços em colunas vazias**  
   O gerador do CSV preenchia colunas E e F do Header com espaço em branco. O layout exige 7 colunas, mas os campos não utilizados devem permanecer vazios.

5. **Exportação com BOM UTF-8**  
   A exportação usava `utf-8-sig`. Foi ajustada para `utf-8`, mantendo aderência direta à orientação de Unicode UTF-8.

6. **Risco de truncamento silencioso de Motivo e Providência antes da validação**  
   Em alguns fluxos, os campos textuais eram limitados antes de a validação apontar excesso de 1024 caracteres. O tratamento foi ajustado para preservar o conteúdo digitado/importado até a validação, evitando truncamento indevido sem ciência do usuário.

## Correções implementadas

1. Ajustado o validador para considerar Motivo, Providência e Valor como opcionais, conforme o anexo STN.
2. Mantida a validação de UG com 6 dígitos e de Restrição com 3 dígitos, conferidas nas tabelas internas do aplicativo.
3. Incluída validação específica do Valor:
   - campo vazio aceito;
   - somente dígitos quando preenchido;
   - limite máximo de 17 posições;
   - ausência de pontos e vírgulas no valor final exportado.
4. Corrigida a coluna visual `Valor em R$` para interpretar o valor bruto como centavos.
5. Corrigida a normalização de valores informados com vírgula ou ponto decimal:
   - `10.023,56` passa a ser exportado como `1002356`;
   - `10023.56` passa a ser exportado como `1002356`;
   - `1002356` permanece como `1002356`, por já estar no padrão de upload.
6. Ajustado o gerador de CSV para produzir Header, Detalhe e Trailer com 7 colunas e campos vazios reais onde aplicável:
   - `H;1;153062;4;;;|`
   - `D;153062;300;;;1002356;|`
   - `T;1;;;;;|`
7. Mantida a ordenação por UG crescente e Restrição crescente.
8. Mantida a coluna `Valor em R$` apenas como conferência visual, sem compor o CSV final.
9. Mantida a preservação de Motivo e Providência nos fluxos de importação, digitação manual, edição e exportação.
10. Ajustada a codificação do download para UTF-8.

## Arquivos alterados

- `modules/normalizacao.py`
- `modules/validador.py`
- `modules/gerador_csv.py`
- `modules/importador_excel_csv.py`
- `app.py`

## Validação técnica realizada

Foi executada validação local das principais regras corrigidas:

- `1002356` é exibido como `10.023,56` na coluna visual.
- `10.023,56` é convertido para `1002356` no CSV.
- `10023.56` é convertido para `1002356` no CSV.
- Motivo e Providência vazios não bloqueiam a validação.
- Header, Detalhe e Trailer são gerados com 7 colunas e pipe na coluna G.
- O CSV final é gerado com delimitador `;`, aspas duplas como delimitador textual quando necessário e codificação UTF-8.
