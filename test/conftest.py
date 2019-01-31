from pytest_timekeeper import Writer, set_writer

pytest_plugins = ["pytester"]


class PrintWriter(Writer):
    def finalize(self, timers):
        for t in timers:
            print(t)


printer = PrintWriter()
set_writer(printer)
