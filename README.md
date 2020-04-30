# PyLadies Snake 🐍 #

## Description ##

[_Snake_](wikipedia_snake) is a notoriously known game. It is also one of the homework
[projects](pyladies_snake) in the PyLadies [course](pyladies_ostrava) in Ostrava.

This repository is my try on programming this game. Its purpose is not to make it fast,
effective or in an easy way, but to exercise my brain a bit on how to do it elegantly or
to leverage some interesting concepts.

## How to run ##

### Requirements ###

* Python 3.7 – `brew install python`
* Pipenv – `pip install pipenv`

### Running ###

* `pipenv install`
* **`pipenv run snake.py`**

🐍

### Testing ###

There are no tests. (Yet?) Shame on me!

## Code style ##

- No global or outer variable references. Only function arguments (immediate or closure)
  can be referenced. For the sake of readability it’s ok to reference a _fact_
  represented by an immutable global/class constant.

## License ##

[MIT License](LICENSE.md)

[wikipedia_snake]: https://en.wikipedia.org/wiki/Snake_(video_game_genre
[pyladies_snake]: https://naucse.python.cz/2019/pyladies-ostrava-jaro/projects/snake/
[pyladies_ostrava]: https://naucse.python.cz/2019/pyladies-ostrava-jaro/
