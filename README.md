<br><br>
<p align="center">
  <img src="https://svgshare.com/i/1CDo.svg" width="500">
  <br>
  Create similar C structs in Python intuitively!
</p>

<p align="center">
  <a href="https://pypi.org/project/structer"><img src="https://img.shields.io/badge/v0.1.0-282C34?style=flat-square&label=Version&labelColor=1D1D1D"></a>
  <a href="https://github.com/d3cryptofc/structer/actions/workflows/ci.yml"><img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/d3cryptofc/structer/ci.yml?style=flat-square&labelColor=1D1D1D&label=Python 3.12&logo=python&logoColor=white"></a>
  <a href="https://github.com/d3cryptofc/structer/LICENSE"><img src="https://img.shields.io/badge/MIT-282C34?style=flat-square&label=License&labelColor=1D1D1D"></a>
</p>

### 📌 Summary

- [Installation](#%EF%B8%8F-installation)
- [Getting Started](#%EF%B8%8F-getting-started)
  - [Creating your first struct model](#1-creating-your-first-struct-model)
  - [Instance generation and data storage](#2-instance-generation-and-data-storage)
  - [Representation and size](#3-representation-and-size)
  - [Getting the serialized data](#4-getting-the-serialized-data)
- [Frequently Asked Questions (FAQ)](#-frequently-asked-questions-faq)
  - [What are structs?](#1-what-are-structs)
  - [Why use structs in Python?](#2-why-use-structs-in-python)

### 🛠️ Installation

Installation from PyPI:
```
pip3 install structer
```

Installation from GitHub:
```
pip3 install git+https://github.com/d3cryptofc/structer.git
```

### 🏃‍♀️ Getting Started

I assure you it's easier than it looks.

#### 1. Creating your first struct model

Create your struct model using `structer.structfy(name, fields)`:

```python3
from structer import structfy, Char, Str, Field

Person = structfy('Person', [
  Field('name', Str(15)),
  Field('gender', Char())
])
```

Notes:

- `structer.Str` is a short nickname for `structer.String`.
- `structer.Char` is like `structer.String(1)`, but **specialized** for this.

#### 2. Instance generation and data storage

You can create an instance by passing the values ​​as an argument:

```python
>>> p = Person(name='John', gender='M')
>>> p
Person(name(15)='John', gender(1)='M') -> 16
```

Or, perhaps you want to make the modifications individually with the already created instance:

```python
>>> p = Person()
>>> p
Person(name(15)='', gender(1)='') -> 16
>>> p.name = 'John'
>>> p.gender = 'M'
>>> p
Person(name(15)='John', gender(1)='M') -> 16
```

#### 3. Representation and size

You may have noticed that the object representation shows the size of each field and the total size of all fields.

To find out the total size of your instance, use the `len` function:

```python
>>> len(p)
16
```

Maybe you want to know the total size of the struct model without having to create an instance, access the `__struct_size__` attribute (size given in bytes):

```python
>>> Person.__struct_size__
16
```

#### 4. Getting the serialized data

Just access the `__struct_binary__` attribute:

```python
>>> p.__struct_binary__
b'John\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00M'
```

Ready! Now you do whatever you want with it.

### 💬 Frequently Asked Questions (FAQ)
#### 1. What are structs?

If you've never programmed in C, you might initially think that a struct is similar to a [dataclass](https://docs.python.org/3/library/dataclasses.html), but unlike a dataclass, structs map fields in memory, so that you have all the data glued together but delimited by their sizes.

You can imagine that internally the mapping is done like:

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

But a struct abstracts this, so that usage is stupidly simple:

```python3
person.first_name = 'John'
person.gender = 'M'
person.age = 23
```

It's important to say that the first example is very crude, structs use bytes instead of strings, allowing you to save an absurd amount of space.

For example, in `age` of the example above, `'23'` was inserted as a string, which consumes 2 bytes in memory, but we could represent numbers from 0 to 255 (00 to FF) using a single byte.

Or better yet, imagine that you want to store the number `18,000,000,000,000,000,000` (18 quintillion) in memory, however storing it in a text file as a string would consume 20 bytes, whereas 8 bytes would be enough to represent the number.

The waste of these 12 bytes would represent twice the number itself, so much so that on a large scale this would throw a huge amount of storage space into the trash, around 60% of the space could be saved, that would be going from 1 TB to just 400G.

#### 2. Why use structs in Python?

Structs are like models for mapping memory space and organizing data, and, unlike C (because it is compiled), in Python each instance that is created will consume space in RAM, just like any other Python class instance.

The point is not to use structs thinking that it will be a lighter alternative to a dataclass as much as a real struct (I don't perform miracles), the point is precisely in the memory mapping made by the struct, it will organize all the data in binary, and from there how you defined it to be organized, so that you can access it whenever you want, whether for:

1. Saving file space.
2. Bandwidth savings in data transmission.
3. Deserialize data from real structs of a network protocol.
4. Creation of binary layouts in general, even from a PNG file.

Or for any other case where it is also useful.