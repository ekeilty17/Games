class queue:
  
    def __init__(self):
        self.store = []

    def enq(self, val):
        self.store += [val]

    def deq(self):
        if self.store == []:
            return False
        r = self.store[0]
        self.store = self.store[1:]
        return r
    
    def isEmpty(self):
        if self.store == []:
            return True
        return False

    # Helper functions for body queue
    def getHead(self):
        if self.store == []:
            return None
        return self.store[-1]

    def getTail(self):
        if self.store == []:
            return None
        return self.store[0]

class snake:

    def __init__(self, start_pos, cell_size, display_width, display_height):
        # Display parameteres
        self.width = display_width
        self.height = display_height
        self.cell_size = cell_size
        # info about snake itself
        self.body = queue()
        self.body.enq(start_pos)
        # info about location of food that has been eaten by the snake
        self.food = queue()

        self.prev_direction = [0, 0]
    
    def eat(self, food_pos):
        self.food.enq(food_pos)
    
    def evolve(self, direction):
        
        if self.prev_direction[0] == -1*direction[0] and self.prev_direction[1] == -1*direction[1]:
            direction = self.prev_direction

        head = self.body.getHead()
        x = head[0]
        y = head[1]

        if direction == [-1, 0]:   # left
            self.body.enq([(x - self.cell_size) % self.width, y])
        elif direction == [1, 0]:  # right
            self.body.enq([(x + self.cell_size) % self.width, y])
        elif direction == [0, 1]:  # down
            self.body.enq([x, (y + self.cell_size) % self.height])
        elif direction == [0, -1]: # up
            self.body.enq([x, (y - self.cell_size) % self.height])
        
        self.prev_direction = direction

        if not self.food.isEmpty():
            if self.body.getTail() == self.food.getTail():
                self.food.deq()
                return False
        return self.body.deq()
