x = 0
a = 0
b = 0
c = 0
d = 0
y = 0
z = 0

correct_answer = "{'que': 2, 'tal': 3, 'colour': 1}"
pre_exec = "global x; x = {'color': 1,'que': 2,'tal': 3}"

test_answer = "a = x['color']; x.pop('color'); x['colour']=a"

def process_code_answer(answer):
    exec("global x; " + answer)
    print(x)
    return x


exec(pre_exec)
print(correct_answer)
print(str(process_code_answer(test_answer)) == correct_answer)