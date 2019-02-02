def version(version):
    def set_version(func):
        func._version = version
        return func

    return set_version
