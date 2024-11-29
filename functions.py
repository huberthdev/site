def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    pesos_1 = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_1 = sum(int(cpf[i]) * pesos_1[i] for i in range(9))
    digito_1 = (soma_1 * 10) % 11
    if digito_1 == 10:
        digito_1 = 0

    pesos_2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
    soma_2 = sum(int(cpf[i]) * pesos_2[i] for i in range(10))
    digito_2 = (soma_2 * 10) % 11
    if digito_2 == 10:
        digito_2 = 0

    return cpf[-2:] == f"{digito_1}{digito_2}"