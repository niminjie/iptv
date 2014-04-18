class DataSet:
    def __repr__(self):
        s = 'DataSet read from %s\n' % self.__fi_path
        s += 'Rows: %d\n' % len(self.__data)
        if len(self.__data[0]) > 0:
            s += 'Columns: %d' % len(self.__data[0])
        return s

    def __init__(self, path, sep=','):
        self.__fi_path = path
        self.fi = open(self.__fi_path, 'r')
        self.__data = self._loadData(self.fi, sep)

    def _loadData(self, fi, sep=','):
        data = []
        for line in fi:
            arr = line.split(sep)
            # Remove \n in last element
            arr[-1] = arr[-1].strip()
            data.append(tuple(arr))
        return data

    def getData(self):
        return self.__data
