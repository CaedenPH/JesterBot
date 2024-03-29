**Joining Iterables**

If you want to display a list (or some other iterable), you can write:
```py
Colours = ['red', 'green', 'blue', 'yellow']
output = ""
separator = ", "
for Colour in Colours:
    output += Colour + separator
print(output)
# Prints 'red, green, blue, yellow, '
```
However, the separator is still added to the last element, and it is relatively slow.

A better solution is to use `str.join`.
```py
Colours = ['red', 'green', 'blue', 'yellow']
separator = ", "
print(separator.join(Colours))
# Prints 'red, green, blue, yellow'
```
An important thing to note is that you can only `str.join` strings. For a list of ints,
you must convert each element to a string before joining.
```py
integers = [1, 3, 6, 10, 15]
print(", ".join(str(e) for e in integers))
# Prints '1, 3, 6, 10, 15'
```
