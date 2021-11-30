x = 0
a = 0
b = 0
c = 0
d = 0
y = 0
z = 0

correct_answer = "8765432"
pre_exec = "global a; a = '123456789'"

test_answer = "x = a[::-1][1:-1]"

def process_code_answer(answer):
    exec("global x; " + answer)
    return x


exec(pre_exec)
print(str(process_code_answer(test_answer)), correct_answer)
print(str(process_code_answer(test_answer)) == correct_answer)