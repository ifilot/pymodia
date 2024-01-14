class MoDiaStyle():
    """
    Class that combines the style elements used to draw molecular orbital
    diagrams
    """

    def __init__(self, **kwargs):

        allowed_style = {'font_size', 'font_family', 'arrow_length', 'x_space',
                         'x_space_interset', 'orbc_opacity',
                         'orbc_linestyle', 'orbc_font_size',
                         'arrow_head_size', 'background_color',
                         'main_color', 'name_color', 'arrow_color',
                         'orbc_color', 'box_color', 'energy_scale_color',
                         'mo_color', 'ao1_color', 'ao2_color',
                         'level_labels_style', 'mo_labels', 'ao1_labels',
                         'ao2_labels'}
        self.__dict__.update((k, v) for k, v in kwargs.items()
                             if k in allowed_style)

        self.font_size = 10
        self.font_family = "Noto Sans"
        self.arrow_length = 15
        self.x_space = 12
        self.x_space_interset = 2
        self.orbc_opacity = 0
        self.orbc_linestyle = '6'
        self.orbc_font_size = 10
        self.arrow_head_size = 6
        self.background_color = "#ffffff"
        self.main_color = "#000000"
        self.name_color = "#000000"
        self.arrow_color = "#000000"
        self.orbc_color = "#000000"
        self.box_color = "#000000"
        self.energy_scale_color = "#000000"

        self.mo_color = ["#000000"]
        self.ao1_color = ["#000000"]
        self.ao2_color = ["#000000"]
