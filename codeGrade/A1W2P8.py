import re

patterns = [
    r'^[A-Z]{2}-\d{2}-\d{2}$',  # XX-99-99
    r'^\d{2}-\d{2}-[A-Z]{2}$',  # 99-99-XX
    r'^\d{2}-[A-Z]{2}-\d{2}$',  # 99-XX-99
    r'^[A-Z]{2}-\d{2}-[A-Z]{2}$',  # XX-99-XX
    r'^[A-Z]{2}-[A-Z]{2}-\d{2}$',  # XX-XX-99
    r'^\d{2}-[A-Z]{2}-[A-Z]{2}$',  # 99-XX-XX
    r'^\d{2}-[A-Z]{3}-\d$',  # 99-XXX-9
    r'^\d-[A-Z]{3}-\d{2}$',  # 9-XXX-99
    r'^[A-Z]{2}-\d{3}-[A-Z]$',  # XX-999-X
    r'^[A-Z]-\d{3}-[A-Z]{2}$',  # X-999-XX
    r'^[A-Z]{3}-\d{2}-[A-Z]$',  # XXX-99-X
    r'^\d-[A-Z]{2}-\d{3}$'  # 9-XX-999
]

def check_license_plate(license_plate):
    license_plate = license_plate.strip().upper()

    for pattern in patterns:
        if re.match(pattern, license_plate):
            return "Valid"
    
    return "Invalid"

license_plate = input("License: ")

result = check_license_plate(license_plate)
print(result)