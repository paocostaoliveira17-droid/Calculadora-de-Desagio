def calcular_imc(peso, altura):
    return peso / (altura ** 2)

def classificar_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 25:
        return "Peso normal"
    elif 25 <= imc < 30:
        return "Sobrepeso"
    elif 30 <= imc < 35:
        return "Obesidade Grau I"
    elif 35 <= imc < 40:
        return "Obesidade Grau II"
    else:
        return "Obesidade Grau III"

def main():
    print("Calculadora de IMC\n")

    try:
        peso = float(input("Digite seu peso em kg (ex: 70.5): "))
        altura = float(input("Digite sua altura em metros (ex: 1.75): "))

        if peso <= 0 or altura <= 0:
            print("Peso e altura devem ser maiores que zero.")
            return

        imc = calcular_imc(peso, altura)
        classificacao = classificar_imc(imc)

        print(f"\nSeu IMC é: {imc:.2f}")
        print(f"Classificação: {classificacao}")

    except ValueError:
        print("Entrada inválida. Use apenas números (ex: 70.5 para peso, 1.75 para altura).")

if __name__ == "__main__":
    main()
