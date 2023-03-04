class ViewModel:
    def __init__(self, items):
        self._items = items
 
    @property
    def items(self):
        return self._items
    
    @property
    def done_items(self):
        done_items = []
        for it in self._items:
            if it.status == "Done":
                done_items.append(it)
        return done_items