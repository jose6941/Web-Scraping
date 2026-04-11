<div align="center">
  <h1>Teste Técnico Estágio Instar</h1>
</div>

</br>

<p align="center">
  Este repositório contém três partes do teste técnico:
</p>

</br>

- **Raciocínio Lógico em Python:**  Tratamento e formatação de dados JSON.  
- **Consultas em Banco de Dados SQL:**  Queries para clientes e pedidos.  
- **Extração de Dados com Scrapy:**  Spider que coleta informações do site Books.toScrape.  

---
## Sites

- https://sandbox.oxylabs.io/products.
- https://www.scrapethissite.com/pages/.
- https://quotes.toscrape.com/.

## Raciocínio Lógico em Python

Consiste em realizar uma série de tratamentos nos dados, para garantir que os dados estejam formatados corretamente e prontos para uso em um sistema.  

### Passos principais
- Remoção de caracteres indesejados (`NBSP`, espaços extras).  
- Conversão e padronização de datas.  
- Substituição de marcadores (`...`) em títulos.  
- Transformação de listas em strings.  
- Remoção de chaves nulas ou substituição por valores padrão.  

## Lógica do código

</br>

1. **Leitura do arquivo JSON:**
 Abre o arquivo original `teste_estagio_instar.json` e carrega os dados em memória usando `json.load()`.

```bash

    # Abre o arquivo json no modo leitura
    with open(file_path, "r", encoding="utf-8") as f:

        # Guarda o arquivo em uma variável
        arquivo = json.load(f)

```

</br>

2. **Limpeza de campos de texto:**
 Remove caracteres especiais como `\xa0` e espaços extras usando a função `strip()` dos campos `nome`, `sobrenome` e `titulo`.  

```bash

    # Analise cada chave para remover o caracter especial
    for chave in ["nome", "sobrenome", "titulo"]:
        if chave in item and item[chave]:

            # Substitui o caracter especial por espaço e depois 
            # remove esse espaço, deixando-o formatado
            item[chave] = item[chave].replace("\xa0", " ").strip()

```

</br>

3. **Padronização de datas:**
 Utiliza a função `converter_data()` para tenta converter datas no formato `"dd/mm/yyyy HH:MM:SS"`, se caso for o formato sem o horário, converte no formato `"dd/mm/yyyy"`. Assim ele retorna a data no padrão `"YYYY-MM-DD HH:MM:SS"`. Escolhi fazer uma função para conversão de datas para facilitar a conversão dos dois tipos que foram pedidos, o dataRealizacao e a data dentro dos arquivos.

```bash

    def converter_data(data): 
        try: 

            # Tenta converter primeiro a string da data que está no formato ("%d/%m/%Y %H:%M:%S")
            data_original = datetime.strptime(data, "%d/%m/%Y %H:%M:%S") 
        except ValueError: 

            # Caso não seja o primeiro formato, a string será convertida no formato ("%d/%m/%Y")
            data_original = datetime.strptime(data, "%d/%m/%Y") 

        # Retorno a data já convertida em string, se caso não tiver o horário, 
        # sera colocado como 00:00:00
        return data_original.strftime("%Y-%m-%d %H:%M:%S")
       
```

```bash

   # Convertendo dataRealizacao
    if "dataRealizacao" in item:
        data_original = item["dataRealizacao"] 
        item["dataRealizacao"] = converter_data(item["dataRealizacao"]) 
       
```

```bash

   # Convertendo data para cada objeto dos arquivos
    for arq in item["arquivos"]: 
        arq["data"] = converter_data(arq["data"]) 
       
```

</br>

4. **Formatação de títulos:**
 Se o campo `titulo` contiver "...", substitui pela data e hora correspondente ao item, no formato `"dd/mm/yyyy às HH:MM:SS"`, que foi guardado na variável data_original.

```bash

    # Verfica se a chave titulo está contido no arquivo e 
    # se há "..." na string
    if "titulo" in item and "..." in item["titulo"]:

        # Converte a data original da dataRealizacao para o 
        # formato ("%d/%m/%Y %H:%M:%S")
        dt = datetime.strptime(data_original, "%d/%m/%Y %H:%M:%S")

        # Seapra a data original em dois formatos, data e hora
        data_fmt = dt.strftime("%d/%m/%Y")
        hora_fmt = dt.strftime("%H:%M:%S")

        # Substitui o "..." pelos formatos da data original, 
        # data e hora
        item["titulo"] = item["titulo"].replace("...", f"{data_fmt} às {hora_fmt}")

```

</br>

5. **Remoção de valores nulos:**
 Remove chaves com valor "None" ,Para o objeto "arquivos",percebi que na saída desejada os valores nulos não foram excluídos, logo os valores nulos foram substituídos por strings vazias, como estava no arquivo de saída.

```bash

    # Para cada chave do arquivo json que tiver campo nulo, 
    # será armazenado em um vetor para depois serem deletadas
    chaves_remover = [chave for chave, valor in item.items() if valor is None] 
    for chave in chaves_remover: 

        # Deleta as chaves nulas que foram encontradas no arquivo json
        del item[chave] 

        # Verifica todos os valores das chaves do objeto "arquivos"
        for arq in item["arquivos"]: 

            # Armazena os valores nulos em um vetor
            chaves_remover = [chave for chave, valor in arq.items() if valor is None] 

            for chave in chaves_remover: 
                # Substitui os valores nulos por string vazia
                arq[chave] = ""

```

</br>

6. **Concatenação de listas:**
 Se o campo `descricao` for uma lista, converte para uma única string separada por espaços.

```bash

    # Verifica se o valor da chave "descricao" é uma lista
    if isinstance(item.get("descricao"), list):

        # Junta todos os valores da lista em uma única string 
        # separado por espaço
        item["descricao"] = " ".join(item["descricao"])
    
    # Armazena apenas as chaves que não forem nulas
    item_limpo = {chave: valor for chave, valor in item.items() if valor is not None}
    arquivo[arquivo.index(item)] = item_limpo

```

</br>

7. **Criação do arquivo final:**
 Salva os dados tratados em "teste_estagio_instar_tratado.json" usando json.dump() com indentação e codificação UTF-8.

```bash

    # Arquivo de saída
    output_path = "teste_estagio_instar_tratado.json"

    # Abre o arquivo de saída como escrita
    with open(output_path, "w", encoding="utf-8") as f:

        # Grava o arquivo no formato json no arquivo de saída
        json.dump(arquivo, f, indent=4, ensure_ascii=False)

```
8. **Resultado:**

Arquivo json formatado

```bash

[
    {
        "nome": "João",
        "sobrenome": "Silva de Oliveira",
        "dataRealizacao": "2015-12-31 08:30:00",
        "titulo": "O evento será dia 31/12/2015 às 08:30:00 às 31/12/2015 às 08:30:00",
        "descricao": "o evento será realizado no auditório da Prefeitura Municipal de 
         Penápolis às 08:30 horas",
        "arquivos": [
            {
                "arquivo": "https://www.evento.com.br/uploads/2016/01/capa-evento.pdf",
                "titulo": "",
                "data": "2016-01-11 00:00:00"
            },
            {
                "arquivo": "https://www.evento.com.br/uploads/2016/01/capa-evento2.pdf",
                "titulo": "Capa do evento",
                "data": "2016-01-12 00:00:00"
            }
        ]
    }
]

```

</br>

## Consulta em banco de dados SQL

Consiste na criação de consultas entre tabelas de clientes e pedidos. Obtendo todos os clientes que realizaram pedidos acima de R$ 100, ordenados pelo nome e o total de pedidos realizados por cada cliente.  

### Passos principais
- Criar as tabelas de clientes e pedidos
- Fazer um SELECT que retorne todos os clientes que realizaram pedidos acima de R$ 100, ordenados pelo nome.  
- Fazer um SELECT que retorne o total de pedidos realizados por cada cliente.   

## Lógica do código

</br>

1. **Criação das tabelas:**

Cria as tabelas de clientes e pedidos com seus respectivos campos e chaves.

```bash

    CREATE TABLE clientes(
        id INT PRIMARY KEY AUTO_INCREMENT,
        nome VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );

```

```bash

    CREATE TABLE pedidos(
        id INT PRIMARY KEY AUTO_INCREMENT,
        id_clientes INT NOT NULL,
        data DATE NOT NULL,
        total DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (id_clientes) REFERENCES clientes(id)
    );
    
```

</br>

2. **Consulta dos clientes que fizeram algum pedido:**

Neste código há um SELECT para todos os clientes que realizaram pedidos acima de R$ 100, ordenados pelo nome. Foi utilizado o inner join, que foi escrito apenas join, para retornar apenas os clientes que possuem pelo menos um pedido acima de R$ 100.

```bash

    SELECT DISTINCT c.id,c.nome, c.email # Seleciona os cliente evitando os campos duplicados
    FROM clientes c 
    JOIN pedidos p ON c.id = p.id_clientes # Retorna os clientes que possuem algum pedido
    WHERE p.total > 100 # Apenas para pedidos acima de R$ 100
    ORDER BY c.nome; # Ordenado por nome
    
```

</br>

3. **Consulta do total de pedidos realizados por cada cliente:**

Neste código há um SELECT para mostrar quantos pedidos foram feitos para cada cliente, mesmo que o mesmo não tenha nenhum. Dessa forma foi utilizado o LEFT JOIN, para mostrar todos os clientes mesmo que algum não tenha feito nenhum pedido.

```bash

    SELECT c.id, c.nome, COUNT(p.id) AS total_pedidos # Pega as informações do cliente e o numero de pedidos
    FROM clientes c
    LEFT JOIN pedidos p ON c.id = p.id_clientes # Retorna todos os clientes, mesmo os que não têm pedidos
    GROUP BY c.id, c.nome # Agrupa os resultados por id e nome do cliente
    ORDER BY total_pedidos DESC; # Ordena pelo total de pedidos de forma decrescente
    
```

</br>

## Extração de Dados com Scrapy

consiste em implementar um código que extrai as informações da página books.toscrape utilizando a biblioteca Scrapy do Python, tudo isso em um ambiente virtual.  

### Passos principais
- Criar um ambiente virtual
- Criar o projeto e o spider.  
- Criar o código para extrair os dados do site.
- Executar o spider gerando arquivo em json.   

## Lógica do código

</br>

1. **Criando ambiente virtual:**

Dentro da pasta do projeto, executo os seguintes comandos para criar, ativar o ambiente virtual em python

```bash

    python -m venv "nome do ambiente" # Cria o ambiente virtual

    cd "nome do ambiente" # Entra na pasta do ambiente

    Scripts\activate # Ativa o ambiente

```

</br>

2. **Criando o projeto junto com o spider:**

Dentro da pasta do ambiente virtual, instale a biblioteca scrapy, inicie o projeto scrapy e crie o arquivo do spider com os seguintes comandos

```bash

    pip install scrapy # Instala a biblioteca scrapy

    scrapy startproject "nome do projeto" # Inicia o projeto scrapy

    cd "nome do projeto" # Entra na pasta do projeto

    scrapy genspider "nome do arquivo" "url do site" # Cria o spider com o link do site 

```

</br>

3. **Criando o código para extrair os dados do site:**

Dentro do arquivo spider que foi criado, foi feito os comando para extrair as informações de todos os livros dentro da primeira página, utilizando o comando "response.css" para pegar os valores das classes em css.

```bash

    import scrapy

    class BooksSpider(scrapy.Spider):

        # Nome do arquivo executável e URL da página que terá os dados obtidos
        name = "books"
        start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):

        # Percorre todos os cards dos livros da página por meio da class css
        for livro in response.css('.product_pod'):

            # Retorna as informações de imagem, título, preço e disponibilidade 
            # de estoque de todos os livros da primeira página
            yield{
                "imagem": livro.css('.thumbnail ::attr(src)').get(), 
                "titulo":  livro.css('.product_pod h3 a ::text').get(),
                "preco": livro.css('.price_color ::text').get(),
                "estoque": livro.xpath('//p[@class="instock availability"]/text()[2]').get().strip()
            }

```

</br>

4. **Executando o spider para gerar arquivo json:**

Feito o código, é possível rodar o arquivo spider com as informações no terminal ou exportar em algum formato, nesse caso iremos gerar o arquivo em json

```bash

    scrapy crawl books # Executa o spider mostrando os dados no terminal

    scrapy crawl books -O "nome_do_arquivo.json" # Gera arquivo no formato json

```

</br>

5. **Resultado:**

Arquivo json com a imagem, título, preço e estoque dos livros

```bash

[
    {"imagem": "media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg", "titulo": "A Light in the ...", "preco": "£51.77", "estoque": "In stock"},
    {"imagem": "media/cache/26/0c/260c6ae16bce31c8f8c95daddd9f4a1c.jpg", "titulo": "Tipping the Velvet", "preco": "£53.74", "estoque": "In stock"},
    {"imagem": "media/cache/3e/ef/3eef99c9d9adef34639f510662022830.jpg", "titulo": "Soumission", "preco": "£50.10", "estoque": "In stock"},
    {"imagem": "media/cache/32/51/3251cf3a3412f53f339e42cac2134093.jpg", "titulo": "Sharp Objects", "preco": "£47.82", "estoque": "In stock"},
    {"imagem": "media/cache/be/a5/bea5697f2534a2f86a3ef27b5a8c12a6.jpg", "titulo": "Sapiens: A Brief History ...", "preco": "£54.23", "estoque": "In stock"},
    {"imagem": "media/cache/68/33/68339b4c9bc034267e1da611ab3b34f8.jpg", "titulo": "The Requiem Red", "preco": "£22.65", "estoque": "In stock"},
    {"imagem": "media/cache/92/27/92274a95b7c251fea59a2b8a78275ab4.jpg", "titulo": "The Dirty Little Secrets ...", "preco": "£33.34", "estoque": "In stock"},
    {"imagem": "media/cache/3d/54/3d54940e57e662c4dd1f3ff00c78cc64.jpg", "titulo": "The Coming Woman: A ...", "preco": "£17.93", "estoque": "In stock"},
    {"imagem": "media/cache/66/88/66883b91f6804b2323c8369331cb7dd1.jpg", "titulo": "The Boys in the ...", "preco": "£22.60", "estoque": "In stock"},
    {"imagem": "media/cache/58/46/5846057e28022268153beff6d352b06c.jpg", "titulo": "The Black Maria", "preco": "£52.15", "estoque": "In stock"},
    {"imagem": "media/cache/be/f4/bef44da28c98f905a3ebec0b87be8530.jpg", "titulo": "Starving Hearts (Triangular Trade ...", "preco": "£13.99", "estoque": "In stock"},
    {"imagem": "media/cache/10/48/1048f63d3b5061cd2f424d20b3f9b666.jpg", "titulo": "Shakespeare's Sonnets", "preco": "£20.66", "estoque": "In stock"},
    {"imagem": "media/cache/5b/88/5b88c52633f53cacf162c15f4f823153.jpg", "titulo": "Set Me Free", "preco": "£17.46", "estoque": "In stock"},
    {"imagem": "media/cache/94/b1/94b1b8b244bce9677c2f29ccc890d4d2.jpg", "titulo": "Scott Pilgrim's Precious Little ...", "preco": "£52.29", "estoque": "In stock"},
    {"imagem": "media/cache/81/c4/81c4a973364e17d01f217e1188253d5e.jpg", "titulo": "Rip it Up and ...", "preco": "£35.02", "estoque": "In stock"},
    {"imagem": "media/cache/54/60/54607fe8945897cdcced0044103b10b6.jpg", "titulo": "Our Band Could Be ...", "preco": "£57.25", "estoque": "In stock"},
    {"imagem": "media/cache/55/33/553310a7162dfbc2c6d19a84da0df9e1.jpg", "titulo": "Olio", "preco": "£23.88", "estoque": "In stock"},
    {"imagem": "media/cache/09/a3/09a3aef48557576e1a85ba7efea8ecb7.jpg", "titulo": "Mesaerion: The Best Science ...", "preco": "£37.59", "estoque": "In stock"},
    {"imagem": "media/cache/0b/bc/0bbcd0a6f4bcd81ccb1049a52736406e.jpg", "titulo": "Libertarianism for Beginners", "preco": "£51.33", "estoque": "In stock"},
    {"imagem": "media/cache/27/a5/27a53d0bb95bdd88288eaf66c9230d7e.jpg", "titulo": "It's Only the Himalayas", "preco": "£45.17", "estoque": "In stock"}
]

```

6. **Exemplo**

```bash

import scrapy

class NoticiasSpider(scrapy.Spider):
    name = "noticias"
    start_urls = ["https://exemplo.com/noticias"]

    def parse(self, response):
        links = response.xpath('//div[@class="noticia"]/a/@href').getall()

        for link in links:
            yield response.follow(link, callback=self.parse_noticia)

        proxima_pagina = response.xpath('//a[@class="next"]/@href').get()
        if proxima_pagina:
            yield response.follow(proxima_pagina, callback=self.parse)

    def parse_noticia(self, response):
        titulo = response.xpath('//h1/text()').get()
        data = response.xpath('//span[@class="data"]/text()').get()
        texto = response.xpath('//div[@class="conteudo"]//p/text()').getall()

        texto_completo = " ".join(texto).strip()

        yield {
            "titulo": titulo,
            "data": data,
            "texto": texto_completo,
            "url": response.url,
        }
```
