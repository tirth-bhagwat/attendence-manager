import functools

x=('enroll_num', 'f_name','c','d')
x=('',)+x

res=str(functools.reduce(lambda i,j:f'''{i},"{j}"''',x))[1:]

print(res)
print(x)

