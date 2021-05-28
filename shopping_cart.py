from errors import ItemAlreadyExistsError, ItemNotExistError
from item import Item


class ShoppingCart:
    """
    A class used to represent a shopping cart

    Attributes
    -----------
    items : list
        all the items that in the shopping cart

    Methods
    -------
    add_item(item : Item)
        add the given item to the shopping cart

    remove_item(item_name : str)
        remove the item with the given name from the shopping cart

    get_subtotal()
        return the subtotal price of all the items in the shopping cart
    """

    def __init__(self):
        """initialize new list of items - empty shopping cart
        """
        self.items = []

    def __len__(self):
        """Return the length of the list - number of items

        Returns
        --------
        int
            length of the list - items
        """
        return len(self.items)

    def __iter__(self):
        """Return the next item in the list

        Returns
        --------
        Item
        """
        return iter(self.items)

    def add_item(self, item: Item):
        """Add the given item to the shopping cart

        Parameter
        ----------
         item : Item
            the item to add to the shopping cart

        Raises
        ----------
         ItemAlreadyExistError -
            if item already exists in the shopping cart
        """
        if item in self.items:
            raise ItemAlreadyExistsError

        self.items.append(item)

    def remove_item(self, item_name: str):
        """Remove the item with the given name from the shopping cart

        Parameter
        ----------
        item_name : str
            name of the item to remove from the shopping cart

        Raises
        ----------
         ItemNotExistError -
            if no item with the given name exists
        """
        for item in self.items:
            if item_name in item.name:
                self.items.remove(item)
                return

        raise ItemNotExistError

    def get_subtotal(self) -> int:
        """ Return the subtotal price of all the items currently in the shopping cart

        Returns
        --------
        int
            the price of all the items currently in the shopping cart
        """
        sub_total = [item.price for item in self.items]
        return sum(sub_total)

