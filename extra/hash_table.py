class HashLine:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f'{self.key}:{self.value}'


class HashTable:
    def __init__(self):
        self.table = []

    def put(self, key, value):
        if self.contain(key):
            for i in range(len(self.table)):
                if key == self.table[i].value:
                    self.table[i] = HashLine(key, [self.table[i].value, value])
        else:
            self.table.append(HashLine(key, value))

    def contain(self, key):
        for elem in self.table:
            if key == elem.key:
                return True
            else:
                return False

    def get_value(self, key):
        for elem in self.table:
            if key == elem.key:
                return elem.value
        return None

    def __repr__(self):
        return f'{self.table}'


