class PasswordManager:
    def __init__(self) -> None:
        self.old_passwords = []

    def get_password(self) -> str:
        if self.old_passwords:
            return self.old_passwords[-1]
        else:
            return None

    def set_password(self, new_password: str) -> bool:
        if new_password not in self.old_passwords:
            self.old_passwords.append(new_password)
            return True
        else:
            print("Password already been used before.")
            return False

    def is_correct(self, password: str) -> bool:
        if self.get_password() == password:
            return True
        else:
            return False


def main():
    pass


if __name__ == "__main__":
    main()
