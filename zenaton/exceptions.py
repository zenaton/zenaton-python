"""Zenaton base error class"""
class Error(Exception):
    pass


"""Exception raised when communication with workers failed"""
class InternalError(Exception):
    pass


"""Exception raise when clien code is invalid"""
class ExternalError(Exception):
    pass


"""Exception raised when wrong argument type is provided"""
class InvalidArgumentError(ExternalError):
    pass


"""Exception raised when the workflow is unknown"""
class UnknownWorkflowError(ExternalError):
    pass
