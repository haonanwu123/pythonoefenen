# def fib(n):
#     if n <= 1:
#         return n
#     return fib(n - 1) + fib(n - 2)

# print(fib(4))

# li = ['a', 'b', 'c']
# while li:
#     print(li.pop(), end=' ')  



# data_list = [[]] * 3 # output [[], [], []]
# data_list[0].append(10)# output [[10], [10], [10]]
# data_list[1].append(20)# output [[10,20], [10,20], [10,20]]
# print(data_list)

# data_list = [[] for _ in range(3)]# output [[], [], []]
# data_list[0].append(10)# output [[10], [], []]
# data_list[1].append(20)# output [[10], [20], []]
# print(data_list)


def func(n):
    if n:
        return n + func(n-1)
    else:
        return n
    
print(func(3)) #output 3+(2+(1+(0)))