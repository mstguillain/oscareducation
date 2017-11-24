# Selenium Tests

We use Selenium in our project in order to test the different views related to our module (student collaborative tool)

## Installation and uses


### Parametrization

In order to ease it uses, all constant parameters used are in the head of the file, just under the different imports, feel free to change them to suit to your implementation.



### Tests

We cover some tests, but you can modify that focusing tests that looks more important to you, for that you go into the `test(self)` method of the `Selenium` class and (un)comment what you want/need, the function names that are tested are explicit, you can still check their documentation if you'r not sure



## Assumptions

In the current implementation we assume that :

- The teacher already exists (and its credentials are given in the initialization parameters)
- The structure of the main code layout have not been changed since (as we use *xPath* that are sensible of the website body hierarchy). Test will fails if it is not the case causing some unknown behaviors afterward



## Contacts

For more information or question ask to the person in charge of the tests:

- Marco
- Loan