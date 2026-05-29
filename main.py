# configurações iniciais
import pygame
import random 

pygame.init()
pygame.mixer.init() # Inicializa o módulo de áudio do Pygame

pygame.display.set_caption("jogo da cobrita ")
largura, altura = 700, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# cores RGB
preta = (0, 0, 0)
branca = (255, 255, 255)
vermelha = (255, 0, 0)
verde = (0, 255, 0)
amarela = (255, 255, 0) 
verde_escuro = (28, 80, 28) # Cor do fundo sólido

# parametros da cobrinha
tamanho_quadrado = 10
velocidade_jogo = 12


try:
    img_fim = pygame.image.load("perdeu.png")
    img_fim = pygame.transform.scale(img_fim, (200, 200)) # Ajusta o tamanho da imagem
except:
    img_fim = None

try:
    som_fim = pygame.mixer.Sound("som.mp3")
except:
    som_fim = None

try:
    som_comer = pygame.mixer.Sound("pousound.mp3")
except:
    som_comer = None

    
# -----------------------------------------------------------------------------------------

def gerar_comida():
    while True:
        comida_x = round(random.randrange(0, largura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        comida_y = round(random.randrange(0, altura - tamanho_quadrado) / float(tamanho_quadrado)) * float(tamanho_quadrado)
        
        # Evita que a banana apareça atrás do texto de pontuação (área x < 200 e y < 40)
        if comida_x < 200 and comida_y < 40:
            continue 
            
        return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    # Pontos da banana calculados para formar o desenho curvado
    pontos_banana = [
        (comida_x - 1, comida_y + 9),
        (comida_x + 4, comida_y + 11),
        (comida_x + 8, comida_y + 9),
        (comida_x + 11, comida_y + 4),
        (comida_x + 10, comida_y - 1),
        (comida_x + 7, comida_y + 5),
        (comida_x + 3, comida_y + 6)
    ]
    # Desenha primeiro um contorno preto grosso
    pygame.draw.polygon(tela, preta, pontos_banana, 3)
    # Preenche o miolo com amarelo forte
    pygame.draw.polygon(tela, amarela, pontos_banana, 0)

def desenhar_cobra(tamanho, pixels):
    tamanho_lista = len(pixels)
    
    for i, pixel in enumerate(pixels):
        distancia_da_cabeca = (tamanho_lista - 1) - i
        
        # Cabeça (distância 0 = par) começa PRETA
        if distancia_da_cabeca % 2 == 0:
            cor_corpo = preta 
        # Segundo quadrado (distância 1 = ímpar) fica VERMELHO
        else:
            cor_corpo = vermelha    
            
        pygame.draw.rect(tela, cor_corpo, [pixel[0], pixel[1], tamanho, tamanho])

    if not pixels:
        return

    cabeca = pixels[-1]
    cabeca_x, cabeca_y = cabeca[0], cabeca[1]

    direcao = "DIREITA"  
    if len(pixels) > 1:
        anterior = pixels[-2]
        anterior_x, anterior_y = anterior[0], anterior[1]

        if cabeca_x > anterior_x:   direcao = "DIREITA"
        elif cabeca_x < anterior_x: direcao = "ESQUERDA"
        elif cabeca_y > anterior_y: direcao = "BAIXO"
        elif cabeca_y < anterior_y: direcao = "CIMA"

    cor_lingua = vermelha  
    tam_olho = 2        
    comp_lingua = 4    
    
    if direcao == "DIREITA":
        olho1 = [cabeca_x + tamanho - tam_olho - 2, cabeca_y + 2, tam_olho, tam_olho]
        olho2 = [cabeca_x + tamanho - tam_olho - 2, cabeca_y + tamanho - tam_olho - 2, tam_olho, tam_olho]
        lingua = [cabeca_x + tamanho, cabeca_y + (tamanho // 2) - 1, comp_lingua, 2]
    elif direcao == "ESQUERDA":
        olho1 = [cabeca_x + 2, cabeca_y + 2, tam_olho, tam_olho]
        olho2 = [cabeca_x + 2, cabeca_y + tamanho - tam_olho - 2, tam_olho, tam_olho]
        lingua = [cabeca_x - comp_lingua, cabeca_y + (tamanho // 2) - 1, comp_lingua, 2]
    elif direcao == "CIMA":
        olho1 = [cabeca_x + 2, cabeca_y + 2, tam_olho, tam_olho]
        olho2 = [cabeca_x + tamanho - tam_olho - 2, cabeca_y + 2, tam_olho, tam_olho]
        lingua = [cabeca_x + (tamanho // 2) - 1, cabeca_y - comp_lingua, 2, comp_lingua]
    elif direcao == "BAIXO":
        olho1 = [cabeca_x + 2, cabeca_y + tamanho - tam_olho - 2, tam_olho, tam_olho]
        olho2 = [cabeca_x + tamanho - tam_olho - 2, cabeca_y + tamanho - tam_olho - 2, tam_olho, tam_olho]
        lingua = [cabeca_x + (tamanho // 2) - 1, cabeca_y + tamanho, 2, comp_lingua]

    # Desenha os olhos brancos e a língua vermelha
    pygame.draw.rect(tela, branca, olho1)
    pygame.draw.rect(tela, branca, olho2)
    pygame.draw.rect(tela, cor_lingua, lingua)

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("helvetica", 35)
    texto_sombra = fonte.render(f"pontos: {pontuacao}", True, preta)
    texto = fonte.render(f"pontos: {pontuacao}", True, branca)
    tela.blit(texto_sombra, [3, 3])
    tela.blit(texto, [1, 1])

def selecionar_velocidade(tecla, vel_x_atual, vel_y_atual):
    if tecla == pygame.K_DOWN:
        return 0, tamanho_quadrado
    elif tecla == pygame.K_UP:
        return 0, -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        return tamanho_quadrado, 0
    elif tecla == pygame.K_LEFT:
        return -tamanho_quadrado, 0
    
    return vel_x_atual, vel_y_atual   

# --- TELA DE GAME OVER ---
def tela_fim_de_jogo(pontuacao):
    tela.fill(verde_escuro)
    
    # Texto de Game Over
    fonte = pygame.font.SysFont("helvetica", 50, bold=True)
    texto = fonte.render("VOCE PERDEU!", True, branca)
    tela.blit(texto, (largura//2 - 170, altura//2 - 120))
    
    # Renderiza a imagem (se tiver carregado com sucesso)
    if img_fim:
        tela.blit(img_fim, (largura//2 - 100, altura//2 - 60))
        
    # Botão de reiniciar
    pygame.draw.rect(tela, branca, [largura//2 - 75, altura//2 + 160, 150, 40])
    txt_botao = pygame.font.SysFont("helvetica", 20, bold=True).render("REINICIAR", True, preta)
    tela.blit(txt_botao, (largura//2 - 48, altura//2 + 170))
    
    # Mostra a pontuação final na tela de game over
    desenhar_pontuacao(pontuacao)
    pygame.display.update()

def rodar_jogo():
    # Loop externo que permite recomeçar a partida
    rodando = True
    while rodando:
        fim_jogo = False

        x = largura / 2
        y = altura / 2

        velocidade_x = 0
        velocidade_y = 0

        tamanho_cobra = 1
        pixels = []

        comida_x, comida_y = gerar_comida()

        # Loop interno (Partida rolando)
        while not fim_jogo:
            tela.fill(verde_escuro)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return # Fecha o jogo no X
                elif evento.type == pygame.KEYDOWN:
                    velocidade_x, velocidade_y = selecionar_velocidade(evento.key, velocidade_x, velocidade_y)

            desenhar_comida(tamanho_quadrado, comida_x, comida_y)

            # Bateu nas bordas
            if x < 0 or x >= largura or y < 0 or y >= altura:
                fim_jogo = True

            x += velocidade_x
            y += velocidade_y

            pixels.append([x, y])
            if len(pixels) > tamanho_cobra:
                del pixels[0]

            # Bateu no próprio corpo
            for pixel in pixels[:-1]:
                if pixel == [x, y]:
                    fim_jogo = True

            # Se bateu (fim_jogo virou True), toca som de game over e sai do loop da partida
            if fim_jogo:
                if som_fim: 
                    som_fim.play()
                break 

            desenhar_cobra(tamanho_quadrado, pixels)
            desenhar_pontuacao(tamanho_cobra - 1)

            pygame.display.update()

            # LÓGICA DE COMER A BANANA
            if x == comida_x and y == comida_y:
                if som_comer:          # NOVO: Se o som da banana carregou...
                    som_comer.play()   # NOVO: ...toca o áudio!
                tamanho_cobra += 1
                comida_x, comida_y = gerar_comida()

            relogio.tick(velocidade_jogo)

        # Após perder, entra no loop da tela de game over esperando o clique no botão
        esperando = True
        while esperando:
            tela_fim_de_jogo(tamanho_cobra - 1)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return # Fecha o jogo no X
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    # Verifica se o clique foi dentro do quadrado do botão REINICIAR
                    if (largura//2 - 75) <= mx <= (largura//2 + 75) and (altura//2 + 160) <= my <= (altura//2 + 200):
                        esperando = False # Quebra esse loop de espera e a partida recomeça no "while rodando"

rodar_jogo()