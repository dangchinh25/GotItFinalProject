from fastscript import *

from main.controllers.category import get_category, get_categories, get_category_items, create_item, create_category
from main.controllers.item import get_item, update_item, delete_item
from main.controllers.user import app, signin, signup, get_current_user
from create_tables import create_tables


@call_parse
def create_tables_script(init_tables: Param("Init tables", bool_arg) = False):
    if init_tables is True:
        create_tables()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
