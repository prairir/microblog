# Welcome to Microblog!

This is an example application featured in my [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). See the tutorial for instructions on how to work with it.

# Running the docker instance

1. ```docker build -t microblog:latest .```

2. ```docker run --name microblog -d -p 5000:5000 --rm microblog:latest```

# Calculate line coverage

Run ```coverage run -m unittest discover -s ./tests/unit```

After generating the report with the above command then run...

```coverage report``` or ```coverage html```

# How to run behave tutorial

*NOTE* behave steps in the .feature file MUST unicode match those in the 'steps' file

e.g. in the *.feature file there is a Gherkin line like
'the task 'Buy groceries' with estimate '2' should be added to the todo list'

then in the accompanying *step.py file it must follow the exact unicode in the behave decorator
Like this -> '@then("the task '{title}' with estimate '{estimate}' should be added to the todo list")'


Also step files must follow the regex *step.py

1. Running all behave features

run  ```behave tests/features/add-task.feature```

Some examples:
``` behave tests/features/archive-post.feature ```
``` behave tests/features/delete-post.feature ```
``` behave tests/features/enable-2fa.feature ```
``` behave tests/features/enable-editing-post.feature ```

# How to run unit tests

unit tests must follow the "test*.py" regex to be picked up

1. Individual tests

run ```python ./tests/unit/test_example.py ```

2. Run all unit tests

run ``` python -m unittest discover -s ./tests/unit ```

# How to run SonarQube

### Make sure that sonar cube scanner is installed

Run ``` docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest ```

Go to localhost:9000 and login with admin/admin on the spun up SonarQube webapp

### Then run the scanner to create the report

Windows
Run ``` sonar-scanner.bat -D"sonar.projectKey=Microblog" -D"sonar.sources=." -D"sonar.host.url=http://localhost:9000" -D"sonar.token=sqp_4a8f52f75c3f744c5080ec85f786e5927cef3c8e" ```

Linux Run ```sonar-scanner \
  -Dsonar.projectKey=Microblog \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000/ \
  -Dsonar.token=sqp_4a8f52f75c3f744c5080ec85f786e5927cef3c8e ```