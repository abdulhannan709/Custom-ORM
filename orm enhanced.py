class Field:
    """Base descriptor class for model fields"""
    def __init__(self, default=None):
        self.name = None
        self.default = default
        
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)
    
    def __set__(self, instance, value):
        if self.validate(instance, value):
            instance.__dict__[self.name] = value
            
    def validate(self, instance, value):
        return True

class StringField(Field):
    """Field type for string values"""
    def validate(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string, got {type(value).__name__}")
        return True

class IntegerField(Field):
    """Field type for integer values"""
    def validate(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer, got {type(value).__name__}")
        return True

class Manager:
    """Manages database operations for a model class"""
    def __init__(self, model_cls):
        self.model_cls = model_cls
        self.database = []  # Simple in-memory database
    
    def all(self):
        """Return all records"""
        return self.database
    
    def count(self):
        """Return count of records"""
        return len(self.database)
    
    def save(self, model):
        """Save a model instance"""
        if not isinstance(model, self.model_cls):
            raise TypeError(f"Can only save {self.model_cls.__name__} instances")
        if not hasattr(model, 'id'):
            model.id = self.count() + 1
        self.database.append(model)
        return model
    
    def filter(self, **kwargs):
        """Filter records based on field values"""
        results = []
        for record in self.database:
            matches = True
            for key, value in kwargs.items():
                if getattr(record, key) != value:
                    matches = False
                    break
            if matches:
                results.append(record)
        return results

class Meta(type):
    """Metaclass for model classes"""
    def __new__(cls, name, bases, attrs):
        if not bases:  # Skip base Model class
            return super().__new__(cls, name, bases, attrs)
        
        # Create new class
        new_attrs = attrs.copy()
        fields = {
            name: value for name, value in attrs.items() 
            if isinstance(value, Field)
        }
        new_attrs['_fields'] = fields
        new_attrs['objects'] = Manager(None)  # Will be set properly after class creation
        
        new_class = super().__new__(cls, name, bases, new_attrs)
        new_class.objects.model_cls = new_class  # Set correct model class reference
        
        return new_class

class Model(metaclass=Meta):
    """Base model class"""
    def __init__(self, **kwargs):
        self.id = None
        # Set default values for all fields
        for name, field in self._fields.items():
            setattr(self, name, kwargs.get(name, field.default))
    
    def save(self):
        """Save the current instance"""
        return self.__class__.objects.save(self)
    
    def __str__(self):
        if self.id is None:
            return f'Unsaved {self.__class__.__name__}'
        return f"{self.__class__.__name__} ({self.id})"
    
    def __repr__(self):
        fields_str = ', '.join(f"{name}={getattr(self, name)!r}" 
                             for name in self._fields)
        return f"{self.__class__.__name__}({fields_str})"

# Example model classes
class Person(Model):
    name = StringField()
    age = IntegerField()

class Car(Model):
    name = StringField()
    model = IntegerField()

# Example usage
if __name__ == "__main__":
    # Create and save a person
    john_doe = Person(name='John Doe', age=30)
    assert Person.objects.count() == 0
    john_doe.save()
    assert Person.objects.count() == 1
    
    # Print all people
    for person in Person.objects.all():
        print(f'{person.name} is {person.age} years old.')
    
    # This will raise a TypeError
    try:
        car = Car(name=1, model='Honda')  # Invalid types
        car.save()
    except TypeError as e:
        print(f"Error: {e}")