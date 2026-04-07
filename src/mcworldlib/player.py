# This file is part of MCWorldLib
# Copyright (C) 2019 Rodrigo Silva (MestreLion) <linux@rodrigosilva.com>
# License: GPLv3 or later, at your choice. See <http://www.gnu.org/licenses/gpl>

"""Player and its Inventory

Exported items:
    Player -- Class representing a player
"""

from pathlib import Path

from . import nbt
from . import util as u
from . import level


__all__ = ["Player"]


class Player(nbt.File):
    __slots__ = ("name", "level")

    def __init__(self, *args, name="Player", level=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.level: "level.Level | None" = level

    @property
    def inventory(self) -> nbt.List[nbt.Compound]:
        return self["Inventory"]

    @inventory.setter
    def inventory(self, value: nbt.List[nbt.Compound]):
        self["Inventory"] = value

    def get_chunk(self):
        """The chunk containing the player location"""
        if not (self.level and self.level.world):
            return None

        return self.level.world.get_chunk_at(
            self["Pos"], u.Dimension.from_nbt(self["Dimension"])
        )

    @classmethod
    def load(cls, path: u.AnyPath, **kwargs):
        with open(path, "rb") as buff:
            player = super().load(buff, gzipped=True, **kwargs)
            player.filename = Path(path).name

        return player

    def save(self, filename=None, *, gzipped=None, byteorder=None):
        if (
            not filename
            and self.level
            and self.level.world
            and self.level.world.path
            and self.filename
        ):
            filename = Path(self.level.world.path) / "playerdata" / self.filename
        return super().save(filename, gzipped=gzipped, byteorder=byteorder)
