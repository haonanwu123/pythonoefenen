import os
import sys
import json


def display(addressbook: list):
    """Print all contacts in the specified format."""
    for contact in addressbook:
        print("======================================")
        print(f"Position:  {contact['id']}")
        print(f"First name:  {contact['first_name']}")
        print(f"Last name:  {contact['last_name']}")
        print("Emails: ", ", ".join(contact["emails"]))
        print("Phone numbers: ", ", ".join(contact["phone_numbers"]))
    print("======================================")


def list_contacts(addressbook: list, direction="DESC"):
    """Return list of contacts sorted by first_name or last_name."""
    return sorted(
        addressbook,
        key=lambda x: (x["first_name"], x["last_name"]),
        reverse=(direction.upper() == "DESC"),
    )


def add_contact(
    addressbook: list,
    first_name: str,
    last_name: str,
    emails: list,
    phone_numbers: list,
):
    """Add a new contact."""
    # Generate new ID
    new_id = max(contact["id"] for contact in addressbook) + 1 if addressbook else 1

    new_contact = {
        "id": new_id,
        "first_name": first_name,
        "last_name": last_name,
        "emails": list(set(emails)),  # Unique emails
        "phone_numbers": list(set(phone_numbers)),  # Unique phone numbers
    }
    addressbook.append(new_contact)
    print("Contact added to addressbook")


def remove_contact(addressbook: list, contact_id: int):
    """Remove a contact by ID."""
    # Use a list comprehension to filter the addressbook
    original_length = len(addressbook)
    addressbook[:] = [contact for contact in addressbook if contact["id"] != contact_id]

    if len(addressbook) < original_length:
        print(f"Contact with ID {contact_id} removed.")
    else:
        print(f"No contact found with ID {contact_id}.")


def merge_contacts(addressbook: list):
    """Merge duplicate contacts."""
    merged = {}
    for contact in addressbook:
        full_name = f"{contact['first_name']} {contact['last_name']}"
        if full_name not in merged:
            merged[full_name] = contact
        else:
            # Merge emails and phone numbers
            merged[full_name]["emails"].extend(contact["emails"])
            merged[full_name]["phone_numbers"].extend(contact["phone_numbers"])
            # Keep only unique emails and phone numbers
            merged[full_name]["emails"] = list(set(merged[full_name]["emails"]))
            merged[full_name]["phone_numbers"] = list(
                set(merged[full_name]["phone_numbers"])
            )
            # Optionally remove contact with lower ID
            if contact["id"] > merged[full_name]["id"]:
                merged[full_name]["id"] = contact["id"]

    # Convert merged dictionary back to a list
    addressbook[:] = list(merged.values())
    print("Contacts merged successfully.")


def read_from_json(filename) -> list:
    """Read contacts from a JSON file."""
    addressbook = []
    # Read file
    with open(os.path.join(sys.path[0], filename)) as outfile:
        json_data = json.load(outfile)
        # Iterate over each line in data
        for contact in json_data:
            addressbook.append(contact)
    return addressbook


def write_to_json(filename, addressbook: list) -> None:
    """Write contacts to a JSON file."""
    json_object = json.dumps(addressbook, indent=4)
    with open(os.path.join(sys.path[0], filename), "w") as outfile:
        outfile.write(json_object)


def main(json_file):
    """Main function for managing contacts."""
    addressbook = read_from_json(json_file)

    while True:
        print("\nMenu:")
        print("[L] List contacts")
        print("[A] Add contact")
        print("[R] Remove contact")
        print("[M] Merge contacts")
        print("[Q] Quit program")

        choice = input("Choose an option: ").strip().upper()

        if choice == "L":
            sorted_contacts = list_contacts(addressbook)
            display(sorted_contacts)
        elif choice == "A":
            first_name = input("Firstname: ").strip()
            last_name = input("Lastname: ").strip()
            emails = input("Emails (comma-separated): ").strip().split(",")
            phone_numbers = input("Phonenumbers (comma-separated): ").strip().split(",")
            add_contact(addressbook, first_name, last_name, emails, phone_numbers)
        elif choice == "R":
            contact_id = int(input("Enter the contact ID to remove: ").strip())
            remove_contact(addressbook, contact_id)
        elif choice == "M":
            merge_contacts(addressbook)
        elif choice == "Q":
            write_to_json(json_file, addressbook)
            print("Exiting program.")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main("file/contacts.json")
