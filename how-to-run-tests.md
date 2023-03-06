How do I run ALL tests?

run: `python3 -m unittest discover tests`

What does this command do?
The __init__.py file in the 'tests' directory denotes it as a package
using the 'unittest' cli we discover all the tests within the 'tests' directory
For a tests to be discovered it must start with 'test' e.g match the pattern test*.py 


How do I run a single test module (note* module = python file)?

run: `python3 tests/testModuleName.py` 