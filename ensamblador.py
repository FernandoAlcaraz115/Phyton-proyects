D1 = [0xF3, 0x2C, 0x4B, 0x5A]
D2 = [0xDD, 0xAC, 0x3F, 0x9D]
D3 = [0xAC, 0x6F, 0xF2, 0x88]
D4 = [0xF2, 0x1D, 0x7C, 0xAA]

def suma_multibyte(A, B):
    resultado = [0]*5
    carry = 0
    for i in range(4):
        temp = A[i] + B[i] + carry
        resultado[i] = temp & 0xFF
        carry = (temp >> 8) & 0xFF
    resultado[4] = carry
    return resultado

R = suma_multibyte(D1, D2)
R = suma_multibyte(R[:4], D3)
R = suma_multibyte(R[:4], D4)

print("Resultado final:", [hex(x) for x in R])




