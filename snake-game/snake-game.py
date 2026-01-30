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
    
    def add_segment(self, position):
        """Add a segment to the snake"""
        segment = turtle.Turtle()
        segment.shape("square")
        segment.color("green")
        segment.penup()
        segment.goto(position)
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
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.setup(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.title("Snake Game")
        self.screen.tracer(0)  # Disable animation (manual update)
        
        # Score display
        self.score = 0
        self.score_display = turtle.Turtle()
        self.score_display.hideturtle()
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.goto(0, WINDOW_HEIGHT//2 - 40)
        
        # Initialize game objects
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.game_over = False
        
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
        self.screen.onkey(lambda: self.snake.change_direction(UP), "Up")
        self.screen.onkey(lambda: self.snake.change_direction(DOWN), "Down")
        self.screen.onkey(lambda: self.snake.change_direction(LEFT), "Left")
        self.screen.onkey(lambda: self.snake.change_direction(RIGHT), "Right")
        self.screen.onkey(lambda: self.snake.change_direction(UP), "w")
        self.screen.onkey(lambda: self.snake.change_direction(DOWN), "s")
        self.screen.onkey(lambda: self.snake.change_direction(LEFT), "a")
        self.screen.onkey(lambda: self.snake.change_direction(RIGHT), "d")
        self.screen.onkey(self.reset_game, "space")
    
    def reset_game(self):
        """Reset the game"""
        # Clear existing objects
        if hasattr(self, 'snake') and self.snake:
            for segment in self.snake.segments:
                segment.hideturtle()
                segment.clear()
            self.snake.segments.clear()
        
        if hasattr(self, 'food') and self.food:
            self.food.food.hideturtle()
            self.food.food.clear()
        
        if hasattr(self, 'start_message'):
            self.start_message.clear()
            self.start_message.hideturtle()
        
        # Clear screen
        self.screen.clear()
        self.screen.bgcolor("black")
        self.screen.tracer(0)
        
        # Create new game objects
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.score = 0
        self.game_over = False
        
        # Recreate score display
        self.score_display = turtle.Turtle()
        self.score_display.hideturtle()
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.goto(0, WINDOW_HEIGHT//2 - 40)
        
        self.setup_keys()
        self.update_score()
        self.show_start_message()
        self.screen.update()
    
    def update_score(self):
        """Update score display"""
        self.score_display.clear()
        self.score_display.write(f"Score: {self.score}", 
                                align="center", 
                                font=("Arial", 16, "bold"))
    
    def check_game_over(self):
        """Display game over screen"""
        game_over = turtle.Turtle()
        game_over.hideturtle()
        game_over.color("white")
        game_over.penup()
        game_over.goto(0, 0)
        game_over.write("Game Over!\nPress SPACE to restart", 
                       align="center", 
                       font=("Arial", 24, "bold"))
        self.game_over_msg = game_over
    
    def run(self):
        """Main game loop"""
        while True:
            if not self.game_over:
                # Hide start message once game starts
                if self.snake.started and hasattr(self, 'start_message'):
                    self.start_message.clear()
                    self.start_message.hideturtle()
                    delattr(self, 'start_message')
                
                self.snake.move()
                
                # Check if food is eaten
                if self.snake.eat_food(self.food.position):
                    self.score += 10
                    self.update_score()
                    self.food.respawn(self.snake.body)
                
                # Check for collisions
                if self.snake.check_collision():
                    self.game_over = True
                    self.check_game_over()
                
                # Update screen
                self.screen.update()
                time.sleep(DELAY)
            else:
                self.screen.update()
                time.sleep(0.1)
        
        self.screen.mainloop()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()