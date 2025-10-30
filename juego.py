import pygame, random, sys

pygame.init()
ANCHO, ALTO = 700, 500
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Alerta CO — Prevención del Monóxido de Carbono")
clock = pygame.time.Clock()

fondo = pygame.transform.scale(pygame.image.load("imagenes/fondo2.jpg"), (ANCHO, ALTO))
jugador_img = pygame.transform.scale(pygame.image.load("imagenes/jugador.png"), (50, 50))
riesgo_img = pygame.transform.scale(pygame.image.load("imagenes/peligro.png"), (40, 40))
ventilador_img = pygame.transform.scale(pygame.image.load("imagenes/ventilador.png"), (90, 90))

pygame.mixer.music.load("sonidos/musica.mp3")
pygame.mixer.music.play(-1)
alarma = pygame.mixer.Sound("sonidos/alarma.mp3")
correcto = pygame.mixer.Sound("sonidos/correcto.mp3")

font = pygame.font.SysFont("arial", 28)
boton_font = pygame.font.SysFont("arial", 26)

def reiniciar():
    global jugador, riesgos, ventiladores, co_nivel, juego_terminado, gano
    jugador = pygame.Rect(100, 250, 50, 50)
    riesgos = [pygame.Rect(random.randint(150, 650), random.randint(80, 420), 40, 40) for _ in range(4)]
    ventiladores = []
    co_nivel = 0
    juego_terminado = False
    gano = False

reiniciar()

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.MOUSEBUTTONDOWN and juego_terminado:
            if boton.collidepoint(e.pos):
                reiniciar()

    teclas = pygame.key.get_pressed()
    if not juego_terminado:
        if teclas[pygame.K_LEFT] and jugador.x > 0: jugador.x -= 5
        if teclas[pygame.K_RIGHT] and jugador.x < ANCHO - 50: jugador.x += 5
        if teclas[pygame.K_UP] and jugador.y > 0: jugador.y -= 5
        if teclas[pygame.K_DOWN] and jugador.y < ALTO - 50: jugador.y += 5
        if teclas[pygame.K_SPACE]:
            ventiladores.append(pygame.Rect(jugador.x, jugador.y, 60, 60))
            correcto.play()

        co_nivel += 0.05

        for r in riesgos[:]:
            if jugador.colliderect(r):
                riesgos.remove(r)
                co_nivel -= 10
                correcto.play()

        for v in ventiladores[:]:
            co_nivel -= 0.2
            if co_nivel < 0:
                co_nivel = 0

        if co_nivel >= 100:
            juego_terminado = True
            alarma.play()
        if not riesgos and co_nivel < 50:
            gano = True
            juego_terminado = True

    pantalla.blit(fondo, (0, 0))
    pantalla.blit(jugador_img, jugador)
    for r in riesgos:
        pantalla.blit(riesgo_img, r)
    for v in ventiladores:
        pantalla.blit(ventilador_img, v)

    pygame.draw.rect(pantalla, (255, 0, 0), (50, 30, co_nivel * 5, 20))
    texto = font.render(f"Nivel CO: {int(co_nivel)}", True, (255, 255, 255))
    pantalla.blit(texto, (50, 5))

    if juego_terminado:
        if gano:
            msg = "Recorda Ventilar el ambiente para prevenir intoxicación"
            color = (0, 143, 57)
        else:
            msg = "¡Peligro! Intoxicación por monoxido de carbono"
            color = (255, 0, 0)
        t = font.render(msg, True, color)
        pantalla.blit(t, (ANCHO//2 - t.get_width()//2, ALTO//2 - 40))
        boton = pygame.Rect(ANCHO//2 - 70, ALTO//2 + 20, 140, 50)
        pygame.draw.rect(pantalla, (0, 0, 0), boton, border_radius=8)
        txt_boton = boton_font.render("Reiniciar", True, (255, 255, 255))
        pantalla.blit(txt_boton, (boton.centerx - txt_boton.get_width()//2, boton.centery - txt_boton.get_height()//2))

    pygame.display.flip()
    clock.tick(60)
