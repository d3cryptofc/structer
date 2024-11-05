<br><br>
<p align="center">
  <img src="https://svgshare.com/i/1CDo.svg" width="500">
  <br>
  Create similar C structs in Python intuitively!
</p>

<p align="center">
  <a href="https://pypi.org/project/structer"><img src="https://img.shields.io/badge/v0.1.0-282C34?style=flat-square&label=Version&labelColor=1D1D1D"></a>
  <a href="https://github.com/d3cryptofc/structer/LICENSE"><img src="https://img.shields.io/badge/MIT-282C34?style=flat-square&label=License&labelColor=1D1D1D"></a>
</p>

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
