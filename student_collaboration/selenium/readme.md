# Selenium Tests

We use Selenium in our project in order to test the different views related to our module (student collaborative tool)

## Installation

The current implementation consider that you have *Chrome* Web browser installed on the computer, and tour computer is either *Windows* (64-bit) or *Linux*.

Don't forget to install the selenium package which is in the `requirements-oscar2.txt` (or add it via *pip* directy `pip install selenium`)

### If it is not the case

You will have to add the correct driver by hand on the selenium file. Check on internet how to install on your desired OS and web browser.

You will probably need to add a `<webBrowser>driver` to the `student_collaboration/selenium` path and edit the `__initDriver(self)` function of the `Selenium` class to add your custom driver.

## Uses	 :rocket:

To launch the *Selenium* tests you should first have the website running then you could launch the Selenium tests.

You will probably first have to move your current directory to the selenium directory

```sh
cd student_collaboration/selenium
```

Then simply launch (via the virtual environment) the main file

```sh
python selen.py
```

### Uses errors

If you encounter some errors like `selen not exists`, `can't import selen` or `webDriver Error` . It's likely that you forgot a step in the installation.

In an error is persisting and you can't find the solution online, don't hesitate to contact us (see [Contacts](#contacts) section below)


### Parametrization

In order to ease it uses, all constant parameters used are in the head of the file, just under the different imports, feel free to change them to suit to your implementation.



### Tests

We cover some tests, but you can modify that focusing tests that looks more important to you, for that you go into the `testAll(self)` method of the `Selenium` class and (un)comment what you want/need, the function names that are tested are explicit, you can still check their documentation if you'r not sure



## Assumptions

In the current implementation we assume that :

- The teacher already exists (and its credentials are given in the initialization parameters)
- The structure of the main code layout have not been changed since (as we use *xPath* that are sensible of the website body hierarchy). Test will fails if it is not the case causing some unknown behaviors afterward



## Contacts

For more information or question ask to the person in charge of the tests:

- Marco
- Loan <loan.sens@student.uclouvain.be>