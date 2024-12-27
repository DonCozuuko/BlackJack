

class Button():
    def __init__(self, image, pos, text_input, font, base_colour, hovering_colour):
        self.image = image
        self.x_pos = pos[0] #Assuming the inputted pos attribute is pg.mouse.get_pos()
        self.y_pos = pos[1]
        self.font = font
        self.base_colour, self.hovering_colour = base_colour, hovering_colour
        self.text_input = text_input
        if self.text_input != None:
            self.text = self.font.render(self.text_input, True, base_colour)
            self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if not self.image == None and not self.text_input == None:
            screen.blit(self.image, self.rect)
            screen.blit(self.text, self.text_rect)
        elif self.image == None and not self.text_input == None:
            screen.blit(self.text, self.text_rect)
        elif not self.image == None and self.text_input == None:
            screen.blit(self.image, self.rect)
        

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColour(self, position):
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_colour)
        else:
            self.text = self.font.render(self.text_input, True, self.base_colour)
