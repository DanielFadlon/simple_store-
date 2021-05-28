import yaml

from collections import Counter
from errors import ItemNotExistError, TooManyMatchesError
from item import Item
from shopping_cart import ShoppingCart


class Store:
    """
    A class used to represent a Store.

    Attributes
    ----------
    _items : list
        the items in the store.
    _shopping_cart : ShoppingCart
        the shopping cart of customer in the store.

    Methods
    --------
    get_items()
        return all the items in the store.

    search_by_name(item_name : str)
        find and return all the items of which the given name is a part of their name.

    search_by_hashtag(hashtag : str)
        find and return all the items that have the given hashtag.

    add_item(item_name)
        add the item that the given name is sub-name of the his name to the customer shopping cart.

    remove_item(item_name)
        remove the item that the given name is sub-name of his name from the customer shopping cart.

    checkout()
        return the total price of all the items in the customer's shopping cart.
     """

    def __init__(self, path):
        """ Initialize new Store by details from the given file

        Parameter
        ----------
        path : str
            the path of the file that consist store items and details

        """
        with open(path) as inventory:
            items_raw = yaml.load(inventory, Loader=yaml.FullLoader)['items']
        self._items = self._convert_to_item_objects(items_raw)
        self._shopping_cart = ShoppingCart()

    @staticmethod
    def _convert_to_item_objects(items_raw):
        """--static method--
        Convert the information from the given list of dictionaries to list of Items

        Parameter
        -----------
        items_raw : list
            A list of dictionaries - each dictionary represent an item
            which means for each dictionary there are the keys -
                    name:str , price: int, hashtags: list, description: str.
        """
        return [Item(item['name'],
                     int(item['price']),
                     item['hashtags'],
                     item['description'])
                for item in items_raw]

    def get_items(self) -> list:
        """Return list of all the items in the store

        Returns
        -------
        list
            list of the items in the store
        """
        return self._items

    def search_by_name(self, item_name: str) -> list:
        """Find a list of items that the given name appear in their name.
            Search in items that not in the shopping cart.

            list order - according to the common of hashtags in the shopping cart
                or by lexicographic order if there is 2 items with the same rate.

        Parameter
         ---------
         item_name: str
                the name to be searched. name or sub-name of item's name.

        Returns
        ---------
        list
            order list with all the items that the given name appear in their name.
        """
        my_items = []
        for item in self._items:
            if item_name in item.name and item not in self._shopping_cart:
                my_items.append(item)

        return self.sort_by_rate(my_items)

    def search_by_hashtag(self, hashtag: str) -> list:
        """Find a list of items that have the given hashtag.
            Search in items that not in the shopping cart.

            list order - according to the common of hashtags in the shopping cart
                or by lexicographic order if there is 2 items with the same rate.

        Parameter
         ---------
         hashtag: str
                the hashtag to be searched.

        Returns
        ---------
        list
            order list with all the items that the given hashtag appear in their hashtags list.
        """
        my_hashtags = []
        for item in self._items:
            if hashtag in item.hashtags and item not in self._shopping_cart:
                my_hashtags.append(item)

        return self.sort_by_rate(my_hashtags)

    def add_item(self, item_name: str):
        """Adds the item with the given name to the customer's shopping cart

        Note: to ease the search, not the whole item's name must be given, but rather a distinct substring.

        Parameter
         ----------
         item_name: str
                the name of the item.

        Raises
        -----------
        ItemNotExistError -
            if no such item exists.
        TooManyArgumentsError -
            if there are multiply items matching the given name.
        ItemAlreadyExistError -
            if the item correspond to the given name is already in the shopping cart
        """
        my_items = [item for item in self._items if item_name in item.name]
        if len(my_items) == 0:
            raise ItemNotExistError
        elif len(my_items) > 1:
            raise TooManyMatchesError

        self._shopping_cart.add_item(my_items[0])

    def remove_item(self, item_name: str):
        """Removes the item with the given name from the customer's shopping cart

        Note: to ease the search, not the whole item's name must be given, but rather a distinct substring.

        Parameter
         ----------
         item_name: str
                the name of the item.

        Raises
        -----------
        ItemNotExistError -
            if no such item exists.
        TooManyArgumentsError -
            if there are multiply items matching the given name.
        """
        my_items = [item for item in self._shopping_cart.items if item_name in item.name]
        if len(my_items) > 1:
            raise TooManyMatchesError

        self._shopping_cart.remove_item(item_name)

    def checkout(self) -> int:
        """Return the total price of all the items in the customer's shopping cart.

        Returns
        --------
        int
            total price
        """
        return self._shopping_cart.get_subtotal()

    def compute_rate(self, items_list):
        """ ---helper function--
        For each item in the give list return his rate as a tuple (rate,item).

        rate of one item is compute according to -
            the number of hashtags in the current shopping cart that exists in the item hashtags

        Parameter
        -----------
        item_list: list
                 list to rate.

        Returns
        -----------
        list
            list of tuples - (rate,item)
        """
        rate_list = []
        list_of_hashtags = [hashtag for item in self._shopping_cart.items for hashtag in item.hashtags]
        c = Counter(list_of_hashtags)
        for item in items_list:
            rate_numbers = [c[tag] for tag in item.hashtags if tag in list_of_hashtags]
            rate_list.append((sum(rate_numbers), item))

        return rate_list

    def sort_by_rate(self, items_list: list):
        """---helper function---
        Return sorted list according to the following rules:
            1- rate: number of common hashtags that appear in the shopping cart items.
            2- lexicographic: when rate is equal

        Parameter
        -----------
        items_list: list
                the list of items to sort

        Returns
        ----------
        list
            sorted by rate
        """
        items_list = sorted(items_list, key=lambda item: item.name)
        items_list = sorted(self.compute_rate(items_list), key=lambda tup: tup[0], reverse=True)

        return [tup[1] for tup in items_list]




