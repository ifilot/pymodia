import drawsvg as draw


def add_background(self):
    """
    Function to add a background
    """
    self.image.append(draw.Rectangle(0, 0, self.width, self.height,
                                     fill=self.background_color))

    return self
