from database.db import Database
from core.utils import dict_factory


def test_init_db(db: Database = None) -> tuple:
    """
    Tests that the database is initialized correctly.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db") if db is None else db

    if db.database_path != "database/store_records.db":
        error = f"Error in test_init_db: Database path is not correct.\n  - Actual: {db.database_path}"
        return False, error
    else:
        return True, "Database path is correct."


def test_get_inventory_exists(db: Database = None) -> tuple:
    """
    Tests that the inventory is not empty.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db") if db is None else db
    full_inventory = db.get_full_inventory()

    if len(full_inventory) == 0:
        error = f"Error in test_get_full_inventory: Full inventory is empty.\n  - Actual: {len(full_inventory)}"
        return False, error
    else:
        return True, "Full inventory is not empty."


def test_dict_factory_link(db: Database = None) -> tuple:
    """
    Tests that the row factory is linked to dict_factory.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string,
    """
    db = Database("database/store_records.db") if db is None else db
    row_factory = db.connection.row_factory

    if row_factory != dict_factory:
        error = f"Error in test_dict_factory_link: Row factory is not linked to dict_factory.\n  - Expected: {dict_factory}\n  - Actual: {row_factory}"
        return False, error
    else:
        return True, "Row factory is linked to dict_factory."


def test_check_connection_threaded(db: Database = None) -> tuple:
    """
    Tests that the database connection is not single threaded.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string,
    """

    db = Database("database/store_records.db") if db is None else db
    connection_is_threaded = db.connection.isolation_level is None

    if connection_is_threaded:
        error = f"Error in test_check_connection_single_thread: Connection is single threaded.\n  - Actual: {connection_is_threaded}"
        return False, error
    else:
        return True, "Connection is not single threaded."

def test_strawberry_covered_chocolate_info(db: Database = None) -> tuple:
    """
    Tests that database description matches expected.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db") if db is None else db
    full_inventory = db.get_full_inventory()
    actual =[info for info in full_inventory if info['item_name']=='Strawberry Covered Chocolate'][0]
    expected = 'Six layer of  chocolate cake filled with ganache then iced in strawberry buttercream. Garnished with ganache, chocolate dipped strawberries, fudge icing, chocolate pieces, and macarons.'
    if actual != expected:
        error = f"Error in test_strawberry_covered_chocolate_info: description does not match expected value.\n  - Actual: {actual}"
        return False, error
    else:
        return True, "Descriptions match."
    
def test_cookies_and_cream_info(db: Database = None) -> tuple:
    """
    Tests that database description matches expected.

    args:
        - db: an sqlite3 database object (optional)

    returns:
        - error_report: a tuple containing a boolean and a string, 
          where the boolean is True if the test passed and False if it failed, 
          and the string is the error report.
    """

    db = Database("database/store_records.db") if db is None else db
    full_inventory = db.get_full_inventory()
    actual =[info for info in full_inventory if info['item_name']=='Cookies & Cream'][0]
    expected = 'Three layers of chocolate and three layers of vanilla cake filled with cookies and cream mousse and iced with alternating stripes of mousse and buttercream. Coated with chocolate ganache and then garnished with sandwich cookies, chocolate bars, and chocolate pieces.'
    if actual != expected:
        error = f"Error in test_cookies_and_cream_info: description does not match expected value.\n  - Actual: {actual}"
        return False, error
    else:
        return True, "Descriptions match."