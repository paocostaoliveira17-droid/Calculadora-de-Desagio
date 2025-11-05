def new_func():
    
    operator = input("Insira um Operador (- + / *):")

    num1 = float (input("Insira o primeiro número:"))
    num2 = float (input("Insira o segundo número:"))

    if operator == "-":
        result = num1 - num2
        print(f"O resultado é {result}")

    elif operator == "+":
        result = num1 + num2
        print(f"O resultado é {result}")

    elif operator == "/":
        result = num1 / num2
        print(f"O resultado é {result}")
    
    elif operator == "*":
        result = num1 * num2
        print(f"O resultado é {result}")

    else:
        print(f"O operador {operator} não é válido")

new_func()