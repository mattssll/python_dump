Chapter 02: Pythonic Code
=========================

Test the code::

   make test


Indexes are same as slice objects
lists, tuples, and strings are examples of sequences and iterators
Sequences implement the __getitem__ and the __len__ method, ranges are examples of sequences, list data structure
Iterators implement the __iter__ and the __next__ method, the __iter__ method can return a generator object to avoid iterators only being able to be used once
When yielding a generator in the __iter__ method, the __next__ is not necessary
Context Managers implement the __enter__ and the __exit__ methods
List comprehensions, set comprehensions, and dictionary comprehensions
Expressions use the walrus operator (:=) to assign and return a value in the same expression
@property (_attribute), @prop.setter, "__" changes method name to _ClassName__method_name (not rly private)
@dataclasses: dataclass, field, InitVar, replace, asdict, astuple, make_dataclass
Container objects and __contains__ method is a boolean evaluator - it allows the "in" operator that internally does "container.__contains__(item)"
__getattribute__ method is used to get an attribute (myobject.attribute), for dynamic attributes __getattr__ is called when an attribute is not found, we add exception not to let adding non existing attrib (dynamic) to our object/class
__call__ method is used to call an object as a function (myobject() executes __call__ code in myobject class)
__new__ method is used to create an object (myobject = MyClass() executes __new__ code in MyClass class)
to extend builtin types we use the collections module

For async programming the idea is that our code is called by an event loop with schedules the coroutines in the same thread
async is a single threaded programming model, mulitple coroutines can run in sequence being intercalated by the event loop and the i/o operations
with the "await" keyword we can let the event loop know that this coroutine is waiting for something, so another coroutine can continue,
when the awaited operation is done the event loop will get back to the coroutine that was waiting again
point of async is NOT TO block on I/O operations - asyncio is a library that provides an event loop and coroutines