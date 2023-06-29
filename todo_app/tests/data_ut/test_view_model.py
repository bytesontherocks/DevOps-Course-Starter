
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

def test_view_model_to_do_property():
    items_to_test = []
    items_to_test.append(Item(1, "testing1", "Done"))
    items_to_test.append(Item(100, "Dibi", "To Do"))
    items_to_test.append(Item(96, "testing2", "Done"))
    items_to_test.append(Item(101, "Daba", "To Do"))
    items_to_test.append(Item(101, "Dudu", "To Do"))
    vm = ViewModel(items_to_test)
    to_do_its = vm.to_do_items

    assert(len(to_do_its) == 3)
    assert(to_do_its[0] == items_to_test[2])
    assert(to_do_its[1] == items_to_test[3])
    assert(to_do_its[2] == items_to_test[4])

def test_view_model_doing_property():
    items_to_test = []
    items_to_test.append(Item(1, "testing1", "Done"))
    items_to_test.append(Item(100, "Dibi", "Doing"))
    items_to_test.append(Item(101, "Daba", "Done"))
    items_to_test.append(Item(1012, "Daba2", "Done"))
    items_to_test.append(Item(1013, "Daba3", "Done"))
    items_to_test.append(Item(1014, "Daba4", "Doing"))
    
    vm = ViewModel(items_to_test)
    doing_its = vm.doing_items

    assert(len(doing_its) == 2)
    assert(doing_its[0] == items_to_test[1])
    assert(doing_its[1] == items_to_test[5])

