from adresbook import contacts, add_contact, search_by_name, delete_contact

def test_add_contact(): 
    # Test adding a contact
    add_contact('John Doe', '06876543210', 'john@example.com')
    # Let's check if the function works correctly
    assert len(contacts) == 1
    assert contacts[0]['name'] == "John Doe"
	
def test_search_contact():
    # Test searching contacts
    add_contact('Haonan Wu', '06876543290', 'Haonan@example.com')
    search_results = search_by_name("John")

    assert len(search_results) == 1
    assert search_results[0]['name'] == "John Doe"
    # todo: Implement a test here.
        
def test_delete_contact():
    # Test deleting a contact
    add_contact('john Doe', '06876543210', 'john@example.com')
    assert len(contacts) == 1

    delete_contact("John Doe")
    assert len(contacts) == 0
    # todo: Implement a test here.


def main():
    test_add_contact()
    test_search_contact()
    test_delete_contact()

if __name__ == "__main__":
    main()
