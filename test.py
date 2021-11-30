x = 0

def process_code_answer(answer):
    exec("global x; " + answer)
    return x

test_answer = "x = 2"
print(process_code_answer(test_answer))