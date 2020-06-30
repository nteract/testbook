---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Usage

The motivation behind creating testbook was to be able to write conventional unit tests for Jupyter Notebooks.

## How it works

Testbook achieves conventional unit tests to be written by setting up references to variables/functions/classes in the Jupyter Notebook. All interactions with these reference objects are internally "pushed down" into the kernel, which is where it gets executed.

## Set up Jupyter Notebook under test

### Decorator and context manager pattern

These patterns are interchangeable in most cases. If there are nested decorators on your unit test function, consider using the context manager pattern instead.

- Decorator pattern

  ```{code-block} python

   from testbook import testbook

   @testbook.testbook('/path/to/notebook.ipynb', execute=True)
   def test_func(tb):
       func = tb.ref("func")

       assert func(1, 2) == 3
  ```

- Context manager pattern

  ```{code-block} python

   from testbook import testbook

   def test_func():
       with testbook('/path/to/notebook.ipynb', execute=True) as tb:
           func = tb.ref("func")

           assert func(1, 2) == 3
  ```

### Using `execute` to control which cells are executed before test

You may also choose to execute all or some cells:

- Pass `execute=True` to execute the entire notebook before the test. In this case, it might be better to set up a [module scoped pytest fixture](#share-kernel-context-across-multiple-tests).

- Pass `execute=['cell1', 'cell2']` or `execute='cell1'` to only execute the specified cell(s) before the test.

## Obtain references to objects present in notebook

### Testing functions in Jupyter Notebook

Consider the following code cell in a Jupyter Notebook:

```{code-cell} ipython3
def foo(name):
    return f"You passed {name}!"

my_list = ['spam', 'eggs']
```

Reference objects to functions can be called with,

- explicit JSON serializable values (like `dict`, `list`, `int`, `float`, `str`, `bool`, etc)
- other reference objects

```{code-block} python
@testbook.testbook('/path/to/notebook.ipynb', execute=True)
def test_foo(tb):
    foo = tb.ref("foo")

    # passing in explicitly
    assert foo(['spam', 'eggs']) == "You passed ['spam', 'eggs']!"

    # passing in reference object as arg
    my_list = tb.ref("my_list")
    assert foo(my_list) == "You passed ['spam', 'eggs']!"
```

### Testing function/class returning a non-serializable value

Consider the following code cell in a Jupyter Notebook:

```{code-cell} ipython3
class Foo:
    def __init__(self):
        self.name = name

    def say_hello(self):
        return f"Hello {self.name}!"
```

When `Foo` is instantiated from the test, the return value will be a reference object which stores a reference to the non-serializable `Foo` object.

```{code-block} python
@testbook.testbook('/path/to/notebook.ipynb', execute=True)
def test_say_hello(tb):
    Foo = tb.ref("Foo")
    bar = Foo("bar")

    assert bar.say_hello() == "Hello bar!"
```

## Share kernel context across multiple tests

If your use case requires you to execute many cells (or all cells) of a Jupyter Notebook, before a test can be executed, then it would make sense to share the kernel context with multiple tests.

It can be done by setting up a [module or package scoped pytest fixture][fixture].

Consider the code cells below,

```{code-cell} ipython3
def foo(a, b):
    return a + b
```

```{code-cell} ipython3
def bar(a):
    return [x*2 for x in a]
```

The unit tests can be written as follows,

```{code-block} python
import pytest
from testbook import testbook


@pytest.fixture(scope='module')
def tb():
    with testbook('/path/to/notebook.ipynb', execute=True) as tb:
        yield tb

def test_foo(tb):
    foo = tb.ref("foo")
    assert foo(1, 2) == 3


def test_bar(tb):
    bar = tb.ref("bar")

    tb.inject("""
        data = [1, 2, 3]
    """)
    data = tb.ref("data")

    assert bar(data) == [2, 4, 6]
```

```{warning}
Note that since the kernel is being shared in case of module scoped fixtures, you might run into weird state issues. Please keep in mind that changes made to an object in one test will reflect in other tests too. This will likely be fixed in future versions of testbook.
```

[fixture]: https://docs.pytest.org/en/stable/fixture.html#scope-sharing-a-fixture-instance-across-tests-in-a-class-module-or-session
