read.me jogo da cobrinha:
esse é um jogo da cobrinha que fiz usando pygame.

nesse jogo voce controla uma cobrinha que come bananas, seu objetivo é comer o maximo de bananas e bater seu recorde sem morrer, os controles sao basicos, apenas usando as setas pra se movimentar e comer as bananas, se vc bater no seu propio corpo ou nas bordas do mapa voce perde.

para jogar o jogo, voce deve baixar o py game no seu vscode e abrir depois abrir o main.py e dar run no codigo, de enter e começe a se mexer

Divirta-se :D

-->Design da Comida (Banana):** Substituí o padrão geométrico simples por um desenho em polígono com contorno, melhorando a identificação visual do item coletável no mapa.
-->Inteligência de Orientação:** A cabeça da cobra (incluindo olhos e língua) possui um sistema de detecção de direção. A face da cobra é renderizada dinamicamente com base no seu vetor de movimento (Cima, Baixo, Esquerda ou Direita).
-->Estilo Visual do Fundo:** O fundo foi definido como um verde escuro sólido, removendo ruídos visuais de texturas desnecessárias e focando na clareza do jogo.
-->Padrão do Corpo (Listras):** A cobra apresenta um padrão listrado alternando entre preto e vermelho. A lógica é baseada na paridade da distância de cada segmento em relação à cabeça, garantindo que o padrão se mantenha consistente mesmo quando a cobra aumenta de tamanho.