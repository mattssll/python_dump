import contextlib

"""
fd = open(filename)
try:
    process_file(fd)
finally:
    fd.close()

is the same as with the context manager:

with open(filename) as fd:
    process_file(fd)

The open fx implements the context manager protocol and the __enter__ method returns what comes after the 'as' keyword.
"""

run = print


def stop_database():
    run("systemctl stop postgresql.service")


def start_database():
    run("systemctl start postgresql.service")

# Context Managers 1 (CM1) - As a class with magic methods:
class DBHandler:
    def __enter__(self):
        stop_database()
        return self

    def __exit__(self, exc_type, ex_value, ex_traceback):  # all none if no exception
        start_database()


def db_backup():
    run("pg_dump database")


# Context Managers 2 (CM2) - db_handler is a generator fx that yields the context manager object
@contextlib.contextmanager
def db_handler():
    try:
        stop_database()
        yield  # same as return in __enter__, yielded result goes to variable after the "as" keyword
    finally:
        start_database()


# Context Managers 3 (CM3) - We define a decorator that can be used in a method to make it a context manager
class dbhandler_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        stop_database()
        return self

    def __exit__(self, ext_type, ex_value, ex_traceback):  
        start_database()
        # If we return True on exit the exception will be ignored


@dbhandler_decorator()
def offline_backup():
    run("pg_dump database")

# or, if we want the variable from the __enter__ method
def offline_backup():
    with dbhandler_decorator() as handler:
        run("pg_dump database")


# Context Managers 4 (CM4) - using context manager while ignoring certain exceptions we know we can ignore
def parse_data(input_data: dict):
    pass 

with contextlib.suppress(Exception):  # ignoring all exceptions, not good - be specific and use this only if needed
    parse_data({"key": "value"})


def main():
    # Running our CM1
    with DBHandler():
        db_backup()
    # Running our CM2
    with db_handler():
        db_backup()
    # Running our CM3
    offline_backup()
    # and also


if __name__ == "__main__":
    main()
