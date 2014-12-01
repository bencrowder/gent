## Gent

A simple genealogy todo item app.

### Installation

These installation instructions assume some basic knowledge of Django.

- Clone the repo
- Create a virtualenv for the project if you want
- Copy `settings_sample.py` to `settings.py` and edit to taste (and make sure you put something in `SECRET_KEY`)
- `pip install -r requirements.txt`
- `./manage.py migrate`
- `./manage.py createsuperuser`
- `./manage.py runserver 8001`

### Usage

Items are attached to families, which have a husband and/or a wife.

To add a new item/family:

- Click the "Add Item" button at the top of the screen (or hit `Ctrl+Return`)
- Type in the todo item in the box at the top of the dialog
- In the Family field, type the husband's name followed by a slash followed by the wife's name (and you can leave the husband's or wife's name blank)
	- For example, "Gregorio Sanchez / Isabella Gutierrez"
	- If you've already added families, they'll show up in an autosuggest box
- Click Add Item
- On the detail page for the new item, you can click on the family link and then edit the family to add Family Tree ID numbers
- To complete an item, click its box on the detail page
- To uncomplete an item, click its box again on the detail page

On the family page, items can be rearranged (drag and drop).

To see everything in the system, search for `*`.


### Keyboard shortcuts

- `Ctrl+Return` to open Add Item dialog
- `Shift+Return` to save changes on a dialog
- `/` to focus on the search box
- `h` to return to the home page


