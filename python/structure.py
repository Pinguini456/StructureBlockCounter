from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from pynbt import BaseTag, NBTFile, TAG_Compound, TAG_Int, TAG_List, TAG_String
from typing import Any, BinaryIO, Tuple

BlockStateValue = str | bool | int



def _into_pyobj(tag: BaseTag) -> Any:
    """
    Turns an NBT tree into a python tree.
    """
    if isinstance(tag, (TAG_Compound, dict)):
        res = {}
        for key, value in tag.items():
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res[key] = value
        return res

    if isinstance(tag, (TAG_List, list)):
        res = []
        for value in tag:
            if isinstance(value, BaseTag):
                value = _into_pyobj(value)
            res.append(value)
        return res

    if isinstance(tag, BaseTag):
        return tag.value

    return tag




@dataclass(init=False)
class Block:
    """
    Attributes
    ----------
    name
        The name of the block.

    states
        The states of the block.

    Examples
    --------
    .. code-block::

        Block("minecraft:beehive", honey_level=4)
        Block("minecraft:grass")

    """

    identifier: str
    states: dict[str, BlockStateValue]

    __slots__ = ("identifier", "states")

    def __init__(self, identifier: str, **states: BlockStateValue):
        """
        Parameters
        ----------
        identifier
            The identifier of the block (e.g. "minecraft:wool").

        states
            The block states such as ``color`` or ``stone_type``.
            This varies by every block.

            .. seealso:: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/blockreference/examples/blockstateslist
        """
        self.identifier = identifier
        self.states = states

    def __str__(self) -> str:
        return self.stringify()

    def stringify(
        self,
        *,
        with_namespace: bool = True,
        with_states: bool = True,
    ) -> str:
        """Returns a human-readable representation of the structure.

        Parameters
        ----------
        with_namespace
            Whether to include the block's namespace.

        with_states
            Whether to include the block's states.
        """
        result = ""
        if with_namespace and (ns := self.namespace) is not None:
            result += ns + ":"
        result += self.name
        if with_states:
            result += " ["
            for key, value in self.states.items():
                result += f'"{key}"='
                if isinstance(value, str):
                    result += f'"{value}"'
                elif isinstance(value, bool):
                    result += str(value).lower()
                elif isinstance(value, int):
                    result += str(value)
                else:
                    raise ValueError("block state value must be str, bool or int")
            result += "]"
        return result

    @property
    def namespace_and_name(self) -> tuple[str | None, str]:
        """The namespace and the name of the block.

        Examples
        --------
        .. code-block:: python

            >>> from mcstructure import Block
            >>>
            >>> block = Block("minecraft:wool", color="red")
            >>> block.namespace_and_name
            ("minecraft", "wool")
            >>>
            >>> block = Block("foobar")
            >>> block.namespace_and_name
            (None, "foobar")

        """
        if ":" in self.identifier:
            ns, name = self.identifier.split(":", 1)
            return ns, name

        return (None, self.identifier)

    @property
    def name(self) -> str:
        """The name of the block.

        Examples
        --------
        .. code-block:: python

                >>> from mcstructure import Block
                >>>
                >>> block = Block("minecraft:wool", color="red")
                >>> block.name
                "wool"
                >>>
                >>> block = Block("foobar")
                >>> block.name
                "foobar"

        """
        return self.namespace_and_name[1]

    @property
    def namespace(self) -> str | None:
        """The namespace of the block.

        Examples
        --------
        .. code-block:: python

                >>> from mcstructure import Block
                >>>
                >>> block = Block("minecraft:wool", color="red")
                >>> block.namespace
                "minecraft"
                >>>
                >>> block = Block("foobar")
                >>> (block.namespace,)
                (None,)

        """
        return self.namespace_and_name[0]



class Structure:
    def __init__(self, size: tuple[int, int, int], fill: Block | None = Block("minecraft:air")) -> None:

        self.structure: NDArray[np.intc]

        self._size = size
        self._palette: list[Block] = []

        if fill is None:
            self.structure = np.full(size, -1, dtype=np.intc)

        else:
            self.structure = np.zeros(size, dtype=np.intc)
            self._palette.append(fill)


    @classmethod
    def load(cls, file: BinaryIO):
        """
        Loads a structure from a file.

        Examples
        --------
        .. code-block:: python

            from mcstructure import Structure

            with open("house.mcstructure", "rb") as f:
                struct = Structure.load(f)

        Parameters
        ----------
        file
            File object to read.
        """
        nbt = NBTFile(file, little_endian=True)
        size: tuple[int, int, int] = tuple(x.value for x in nbt["size"])  # type: ignore

        struct = cls(size, None)

        struct.structure = np.array(
            [_into_pyobj(x) for x in nbt["structure"]["block_indices"][0]],
            dtype=np.intc,
        ).reshape(size)

        struct._palette.extend(
            [
                Block(block["name"].value, **_into_pyobj(block["states"].value))
                for block in nbt["structure"]["palette"]["default"]["block_palette"]
            ]
        )

        return struct
    
    def get_structure(self) -> NDArray[Any]:
        """
        Returns the structure as a numpy array filled
        with the corresponding block objects.
        """
        arr = np.full(
            self.structure.shape, Block("minecraft:structure_void"), dtype=object
        )
        for key, block in enumerate(self._palette):
            arr[self.structure == key] = block
        return arr
    
    