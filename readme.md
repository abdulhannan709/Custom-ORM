# Simple Python ORM

A basic Object-Relational Mapping (ORM) implementation in Python. It allows you to work with Python objects instead of writing database code directly.

## What it does

- Creates database-like objects in Python
- Validates data types (strings, integers)
- Stores data in memory
- Lets you save and retrieve objects

## Basic Usage

```python
from orm import Model, StringField, IntegerField

# Define what data looks like
class Person(Model):
    name = StringField()
    age = IntegerField()

# Create and save data
john = Person(name='John Doe', age=30)
john.save()

# Get all saved people
for person in Person.objects.all():
    print(f'{person.name} is {person.age} years old.')
```

## Features

- Type checking (stops you from putting wrong data types)
- Simple saving and loading
- Keeps track of how many objects you've created
- Basic filtering to find specific objects

That's it! This is a learning project to show how ORMs work in a simple way.