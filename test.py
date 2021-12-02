x = 0
a = 0
b = 0
c = 0
d = 0
y = 0
z = 0

correct_answer = "6"
pre_exec = "global a; global b; global mi_funcion2; a = 2; b = 3"

test_answer = "x= mi_funcion2(a,b)"

def mi_funcion(a):
    return a*a
def mi_funcion2(a,b):
    return a*b

def process_code_answer(answer):
    exec("global x; " + answer)
    print(x)
    return x


exec(pre_exec)
print(correct_answer)
print(str(process_code_answer(test_answer)) == correct_answer)