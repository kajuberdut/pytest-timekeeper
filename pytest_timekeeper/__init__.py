from pytest_timekeeper.writers import Writer, JsonWriter

_writer: Writer = JsonWriter()


def set_writer(writer: Writer):
    global _writer
    _writer = writer


def get_writer():
    return _writer
