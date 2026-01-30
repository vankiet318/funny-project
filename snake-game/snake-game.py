import turtle
import random
import time

# Game settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
DELAY = 0.1  # Game speed

# Direction definitions
UP = (0, 20)
DOWN = (0, -20)
LEFT = (-20, 0)
RIGHT = (20, 0)

# Colors
COLOR_SNAKE_BODY = "green"
COLOR_SNAKE_HEAD = "darkgreen"
COLOR_FOOD = "red"
COLOR_BG = "black"
COLOR_TEXT = "white"
COLOR_BORDER = "#333333"

class Snake:
    def __init__(self):
        self.body = [(0, 0), (20, 0), (40, 0)]  # Initial snake body
        self.direction = RIGHT
        self.grow = False
        self.started = False  # Track if player has started moving
        
        # Snake drawing segments
        self.segments = []
        self.create_snake()
    
    def create_snake(self):
        """Create initial snake"""
        for position in self.body:
            self.add_segment(position)
    
    def add_segment(self, position, is_head=False):
        """Add a segment to the snake"""
        segment = turtle.Turtle()
        segment.shape("square")
        segment.color(COLOR_SNAKE_HEAD if is_head else COLOR_SNAKE_BODY)
        segment.penup()
        segment.goto(position)
        if is_head:
            self.segments.insert(0, segment)
        else:
            self.segments.append(segment)
    
    def move(self):
        """Move the snake"""
        # Only move if game has started
        if not self.started:
            return
            
        # Calculate new head position
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Add new head to body
        self.body.insert(0, new_head)
        
        # Remove tail if not growing
        if not self.grow:
            self.body.pop()
            # Remove and clear tail segment
            if len(self.segments) > len(self.body):
                tail_segment = self.segments.pop()
                tail_segment.hideturtle()
                tail_segment.clear()
        else:
            self.grow = False
            # Add new segment when growing
            self.add_segment(self.body[-1])
        
        # Update head color
        if len(self.segments) > 0:
            self.segments[0].color(COLOR_SNAKE_HEAD)
            
        # Update body segments
        for i in range(1, len(self.segments)):
            self.segments[i].color(COLOR_SNAKE_BODY)
                
        # Update all segment positions to match body
        for i, position in enumerate(self.body):
            if i < len(self.segments):
                self.segments[i].goto(position)
            else:
                # Create missing segment
                self.add_segment(position)
    
    def change_direction(self, new_direction):
        """Change direction (can't reverse)"""
        self.started = True  # Game starts when player presses a key
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction
    
    def check_collision(self):
        """Check for collisions"""
        if not self.started:
            return False  # No collision check until game starts
            
        head_x, head_y = self.body[0]
        
        # Wall collision
        if (head_x < -WINDOW_WIDTH//2 or head_x >= WINDOW_WIDTH//2 or
            head_y < -WINDOW_HEIGHT//2 or head_y >= WINDOW_HEIGHT//2):
            return True
        
        # Self collision (only check if body has more than 3 segments)
        if len(self.body) > 3 and self.body[0] in self.body[1:]:
            return True
        
        return False
    
    def eat_food(self, food_pos):
        """Check if food is eaten"""
        if not self.started:
            return False
        if self.body[0] == food_pos:
            self.grow = True
            return True
        return False

class Food:
    def __init__(self, snake_body=None):
        if snake_body is None:
            snake_body = []
        self.position = self.generate_position(snake_body)
        self.create_food()
    
    def create_food(self):
        """Create food"""
        self.food = turtle.Turtle()
        self.food.shape("circle")
        self.food.color("red")
        self.food.penup()
        self.food.goto(self.position)
    
    def generate_position(self, snake_body):
        """Generate random position that doesn't overlap with snake"""
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(-WINDOW_WIDTH//2 + GRID_SIZE, 
                              WINDOW_WIDTH//2 - GRID_SIZE)
            y = random.randint(-WINDOW_HEIGHT//2 + GRID_SIZE, 
                              WINDOW_HEIGHT//2 - GRID_SIZE)
            # Align to grid
            x = (x // GRID_SIZE) * GRID_SIZE
            y = (y // GRID_SIZE) * GRID_SIZE
            position = (x, y)
            if position not in snake_body:
                return position
        # Fallback if can't find position
        return (100, 100)
    
    def respawn(self, snake_body):
        """Respawn food at new position"""
        self.position = self.generate_position(snake_body)
        self.food.goto(self.position)

class Game:
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open(".highscore", "r") as f:
                return int(f.read())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        """Save high score to file"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open(".highscore", "w") as f:
                f.write(str(self.high_score))

    def draw_border(self):
        """Draw game border"""
        border = turtle.Turtle()
        border.speed(0)
        border.color(COLOR_BORDER)
        border.penup()
        border.goto(-WINDOW_WIDTH//2 + 10, -WINDOW_HEIGHT//2 + 10)
        border.pendown()
        border.pensize(3)
        for _ in range(4):
            border.forward(WINDOW_WIDTH - 20)
            border.left(90)
        border.hideturtle()

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.screen.bgcolor(COLOR_BG)
        self.screen.title("Snake Game")
        self.screen.tracer(0)  # Disable animation (manual update)
        
        # Border
        self.draw_border()
        
        # Score display
        self.score = 0
        self.high_score = self.load_high_score()
        self.score_display = turtle.Turtle()
        self.score_display.hideturtle()
        self.score_display.color(COLOR_TEXT)
        self.score_display.penup()
        self.score_display.goto(0, WINDOW_HEIGHT//2 - 40)
        
        # Initialize game objects
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_over = False
        self.delay = DELAY
        
        # Set up key bindings
        self.setup_keys()
        self.update_score()
        self.show_start_message()
        
        # Initial screen update
        self.screen.update()
    
    def show_start_message(self):
        """Show start message"""
        start_msg = turtle.Turtle()
        start_msg.hideturtle()
        start_msg.color("yellow")
        start_msg.penup()
        start_msg.goto(0, -50)
        start_msg.write("Press any arrow key or WASD to start", 
                       align="center", 
                       font=("Arial", 14, "normal"))
        self.start_message = start_msg
    
    def setup_keys(self):
        """Setup keyboard controls"""
        self.screen.listen()
        # Direct functions to ensure one call
        def turn_up(): self.snake.change_direction(UP)
        def turn_down(): self.snake.change_direction(DOWN)
        def turn_left(): self.snake.change_direction(LEFT)
        def turn_right(): self.snake.change_direction(RIGHT)
        
        self.screen.onkey(turn_up, "Up")
        self.screen.onkey(turn_down, "Down")
        self.screen.onkey(turn_left, "Left")
        self.screen.onkey(turn_right, "Right")
        self.screen.onkey(turn_up, "w")
        self.screen.onkey(turn_down, "s")
        self.screen.onkey(turn_left, "a")
        self.screen.onkey(turn_right, "d")
        self.screen.onkey(self.reset_game, "space")
    
    def reset_game(self):
        """Reset the game"""
        # Save high score before reset
        self.save_high_score()
        
        # Clear screen and re-init
        self.screen.clearscreen()
        self.__init__()
    
    def update_score(self):
        """Update score display"""
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}  High Score: {self.high_score}", 
                                align="center", 
                                font=("Arial", 16, "bold"))
    
    def check_game_over(self):
        """Display game over screen"""
        self.save_high_score()
        self.update_score()
        game_over = turtle.Turtle()
        game_over.hideturtle()
        game_over.color(COLOR_TEXT)
        game_over.penup()
        game_over.goto(0, 0)
        game_over.write("Game Over!\nPress SPACE to restart", 
                       align="center", 
                       font=("Arial", 24, "bold"))
        self.game_over_msg = game_over
    
    def game_loop(self):
        """Update game state via ontimer"""
        if not self.game_over:
            # Hide start message once game starts
            if self.snake.started and hasattr(self, 'start_message'):
                self.start_message.clear()
                self.start_message.hideturtle()
                # We don't delete it to avoid errors if referenced elsewhere
            
            self.snake.move()
            
            # Check if food is eaten
            if self.snake.eat_food(self.food.position):
                self.score += 10
                # Dynamic difficulty: speed up as score increases
                self.delay = max(0.04, DELAY - (self.score / 500))
                self.update_score()
                self.food.respawn(self.snake.body)
            
            # Check for collisions
            if self.snake.check_collision():
                self.game_over = True
                self.check_game_over()
            
            # Update screen
            self.screen.update()
            
            # Schedule next frame
            self.screen.ontimer(self.game_loop, int(self.delay * 1000))
        else:
            self.screen.update()
    
    def run(self):
        """Start the game loop"""
        self.game_loop()
        self.screen.mainloop()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()