# Opmerking: De aanpak die hier wordt laten zien, is een eenvoudige introductie in unit testen. 
# Later zal je meer diepgaande technieken leren met behulp van de ingebouwde frameworks en libraries van Python

contacts = []

def add_contact(name, phone_number, email):
    contact = {
        'name': name,
        'phone_number': phone_number,
        'email': email
    }
    contacts.append(contact)

def search_by_name(name):
    return list(filter(lambda c: name.lower() in c['name'].lower(), contacts))

def delete_contact(name):
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            contacts.remove(contact)
            # break # Na het vinden en verwijderen verlaat u de lus