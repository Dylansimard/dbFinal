

class tableHeaders:

    def __init__(self, headers):
        self.headers = {}

        temp = headers.split("|")
        counter = 0
        for i in temp:
            i = i.strip()
            varName = i.split()[0]
            varName = varName.strip()
            self.headers.update({varName : counter})
            counter += 1
        self.totalEntries = counter


    def headerLookup(self, header):
        for key, val in self.headers.items():
            if key.find(header) != -1:
                return val

            if key == header:
                return val
