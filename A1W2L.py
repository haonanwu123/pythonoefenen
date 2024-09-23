class A:
    def __init__(self, func):
        self.name = 'Tom'
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(self.name)
    
def hi(name):
    print(f"hallo, {name}!")

a = A(hi)
a()