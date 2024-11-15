class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


        #Ship settings
        self.ship_limit = 3
        self.ship_speed = 10.0

        # Bullet settings
        self.bullet_speed = 50.0
        self.bullet_width = 3
        # self.bullet_speed = 2.5
        self.bullet_height = 15
        self.bullet_color = (247, 188, 237)
        self.bullets_allowed = 30

        # Alien settings
        self.alien_speed = 2.0
        self.fleet_drop_speed = 5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 2

        #  How quickly the game speeds up
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()
        self.score_scale = 1.5

        # Scoring settings
        self.alien_points = 50

    
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 10.0
        self.bullet_speed = 50.0
        self.alien_speed = 10.0
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
    
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)