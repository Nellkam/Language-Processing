# Templo

A generic template language.

## Installation

Run the following command to install:

```python
pip install templo
```

## Usage

```python
from templo import template

# Generate a render funtion
>>> render = template("foo {{ 2 + 3 }} bar")
>>> render()
'foo 5 bar'

# Generate a render function and pass a dictionary
>>> d = {"name": "Diana"}
>>> render = template("Hello, {{ name or 'World' }}!")
>>> render()
'Hello, World!'
>>> render(d)
'Hello, Diana!'
```

## Developing Templo

To install templo, along with the tools you need to develop and run tests, run the following in your virtualenv:

```bash
$ pip install -e .[dev]
```
