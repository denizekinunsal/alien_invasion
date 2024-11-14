import sys
import pygame
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
# bullet.py
from alien import Alien
# alien.py'dosyasının içindeki Alien fonksiyonunu yükle

from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    
    def __init__(self):
        """Initialize the game, and create game resources."""

        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play") 
        self.bg_image = pygame.image.load('images/background.jpg')
        # oluşturduğumuz dosyaların içindeki sınıfları ve python ve pygame komutlarını yüklediğimiz alan

        

    def run_game(self):
        """Start the main loop for the game."""
        # self.screen.fill(self.settings.bg_color)
        # self.ship.blitme()
        self.screen.blit(self.bg_image, (0, 0)) #arkaplan resmi ayarlıyor"
        pygame.display.update() #
        
        while True:
            
            self._check_events() # kullanıcı girişini kontrol ediyor
            
            if self.game_active: #play tuşuna basılmadan oyunun oynanmasını engelleyen komut
                self.ship.update() #geminin hareket etmesine yarayan fonksiyon
                self._update_bullets() #mermileri kontrol eden fonksiyon
                self._update_aliens() #uzaylıları kontrol eden fonksiyon
            self._update_screen() #ekranı tamamiyle yenileyerek ekrana yazdırılması gereken yazıları veya resimleri yazdırır
            

            
            for bullet in self.bullets.copy(): #mermilerin ekrandan çıkıp silinmesini kontrol ediyor
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                    print(len(self.bullets))
                        
            # ben neyimmmmm <33333333333333333333333 
            # Watch for keyboard and mouse events.
            for event in pygame.event.get(): #oyundan çıkılması yönünde komut gelirse sys.exit() komutu ile programı tamamiyle kapatıyor
                if event.type == pygame.QUIT:
                    sys.exit()
            # Make the most recently drawn screen visible.
                    
            pygame.display.flip()
            self.clock.tick(30) 
            

    def _check_events(self): #kullanıcıdan gelen verileri işleyen fonksiyon
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event): #bir tuşa basılınca yapılacak işin ayarları
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self): #ateş etme fonksiyonu
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
              
    def _check_bullet_alien_collisions(self): #merminin uzaylıya değmesiyle tetiklenen olayları gerçekleştiren fonksiyon
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
               
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.bg_image, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < self.settings.screen_width:
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
            """Create an alien and place it in the row."""
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
        

    def _check_fleet_edges(self): #uzaylıların ekranın köşesine vardığındaki tepkilerini gerçekleştirir
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()
            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

if __name__ == '__main__': #main komut
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game() #oyunun penceresinin açılmasını sağlar