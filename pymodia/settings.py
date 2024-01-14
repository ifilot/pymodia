class MoDiaSettings():
    """
    Class that gathers all settings to draw molecular orbital diagrams
    """

    def __init__(self, **kwargs):

        allowed_settings = {'core_cutoff', 'orbc_cutoff', 'width', 'height',
                            'core_height', 'outer_height', 'margin',
                            'level_width', 'line_width', 'multiplicity_offset',
                            'mo_round', 'ao_round', 'draw_background',
                            'draw_core_box', 'draw_occupancies',
                            'draw_energy_labels', 'draw_level_labels',
                            'draw_configuration', 'draw_orbc',
                            'energy_scale_style', 'energy_scale_labels',
                            'unit', 'label_significant_digits'}
        self.__dict__.update((k, v) for k, v in kwargs.items()
                             if k in allowed_settings)

        self.core_cutoff = -10
        self.orbc_cutoff = 0.4
        self.width = 550
        self.height = 600
        self.core_height = 50
        self.outer_height = 400
        self.margin = 50
        self.level_width = 55
        self.line_width = 1.5
        self.multiplicty_offset = 3
        self.mo_round = 3
        self.ao_round = 3
        self.draw_background = True
        self.draw_core_box = True
        self.draw_occupancies = True
        self.draw_energy_labels = False
        self.draw_level_labels = False
        self.draw_configuration = False
        self.draw_orbc = False
        self.energy_scale_style = 'mo'
        self.energy_scale_labels = None
        self.unit = 'Hartree'
        self.level_labels_style = 'ao'
        self.mo_labels = None
        self.ao1_labels = ['1s', '2s',
                           '2p', '2p', '2p', '3s', '3p', '3p', '3p']
        self.ao2_labels = ['1s', '2s',
                           '2p', '2p', '2p', '3s', '3p', '3p', '3p']
        self.label_significant_digits = 3
