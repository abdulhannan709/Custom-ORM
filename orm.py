class Field:
    name=''
    def __init__(self):
        print('init called for field')

    def __set__(self, value):
        self.name=value

class StringField(Field):
    def __init__(self):
        print('init called for Stringfield')

    def __set__(self, value):
        super.__set__(self, value)

    def validate(self, cls, value):
        if not isinstance(value, str):
            raise TypeError()
        else:
            return True

class IntegerField(Field):
    def __init__(self):
        print('init called for IntegerField')

    def __set__(self, value):
        super.__set__(self, value)

    def validate(self, cls, value):
        if not isinstance(value, int):
            raise TypeError()
        else:
            return True

class Manager:
    def __init__(self, model_cls):
        self.model_cls = model_cls
        self.database = [] # Database is just an array
    def all(self):
        return self.database

    def count(self):
        return len(self.database)

    def save(self, model):
        self.database.append(model)


class Meta(type):
    def __new__(cls, name, parents, attributes):
        if parents:
            attributes['objects']=Manager(name)
            print("Creating class ", name, attributes)
            # for item in attributes:
            #     print(item)
            new_class = super().__new__(cls, name, parents, attributes)
            return new_class
        else:
            model_class = super().__new__(cls, name, parents, attributes)
            return model_class


class Model(metaclass=Meta):
    def save(self):
        # print('saved')
        # objects=Manager('')
        # objects.save()
        pass
        

    def __str__(self):
        if self.id is None:
            return 'Unsaved'
        return f"{self.__class__.__name__} ({self.id})"

class Person(Model):
    name = StringField()
    age = IntegerField()

class Car(Model):
    name = StringField()
    model = IntegerField()

# john_doe = Person()
john_doe = Person(name='John Doe', age=100)

person_count = Person.objects.count()
assert person_count == 0

john_doe.save()

person_count = Person.objects.count()
assert person_count == 1

for person in Person.objects.all():
    print(f'{person.name} is {person.age} years old.')

car = Car(name=1, model='Honda')
car.save() # this will give error