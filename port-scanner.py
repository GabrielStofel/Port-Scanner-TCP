import socket
import platform
from threading import Thread

# Número de threads
NUM_THREADS = 100
# Pilha com números das portas a serem escaneadas
stack_ports = []
# Vetor com tipo de cada uma das portas começando da primeira porta da faixa e indo até o último
# de forma ordenada crescentemente
type_doors = []

# OBJETIVO:
# Desenvolver um Port Scanner simplificado que consiga categorizar as portas
# de um host alvo nessas três classes: "aberta", "filtrada" e "fechada"
def run():
    address = input("Hostname/Endereço IP: ").strip()

    range_prompt = "Faixa de portas a ser analisada separando com um espaço o início e o fim dela (e.g. '20 80'): "
    r = input(range_prompt).strip().split()
    ini_range, end_range = list(map(int, r))
    doors = range(ini_range, end_range + 1)

    # Criando pilha com número das portas para posterior acesso pelas threads
    for door in doors:
        stack_ports.append(door)
        type_doors.append("")

    # Definindo número de threads para que não existam mais threads do que portas a serem escaneadas
    NUM_THREADS = (end_range-ini_range)//2

    # Criando threads
    threads = []
    for i in range(NUM_THREADS):
        # Instanciando thread.
        # Definindo a função scan como função a ser executada por ela.
        # Definindo daemon como True para que a thread seja encerrada automaticamente com o programa,
        # sem necessidade de encerrá-la explicitamente.
        # Passando argumentos da função scan através do parâmetro args.
        thread = Thread(target=scan, daemon=True, args=(ini_range, address))

        # Guardando threads criadas em um vetor para que possam ser manipuladas posteriormente.
        threads.append(thread)

        # Iniciando execução da thread.
        thread.start()

    for t in threads:
        # Realizando join para que o programa principal siga nas linhas abaixo para imprimir o resultado 
        # apenas depois de todas as threads terminarem seus processamentos e conexões.
        t.join()

    #Impressão dos números das portas e seus respectivos estados (aberta, fechada ou filtrada)
    print(f"Classe das portas do host '{address}':")
    for door, door_type in zip(doors, type_doors):
        print(f"{door} = {door_type}")

def scan(ini_range, address):
    global stack_ports, type_doors
    
    # Por padrão, quando se cria uma instância de socket sem passar parâmetros,
    # o tipo de protocolo padrão utilizado é o protocolo TCP.
    # O argumento AF_INET indica que o socket pertence a família de protocolos internet.
    # O argumetno SOCK_STREAM se refere a socket voltado a fluxo confiável de dados que indica o TCP.
    user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while stack_ports != []:
        # Pega número de porta a ser escaneada caso ainda exista alguma na pilha
        door = stack_ports.pop()

        # Se conecta ao endereço passado e retorna um código correspondente ao resultado da conexão
        code = user.connect_ex((address, door))
        
        # Descobre o que fazer baseado no código retornado
        type = get_port_type(code)
        # Atribui tipo da porta no lugar equivalente no vetor
        # Subtração utilizada para encontrar posição correta no vetor.
        type_doors[door-ini_range] = type 

    # Fechamento do socket
    user.close()   

def get_port_type(code: int) -> str:
    # Se o código recebido for o número 0, então a porta está aberta.
    # Aberta == (Código 0)
    if code == 0:
        return "aberta"
    # Se o código recebido for diferente de 0, então a porta pode estar fechada ou filtrada.
    else:
        # Nesses casos os códigos variam para cada Sistema operacional, então primeiramente identificamos o SO do usuário e relacionamos com o código recebido.
        so = platform.system()
        # Filtrada == host inacessível ou tentativa de conexão bloqueada por um firewall (Código 10060 windows, 110 linux, 60 macos) 
        # A conexão expirou. Uma tentativa de conexão falhou porque a parte conectada não respondeu corretamente após um período de tempo, ou a conexão estabelecida falhou porque o host conectado não respondeu.
        if(so == 'Windows' and code == 10060) or (so == 'Linux' and code == 110) or (so == 'Darwin' and code == 60):
          return "filtrada"
        # Se o tipo da porta não for filtrada então consideramos que qualquer outro código de erro recebido indicará que a porta está fechada
        # Fechada == host envia mensagem de erro.
        return "fechada"


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