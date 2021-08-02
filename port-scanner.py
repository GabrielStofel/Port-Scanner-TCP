import socket
import platform
from threading import Thread

# Número de threads
NUM_THREADS = 100
# Pilha com números das portas a serem escaneadas
stack_ports = []
# Vetor com tipo de cada uma das portas começando da primeira porta da faixa e indo até o último
# de forma ordenada crescentemente
tipo_portas = []

# OBJETIVO:
# Desenvolver um Port Scanner simplificado que consiga categorizar as portas
# de um host alvo nessas três classes: "aberta", "filtrada" e "fechada"
def run():
    address = input("Hostname/Endereço IP: ").strip()

    faixa_prompt = "Faixa de portas a ser analisada separando com um espaço o início e o fim dela (e.g. '20 80'): "
    faixa = input(faixa_prompt).strip().split()
    ini_faixa, fim_faixa = list(map(int, faixa))
    portas = range(ini_faixa, fim_faixa + 1)

    # Criando pilha com número das portas para posterior acesso pelas threads
    for porta in portas:
        stack_ports.append(porta)
        tipo_portas.append("")

    # Definindo número de threads para que não existam mais threads do que portas a serem escaneadas
    NUM_THREADS = (fim_faixa-ini_faixa)//2

    # Criando threads
    threads = []
    for i in range(NUM_THREADS):
        # Instanciando thread.
        # Definindo a função scan como função a ser executada por ela.
        # Definindo daemon como True para que a thread seja encerrada automaticamente com o programa,
        # sem necessidade de encerrá-la explicitamente.
        # Passando argumentos da função scan através do parâmetro args.
        thread = Thread(target=scan, daemon=True, args=(ini_faixa, address))

        # Guardando threads criadas em um vetor para que possam ser manipuladas posteriormente.
        threads.append(thread)

        # Iniciando execução da thread.
        thread.start()

    for t in threads:
        # Realizando join para que o programa principal siga nas linhas abaixo para imprimir o resultado 
        # apenas depois de todas as threads terminarem seus processamentos e conexões.
        t.join()

    print(f"Classe das portas do host '{address}':")
    for port, port_type in zip(portas, tipo_portas):
        print(f"{port} = {port_type}")

def scan(ini_faixa, address):
    global stack_ports, tipo_portas
    
    # Por padrão, quando se cria uma instância de socket sem passar parâmetros,
    # o tipo de protocolo padrão utilizado é o protocolo TCP.
    # O argumento AF_INET indica que o socket pertence a família de protocolos internet.
    # O argumetno SOCK_STREAM se refere a socket voltado a fluxo confiável de dados que indica o TCP.
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Estabelece um tempo máximo para o timeout
    #socket.setdefaulttimeout(2)

    while stack_ports != []:
        # Pega número de porta a ser escaneada caso ainda exista alguma na pilha
        porta = stack_ports.pop()

        # Se conecta ao endereço passado e retorna um código correspondente ao resultado da conexão
        codigo = cliente.connect_ex((address, porta))
        
        # Descobre o que fazer baseado no código retornado
        tipo = get_port_type(codigo)
        # Atribui tipo da porta no lugar equivalente no vetor
        # Subtração utilizada para encontrar posição correta no vetor.
        tipo_portas[porta-ini_faixa] = tipo  

    # Fechamento do socket
    cliente.close()   

def get_port_type(codigo: int) -> str:
    if codigo == 0:
        return "aberta"
    else:
        so = platform.system()
        if(so == 'Windows' and codigo == 10060) or (so == 'Linux' and codigo == 110) or (so == 'Darwin' and codigo == 60):
          return "filtrada"
        return "fechada"

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