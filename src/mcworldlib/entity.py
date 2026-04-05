# This file is part of MCWorldLib
# Copyright (C) 2019 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""Entities and associated classes

Exported items:
    Entity -- Class representing an Entity with ID, ultimately inherits from nbt.Compound
"""

from typing import Any, Self

from . import nbt
from . import util as u

__all__: list[str] = [
    "Entity",
]


_NAMESPACE: str = "minecraft"


# TODO: create an nbt.Schema for it
class BaseEntity(nbt.Compound):
    """Base class for all entities"""

    __slots__ = ()


class Entity(BaseEntity):
    """Base for all Entities with id"""

    __slots__ = ()
    entity_id: str = ""

    @property
    def name(self) -> str:
        return self._name_from_id()

    @property
    def pos(self) -> u.Pos:
        return u.Pos.from_tag(self)

    @classmethod
    def subclass(cls, tag: Any) -> Self:
        """Return an instance of the appropriate Entity subclass based on entity ID"""
        return _ENTITY_SUBCLASSES_IDS_MAPPING.setdefault(tag["id"], cls)(tag)

    def _name_from_id(self, eid: str | None = None) -> str:
        return (eid or self["id"]).split(":", 1)[-1].replace("_", " ").title()

    def __str__(self) -> str:
        return f"{self.name} at {self.pos}"


class ItemEntity(Entity):
    __slots__ = ()
    entity_id: str = "item"

    @property
    def name(self) -> str:
        ename = super().name
        iname = self._name_from_id(self["Item"]["id"])
        count = int(self["Item"]["Count"])
        return f"{ename}: {count} {iname}"


_ENTITY_SUBCLASSES_IDS_MAPPING: dict[str, type[Entity]] = {
    (_.entity_id if ":" in _.entity_id else f"{_NAMESPACE}:{_.entity_id}"): _
    for _ in Entity.__subclasses__()
    if _.entity_id is not None
}
