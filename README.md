# dynamic_databases
Django App that allows for the addition of databases on the fly and also the ability to query those database's tables through dynamically generated models.

Currently working:

- Create database model instances in running system.
- Inject them into the known connections as needed.
- Inspect to get any model class for a table of the dynamic database.

To Do:

- Create `content_type` instances for each new model type.

Usage:

- Create instances of the `Database` model.
- The `config` field of the `Database` model should be a json blob that resembles what you add to the `DATABASES` setting in `settings.py`.
- The `name` field is the key in the `DATABASES` struture in `settings.py`
- Once you have an instance of `Database`, call it's `get_model` method with a name of a table from the database. It will return a Model class for you to work with.

It's a work in progress. Feel free to open an issue or submit a pull request.
Use at your own risk.
