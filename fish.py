import pygame
import random
import math

# Constants
# Exercise 2 Change constants
WIDTH, HEIGHT = 512, 512
NUM_FISH = 50  # Changing this increases/decreases the number of fish in the simulation
MAX_SPEED = 10  # Changing this affects  the fish movement
NEIGHBOR_RADIUS = 100  # Increasing this makes fish more closer
SEPARATION_RADIUS = 30  # Decreasing this makes fish stay closer , increasing it spreads them out
SEPARATION_FORCE = 0.8  # Higher values make fish avoid each other more aggressively
ALIGNMENT_FORCE = 0.1  # Higher values make fish match their speed
COHESION_FORCE = 0.05  # Increasing this makes fish stay closer together 
SCREEN_CENTER = (WIDTH // 2, HEIGHT // 2)
BG_COLOR = (15, 10, 15)
FISH_COLOR = (255, 100, 200)

# New constant for trail effect
TRAIL_ALPHA = 20  # How fast the fish trail fades

class Fish:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = self.random_color()  # Start with a random color
        self.trail = []  # Store positions for trail effect
    
    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random RGB color

    def update(self, flock):
        # Rule 1: Separation (Boid rule1 :avoids crowding its neighbors, which helps prevent collisions)
        separation = self.separate(flock)
        # Rule 2: Alignment(Boid rule 2 : align their direction and speed with the average direction and speed of their neighbors)
        alignment = self.align(flock)
        # Rule 3: Cohesion(Biod rule 3 : move towards the center of mass of their neighbors, helping the group stay together )
        cohesion = self.cohere(flock)

        # Update velocity
        self.vx += separation[0] * SEPARATION_FORCE + alignment[0] * ALIGNMENT_FORCE + cohesion[0] * COHESION_FORCE
        self.vy += separation[1] * SEPARATION_FORCE + alignment[1] * ALIGNMENT_FORCE + cohesion[1] * COHESION_FORCE

        # Add some random fluctuation to make the movement more natural
        self.vx += random.uniform(-0.2, 0.2)
        self.vy += random.uniform(-0.2, 0.2)

        # Limit speed
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > MAX_SPEED:
            scale_factor = MAX_SPEED / speed
            self.vx *= scale_factor
            self.vy *= scale_factor

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Wrap around screen
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0

        # Store positions for trail (to leave a trail behind the fish)
        self.trail.append((self.x, self.y))
        if len(self.trail) > 10:  # Keep the trail length limited
            self.trail.pop(0)

        # Randomly change the fish color over time
        if random.random() < 0.01:
            self.color = self.random_color()

    def separate(self, flock):
        separation_vector = [0, 0]
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance == 0:  # To avoid division by zero
                    distance = 0.001
                if distance < SEPARATION_RADIUS:
                    separation_vector[0] += (self.x - other_fish.x) / distance
                    separation_vector[1] += (self.y - other_fish.y) / distance
        return separation_vector

    def align(self, flock):
        avg_velocity = [0, 0]
        num_neighbors = 0

        # Loop through all the fish in the flock
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < NEIGHBOR_RADIUS:  # If within neighborhood radius
                    avg_velocity[0] += other_fish.vx  # Add the velocity in x-direction
                    avg_velocity[1] += other_fish.vy  # Add the velocity in y-direction
                    num_neighbors += 1

        if num_neighbors > 0:
            avg_velocity[0] /= num_neighbors  # Calculate average velocity in x-direction
            avg_velocity[1] /= num_neighbors  # Calculate average velocity in y-direction
            
            # Return the difference between the fish's velocity and the average velocity of the neighbors
            return [avg_velocity[0] - self.vx, avg_velocity[1] - self.vy]
        else:
            # If no neighbors are within the radius, return a zero vector
            return [0, 0]

    def cohere(self, flock):
        center_of_mass = [0, 0]
        num_neighbors = 0
        for other_fish in flock:
            if other_fish != self:
                distance = math.sqrt((self.x - other_fish.x) ** 2 + (self.y - other_fish.y) ** 2)
                if distance < NEIGHBOR_RADIUS:
                    center_of_mass[0] += other_fish.x
                    center_of_mass[1] += other_fish.y
                    num_neighbors += 1
        if num_neighbors > 0:
            center_of_mass[0] /= num_neighbors
            center_of_mass[1] /= num_neighbors
            return [center_of_mass[0] - self.x, center_of_mass[1] - self.y]
        else:
            return [0, 0]

    def draw(self, screen):
        # Draw fish as an arrow shape
        angle = math.atan2(self.vy, self.vx)
        pygame.draw.polygon(screen, self.color, [(self.x + math.cos(angle) * 10, self.y + math.sin(angle) * 10),
                                                  (self.x + math.cos(angle + 5 * math.pi / 6) * 10, self.y + math.sin(angle + 5 * math.pi / 6) * 10),
                                                  (self.x + math.cos(angle - 5 * math.pi / 6) * 10, self.y + math.sin(angle - 5 * math.pi / 6) * 10)])

        # Draw trail with fading effect
        for i in range(len(self.trail) - 1):
            x1, y1 = self.trail[i]
            x2, y2 = self.trail[i + 1]
            alpha = int(255 * (1 - i / len(self.trail)))  # Fade effect
            color_with_alpha = (*self.color, alpha)
            pygame.draw.line(screen, color_with_alpha, (x1, y1), (x2, y2), 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids Simulation")
    clock = pygame.time.Clock()

    # Create fish
    fish = [Fish(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(-1, 1), random.uniform(-1, 1))
            for _ in range(NUM_FISH)]

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update fish
        for fishy in fish:
            fishy.update(fish)

        # Draw
        screen.fill(BG_COLOR)
        for fishy in fish:
            fishy.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
