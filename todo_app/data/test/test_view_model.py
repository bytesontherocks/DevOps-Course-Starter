
from  todo_app.data.Item import Item
from  todo_app.data.ViewModel import ViewModel

def test_view_model_done_property():
    items_to_test = []
    items_to_test.append(Item(1, "testing1", "Done"))
    items_to_test.append(Item(100, "Dibi", "To Do"))
    items_to_test.append(Item(101, "Daba", "Done"))
    vm = ViewModel(items_to_test)
    done_its = vm.done_items

    assert(len(done_its) == 2)
    assert(done_its[0] == items_to_test[0])
    assert(done_its[1] == items_to_test[2])
    

