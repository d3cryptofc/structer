<br><br>
<p align="center">
  <img src="https://gist.githubusercontent.com/d3cryptofc/b137c0ecee656b142ec5265e2b4ec7bc/raw/3db96a47061d61b9db1d8e5b3e59723e328bf753/structer.svg" width="500">
  <br>
  Crie structs similares de C em python de forma intutiva!
</p>

<p align="center">
  <a href="https://pypi.org/project/structer"><img src="https://img.shields.io/badge/v0.1.1-282C34?style=flat-square&label=Version&labelColor=1D1D1D"></a>
  <a href="https://github.com/d3cryptofc/structer/actions/workflows/ci.yml"><img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/d3cryptofc/structer/ci.yml?style=flat-square&labelColor=1D1D1D&label=Python 3.9 | 3.10 | 3.11 | 3.12&logo=python&logoColor=white"></a>
  <a href="https://github.com/d3cryptofc/structer/LICENSE"><img src="https://img.shields.io/badge/MIT-282C34?style=flat-square&label=License&labelColor=1D1D1D"></a>
</p>
<br>

### 📌 Sumário

- [Instalação](#%EF%B8%8F-instala%C3%A7%C3%A3o)
- [Começando](#%EF%B8%8F-come%C3%A7ando)
  - [Criando seu primeiro modelo de struct](#1-criando-seu-primeiro-modelo-de-struct)
  - [Geração de instância e armazenamento de dados](#2-gera%C3%A7%C3%A3o-de-inst%C3%A2ncia-e-armazenamento-de-dados)
  - [Representação e tamanho](#3-representa%C3%A7%C3%A3o-e-tamanho)
  - [Obtendo os dados serializados](#4-obtendo-os-dados-serializados)
- [Perguntas Frequentes (FAQ)](#-perguntas-frequentes-faq)
  - [O que são structs?](#1-o-que-são-structs)
  - [Por que usar structs em Python?](#2-por-que-usar-structs-em-python)

### 🛠️ Instalação

Instalação via PyPI:
```
pip3 install structer
```

Instalação via GitHub:
```
pip3 install git+https://github.com/d3cryptofc/structer.git
```

### 🏃‍♀️ Começando

Te garanto que é mais fácil do que parece.

#### 1. Criando seu primeiro modelo de struct

Crie seu modelo de struct usando `structer.structfy(name, fields)`:

```python3
from structer import structfy, Char, Str, Field

Person = structfy('Person', [
  Field('name', Str(15)),
  Field('gender', Char())
])
```

Notas:

- `structer.Str` é um apelido curto para `structer.String`.
- `structer.Char` é como `structer.String(1)`, porém **especializado** para isso.

#### 2. Geração de instância e armazenamento de dados

Você pode criar uma instância passando os valores como argumento:

```python
>>> p = Person(name='John', gender='M')
>>> p
Person(name(15)='John', gender(1)='M') -> 16
```

Ou, talvez queira fazer as modificações de forma individual com a instância já criada:

```python
>>> p = Person()
>>> p
Person(name(15)='', gender(1)='') -> 16
>>> p.name = 'John'
>>> p.gender = 'M'
>>> p
Person(name(15)='John', gender(1)='M') -> 16
```

#### 3. Representação e tamanho

Você deve ter notado que a representação do objeto mostra o tamanho de cada campo e o tamanho total de todos os campos.

Para saber o tamanho total de sua instância, use a função `len`:

```python
>>> len(p)
16
```

Talvez queira saber o tamanho total do modelo de struct sem precisar criar uma instância, acesse o atributo `__struct_size__` (tamanho dado em bytes):

```python
>>> Person.__struct_size__
16
```

#### 4. Obtendo os dados serializados

Basta acessar o atributo `__struct_binary__`:

```python
>>> p.__struct_binary__
b'John\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00M'
```

Pronto! Agora você faz o que bem quiser com isso.

### 💬 Perguntas Frequentes (FAQ)

#### 1. O que são structs?

Se você nunca programou em C, pode inicialmente pensar que uma struct é similar a um [dataclass](https://docs.python.org/3/library/dataclasses.html), mas diferente de um dataclass, structs mapeiam os campos na memória, de forma que você tenha todos os dados colados um no outro porém delimitados por seus tamanhos.

Você pode imaginar que internamente o mapeamento é feito como:

```python3
# Your field sizes.
f_first_name = 10
f_gender = 1
f_age = 2

# Memory containing the data.
memory = 'John      M23'

# Accessing data delimited by its field sizes.
memory[0:f_first_name] # 'John      '
memory[f_first_name:f_first_name + f_gender] # 'M'
memory[f_first_name + f_gender:f_first_name + f_gender + f_age] # '23'
```

Porém uma struct abstrai isso, de forma que o uso seja estupidamente simples:

```python3
person.first_name = 'John'
person.gender = 'M'
person.age = 23
```

É importante dizer que o primeiro exemplo é bem grosseiro, structs utilizam bytes ao invés de string, permitindo que você economize um espaço absurdo.

Por exemplo, em `idade` do exemplo acima foi inserido `'23'` como string, o que consome 2 bytes na memória, porém poderiamos representar números de 0 a 255 (00 a FF) usando um único byte.

Ou melhor, imagine que você queira armazenar o número `18,000,000,000,000,000,000` (18 quintilhões) na memória, no entanto armazenar num arquivo de texto como uma string iria consumir 20 bytes, sendo que bastaria 8 bytes para representar o número.

O desperdício desses 12 bytes daria pra representar o próprio número duas vezes, tanto que isso em larga escala jogaria um enorme espaço de armazenamento no lixo, cerca de 60% de espaço poderia ser economizado, isso seria ir de 1TB para somente 400G.

#### 2. Por que usar structs em Python?

Structs são como modelos para mapear o espaço na memória e organizar os dados, e, diferente de C (por ser compilado), em python cada instância que for criada vai consumir espaço na memória RAM, assim como qualquer outra instância de classe do Python.

O ponto não é usar structs pensando que será uma alternativa mais leve que dataclass tanto quanto uma struct de verdade (eu não faço milagres), o ponto está justamente no mapeamento de memória feita pela struct, ela organizará todos os dados em binário, e da forma como você definiu que ela organizasse, para que você possa acessar quando bem quiser, seja para:

1. Economia de espaço em arquivo.
2. Economia de banda na transmissão de dados.
3. Desserializar dados oriundos de structs de verdade de um protocolo de rede.
4. Criação de layouts binários em geral, até mesmo de um arquivo PNG.

Ou para qualquer outro caso onde também seja útil.