class NoWarpsException(Exception):
    """
    Exception for empty warp list
    """

    def __init__(self, message):
        super().__init__(message)