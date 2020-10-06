## Hashtable

A presente implementação traz uma tabela de dispersão usando Simple Tabulation Hashing e endereçamento aberto com tentativa linear. 

### Execução

```
python main.py -i <input-file> -o <output-file>
```

### Parâmetros

| Short | Long                  | Valor   | Valor padrão | Descrição                                                                                                            |
|-------|-----------------------|---------|--------------|----------------------------------------------------------------------------------------------------------------------|
| -i    | --input               | string  | input.txt    | Caminho do arquivo de comandos de entrada.                                                                           |
| -o    | --output              | string  | output.txt   | Caminho do arquivo de logs de saída.                                                                                 |
| -s    | --table-size          | integer | 4            | Tamanho inicial da tabela.                                                                                           |
| -d    | --doubling-threshold  | float   | 0.75         | Valor de 0 a 1 representando a porcentagem de preenchimento na qual a tabela será dobrada.               |
| -h    | --halving-threshold   | float   | 0.25         | Valor de 0 a 1 representando a porcentagem de preenchimento na qual a tabela será diminuída pela metade. |