import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Rescate Galáctico")

# Colores
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

class Juego:
    def __init__(self):
        self.reloj = pygame.time.Clock()
        self.correr = True
        self.astronauta = Astronauta(ANCHO // 2, ALTO // 2)
        self.extraterrestres = [Extraterrestre(random.randint(0, ANCHO), random.randint(0, ALTO)) for _ in range(10)]
        self.puntaje = 0
        self.total_extraterrestres = len(self.extraterrestres)

    def correr_juego(self):
        while self.correr:
            self.gestionar_eventos()
            self.actualizar_estado()
            self.dibujar()
            self.verificar_condiciones_ganador()
            pygame.display.flip()
            self.reloj.tick(30)
        pygame.quit()

    def gestionar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.correr = False

    def actualizar_estado(self):
        teclas = pygame.key.get_pressed()
        self.astronauta.mover(teclas)
        for extraterrestre in self.extraterrestres:
            extraterrestre.mover()
        if self.astronauta.capturar(self.extraterrestres):
            self.puntaje += 1
            print(f"¡Extraterrestre capturado! Puntaje: {self.puntaje}")

    def dibujar(self):
        VENTANA.fill(VERDE)
        pygame.draw.rect(VENTANA, ROJO, (0, 0, ANCHO, ALTO), 10)
        for extraterrestre in self.extraterrestres:
            extraterrestre.dibujar()
        self.astronauta.dibujar()
        self.mostrar_puntaje()

    def mostrar_puntaje(self):
        fuente = pygame.font.Font(None, 36)
        texto_puntaje = fuente.render(f"Puntaje: {self.puntaje}", True, BLANCO)
        VENTANA.blit(texto_puntaje, (10, 10))

    def verificar_condiciones_ganador(self):
        if self.puntaje == self.total_extraterrestres:
            self.mostrar_mensaje_final("¡Congratulations! Rescataste todos los extraterrestres")
            pygame.time.delay(3000)
            self.correr = False

    def mostrar_mensaje_final(self, mensaje):
        fuente = pygame.font.Font(None, 36)
        mensaje_final = fuente.render(mensaje, True, BLANCO)
        VENTANA.blit(mensaje_final, (ANCHO//2 - mensaje_final.get_width()//2, ALTO//2 - mensaje_final.get_height()//2))
        pygame.display.flip()

class Astronauta:
    def __init__(self, x, y, velocidad=5):
        self.x = x
        self.y = y
        self.velocidad = velocidad
        self.imagen = pygame.image.load('astronauta.png')
        self.imagen = pygame.transform.scale(self.imagen, (50, 50))
        self.rect = self.imagen.get_rect(center=(self.x, self.y))

    def dibujar(self):
        VENTANA.blit(self.imagen, self.rect)

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO - 10:
            self.rect.x += self.velocidad
        if teclas[pygame.K_UP] and self.rect.top > 10:
            self.rect.y -= self.velocidad
        if teclas[pygame.K_DOWN] and self.rect.bottom < ALTO - 10:
            self.rect.y += self.velocidad

    def capturar(self, extraterrestres):
        for extraterrestre in extraterrestres:
            if self.rect.colliderect(extraterrestre.rect):
                extraterrestres.remove(extraterrestre)
                return True
        return False

class Extraterrestre:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.imagen = pygame.image.load('extraterrestre.png')
        self.imagen = pygame.transform.scale(self.imagen, (40, 40))
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
        self.velocidad = random.randint(3, 6)
        self.direccion_x = random.choice([-1, 1])
        self.direccion_y = random.choice([-1, 1])

    def dibujar(self):
        VENTANA.blit(self.imagen, self.rect)

    def mover(self):
        self.rect.x += self.velocidad * self.direccion_x
        self.rect.y += self.velocidad * self.direccion_y
        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.direccion_x *= -1
        if self.rect.top <= 0 or self.rect.bottom >= ALTO:
            self.direccion_y *= -1

if __name__ == "__main__":
    juego = Juego()
    juego.correr_juego()
