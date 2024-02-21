import os


class MoDiaSettings():
    """
    Class that gathers all settings to draw molecular orbital diagrams
    """

    def __init__(self, **kwargs):

        allowed_settings_file = open(os.path.join(os.path.dirname(__file__),
                                                  'allowed_settings.txt'), "r")
        allowed_settings = allowed_settings_file.read()
        allowed_settings_file.close()

        self.ao1_color = ['#000000']
        self.ao1_labels = ['1s', '2s',
                           '2p', '2p', '2p', '3s', '3p', '3p', '3p']
        self.ao2_color = ['#000000']
        self.ao2_labels = ['1s', '2s',
                           '2p', '2p', '2p', '3s', '3p', '3p', '3p']
        self.ao_round = 3
        self.arrow_color = '#000000'
        self.arrow_head_size = 6
        self.arrow_length = 15
        self.background_color = '#ffffff'
        self.box_color = '#000000'
        self.core_cutoff = -10
        self.core_height = 50
        self.draw_background = True
        self.draw_configuration = True
        self.draw_contributions = True
        self.draw_core_box = True
        self.draw_energy_labels = True
        self.draw_level_labels = False
        self.draw_occupancies = True
        self.draw_orbc = False
        self.energy_scale_color = '#000000'
        self.energy_scale_labels = None
        self.energy_scale_style = 'mo'
        self.font_family = 'Open Sans'
        self.font_size = 10
        self.height = 600
        self.label_significant_digits = 3
        self.level_labels_style = 'ao'
        self.level_width = 55
        self.line_width = 1.5
        self.main_color = '#000000'
        self.margin = 50
        self.mo_color = ['#000000']
        self.mo_labels = None
        self.mo_round = 3
        self.multiplicty_offset = 3
        self.name_color = '#000000'
        self.orbc_color = '#000000'
        self.orbc_cutoff = 0.4
        self.orbc_font_size = 10
        self.orbc_linestyle = '6'
        self.orbc_opacity = 0
        self.outer_height = 400
        self.unit = 'Ht'
        self.width = 550
        self.x_space = 12
        self.x_space_interset = 2

        self.__dict__.update((k, v) for k, v in kwargs.items()
                             if k in allowed_settings)
