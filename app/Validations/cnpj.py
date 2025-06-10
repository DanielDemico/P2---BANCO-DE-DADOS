from itertools import cycle

def validate_cnpj(cnpj: str) -> bool:
    for algarismo in cnpj:
            if not algarismo.isnumeric():
                return False
            
    if len(cnpj) != 14:
         return False
    
    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False
    
    return True

if __name__ == "__main__":
    print(validate_cnpj("90306453000133"))