# Port-Scanner-TCP

Trabalho de implementação em grupo realizado para a Disciplina de Redes de Computadores. 
O objetivo do trabalho é desenvolver um Port Scanner simplificado que consiga categorizar as portas de um host alvo em três classes: **aberta**, **filtrada** e **fechada**.

### Integrantes do grupo

* Gabriel Stofel de Souza
* Gabriela Pinheiro Costa
* Karina Pereira de Lemos
* Valesca Moura de Sousa

### Funcionamento do programa

O programa desenvolvido recebe como argumentos da linha de comando o endereço do host alvo (seja um hostname, seja diretamente o endereço IP) e uma faixa de números de porta a serem analisados (por exemplo, da porta 21 até a porta 1024). O programa varre essas portas tentando estabelecer conexões e, com base no resultado dessa tentativa, classifica cada porta da faixa. Ao final da execução, o programa lista todas as portas abertas, todas as portas filtradas e todas as portas fechadas.

### Como rodar o script python

Para executar o script python, basta rodar o seguinte comando na linha de comando:
```shell
python port-scanner.py
```
E depois informar o hostname/IP e faixa de porta quando requisitado pelo programa.

### Otimização do programa

Para realizar a otimização do programa, em primeiro lugar, cada conexão tem um tempo máximo de *timeout* setado previamente, que é menor do que o *timeout* padrão para quando não se obtém uma resposta.
Em segundo lugar, foram utilizadas threads. As threads utlizadas são da biblioteca *threading*, nativa do Python. As threads desta biblioteca não são executadas simultaneamente de fato, apenas uma realiza processamento na CPU por vez, devido ao GIL - *Global Interpreter Lock* - que gera um bloqueio e só permite que uma thread use o interpretador Python a cada vez. Para realizar processamento simultaneamente poderia ser utilizada a biblioteca *multiprocessing*, que cria subprocessos para cada tarefa e, por isso, não é bloqueada pelo GIL. No entanto, ela geraria uma sobrecarga com a criação e administração de vários processos que, para este problema, não é necessária visto que não existe computação massiva para CPU e existe um tempo de espera considerável no acesso à rede. Isso torna o uso da biblioteca *threading* mais eficiente.

A aceleração do programa foi feita através da criação de threads em número sempre igual, ou aproximado, à metade do número total de portas a serem escaneadas. Dessa forma, cada thread deverá escanear, aproximadamente, duas portas. Levando em consideração que nos casos onde a porta é filtrada a aplicação recebe um *timeout* ao tentar se conectar ao host e isso consome mais tempo do que quando a porta está aberta ou simplesmente o host envia uma mensagem de erro, percebe-se que é possível que uma thread fique "parada" esperando a reposta de uma porta enquanto outra obteve respostas muito mais rapidamente. Como não é possível saber previamente quais portas demorarão mais para serem classificadas devido ao *timeout*, dividir o número de portas igualmente entre as threads não é tão eficiente. A alternativa utilizada aqui foi o uso de uma pilha de portas que todas as threads têm acesso e vão consumindo as portas para efetuar uma conexão conforme terminam as conexões em andamento caso ainda existam portas restantes na pilha. Dessa maneira, a thread que está livre sempre pega uma nova porta para escanear, independente do número de portas já escaneado. Cada uma das threads atribui o resultado da porta escaneada a um vetor que é impresso no terminal pela thread principal do programa, para que não haja concorrência ou sobrescrita.