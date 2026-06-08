# FIFA Players Analysis System

**Dupla - Felipe Avencourt Soares & Luiz Henryque de Ramos Correa**

## O problema

Desenvolver um sistema eficiente para consulta e análise de dados de jogadores de FIFA, utilizando estruturas de dados otimizadas para buscas rápidas por nome, tags, posições e ratings. O sistema deve processar três arquivos CSV contendo informações de jogadores, avaliações de usuários e tags, permitindo diversas operações de busca e filtragem.

## A solução

O sistema implementa múltiplas estruturas de dados para otimizar diferentes tipos de consulta:

- **Hash Table** para acesso rápido aos jogadores por ID
- **Radix Tree** para buscas por prefixo de nomes
- **Trie** para consultas por tags e posições
- **Hash Table** para organização das avaliações por usuário

### Funcionalidades

1. **Busca por prefixo de nome** - Encontra jogadores cujo nome começa com um prefixo específico
2. **Top N jogadores por usuário** - Lista os melhores jogadores avaliados por um usuário
3. **Top N jogadores por tag** - Lista os melhores jogadores com determinada tag
4. **Interseção de tags** - Encontra jogadores que possuem todas as tags especificadas
5. **Dream Team** - Seleciona o melhor jogador para cada posição
6. **Dream Team por país** - Seleciona o melhor jogador de cada posição para um país específico

---

## 🖥️ Pré-requisitos

Antes de iniciar o projeto, é necessário ter instalado:

- Python 3.6+
- pip (gerenciador de pacotes Python)

## ⚙️ Instalação das dependências

Instale as bibliotecas necessárias:

```bash
pip install csv prettytable colorama
