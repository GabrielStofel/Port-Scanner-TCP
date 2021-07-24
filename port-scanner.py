import socket

# OBJETIVO:
# Desenvolver um Port Scanner simplificado que consiga categorizar as portas
# de um host alvo nessas três classes: "aberta", "filtrada" e "fechada"
def run():
    address = input("Hostname/Endereço IP: ")

    faixa_prompt = "Faixa de portas a ser analisada separando com um espaço o início e o fim dela (e.g. '20 80'): "
    faixa = input(faixa_prompt).split()
    ini_faixa, fim_faixa = list(map(int, faixa))
    portas = range(ini_faixa, fim_faixa + 1)

    tipo_portas = []
    for porta in portas:
        # Por padrão, quando se cria uma instância de socket sem passar parâmetros,
        # o tipo de protocolo padrão utilizado é o protocolo TCP
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Estabelece um tempo máximo para o timeout
        socket.setdefaulttimeout(2)

        # Se conecta ao endereço passado e retorna um código correspondente ao resultado da conexão
        codigo = cliente.connect_ex((address, porta))
        
        # Descobre o que fazer baseado no código retornado
        tipo = get_port_type(codigo)
        tipo_portas.append(tipo)
    
    print(f"Classe das portas do host '{address}':")
    for port, port_type in zip(portas, tipo_portas):
        print(f"{port} = {port_type}")


def get_port_type(codigo: int) -> str:
    if codigo == 0:
        return "aberta"
    
    else:
        return ""

# Aberta == (Código 0)
# Filtrada == host inacessível ou tentativa de conexão bloqueada por um firewall (Código ?) 
# Fechada == host envia mensagem de erro (Código ?)

if __name__  == "__main__":
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

    run()