''' Module with descriptors '''


class IntegerExeption(Exception):
    ''' Integer Exception '''
    def __init__(self, val):
        self.message = f'{val} is not Integer'
        super().__init__(self.message)


class StringExeption(Exception):
    ''' String Exception '''
    def __init__(self, val):
        self.message = f'{val} is not String'
        super().__init__(self.message)


class PositiveExeption(Exception):
    ''' Positive Exception '''
    def __init__(self, val):
        self.message = f'{val} is not Positive'
        super().__init__(self.message)


class Integer:
    ''' Integer descriptor '''
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype):
        return obj.__dict__.get(self.name)

    def __set__(self, obj, val):
        if isinstance(val, int):
            obj.__dict__[self.name] = val
        else:
            raise IntegerExeption(val)


class String:
    ''' String descriptor '''
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype):
        return obj.__dict__.get(self.name)

    def __set__(self, obj, val):
        if isinstance(val, str):
            obj.__dict__[self.name] = val
        else:
            raise StringExeption(val)


class PositiveInteger:
    ''' Positive Integer descriptor '''
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype):
        return obj.__dict__.get(self.name)

    def __set__(self, obj, val):
        if isinstance(val, int):
            if val > 0:
                obj.__dict__[self.name] = val
            else:
                raise PositiveExeption(val)
        else:
            raise IntegerExeption(val)


class Data:
    ''' Control types with descriptors '''
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price

    def format_answer(self):
        ''' Get format answer '''
        return f'{self.num}, {self.name}, {self.price}'

    def whole_price(self):
        ''' Calculate whole price '''
        return self.num * self.price
