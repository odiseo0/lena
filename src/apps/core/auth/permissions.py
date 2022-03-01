from pydantic import BaseModel


class Permission(BaseModel):
    """Define a list of a base Permission model"""
    __slots__ = "create", "read", "update", "delete"

    create: bool
    read: bool
    update: bool
    delete: bool
