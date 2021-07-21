# OBJETIVO:
# Desenvolver um Port Scanner simplificado que consiga categorizar as portas
# de um host alvo nessas três classes: "aberta", "filtrada" e "fechada"

# PRIMEIRO PASSO:
# Receber como argumentos da linha de comando o endereço do host alvo
# (seja um hostname, seja diretamente o endereço IP)
# e uma faixa de números de porta a serem analisados (por exemplo, da porta 21 até a porta 1024)

# SEGUNDO PASSO:
# Varrer essas portas tentando estabelecer conexões e, com base no resultado dessa tentativa,
# classificar cada porta da faixa

# TERCEIRO PASSO:
# Ao final da execução, o programa deverá listar todas as portas "abertas",
# todas as portas "filtradas" e todas as portas "fechadas"