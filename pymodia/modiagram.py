import drawsvg as draw
import numpy as np


class PyMoDia():
    """
    Class to draw Molecular Orbital diagrams
    """

    def __init__(self, data: modiadata = None, settings: modiasettings = None,
                 style: modiastyle = None):

        # import data object
        if data:
            self.data = data

        # import settings object
        if settings:
            self.settings = settings

        # import style object
        if style:
            self.style = style

        molecular_orbital_energies,

        orbital_coefficients,

        font_size = 10
        main_color = '#000000'

        mo_round = 5
        ao_round = 5

        self.core_cutoff = core_cutoff
        self.width = width
        self.height = height
        self.margin = margin
        self.core_height = core_height
        self.outer_height = outer_height
        self.level_width = level_width
        self.line_width = line_width
        self.multiplicty_offset = multiplicty_offset
        self.font_family = font_family
        self.font_size = font_size
        self.color = main_color
        self.draw_background = draw_background
        self.background_color = background_color

        self.molecule = molecule
        self.atom1 = molecule.a1
        self.atom2 = molecule.a2
        self.orbc = np.transpose(orbital_coefficients)

        # _______________________________ #

        self.data.moe
        self.data.name
        self.data.atom1.name
        self.data.atom2.name
        self.data.atom1.e
        self.data.atom2.e
        self.data.atom1.nr
        self.data.atom2.nr

        self.settings.core_cutoff = -10
        self.settings.width = 550
        self.settings.height = 600
        self.settings.core_height = 50
        self.settings.outer_height = 400
        self.settings.margin = 50
        self.settings.level_width = 55
        self.settings.line_width = 55
        self.settings.multiplicty_offset = 3
        self.settings.draw_background = True
        self.settings.draw_core_box = True
        self.settings.draw_occupancies = True
        self.settings.draw_energy_labels = True
        self.settings.draw_level_labels = False

        self.style.main_color = "#000000"
        self.style.font_family = "Noto Sans"
        self.style.background_color = "#ffffff"
        self.style.name_color = "#000000"  # name of atoms and molecule
        self.style.arrow_color = "#000000"
        self.style.arrow_length = 15
        self.style.x_space = 12
        self.style.x_space_interset = 2

        self.style.mo_color = [self.style.main_color]
        self.style.ao2_color = [self.style.main_color]
        self.style.ao2_color = [self.style.main_color]

    def draw(self):
        """
        Draws the mo diagram according to the settings of the object

        """
        # initialise image
        self.image = draw.Drawing(self.settings.width, self.settings.height)

        # embed from google
        self.image.embed_google_font(self.style.font_family)

        # add background
        if self.settings.draw_background:
            self.image.append(draw.Rectangle(0, 0, self.settings.width,
                                             self.settings.height,
                                             fill=self.style.background_color))

        # find locations to draw levels
        self.__find_core()
        self.__find_locations()

        # adding levels
        self.__draw_levels()

        # adding atom/molecule information at bottom diagram
        self.__draw_names()
        self.__draw_configuration()

        # add box around core orbitals
        if self.settings.draw_core_box:
            self.__draw_box()

        # add occupancies to drawn levels
        if self.settings.draw_occupancies:
            self.__draw_occupancies()

        # add energy
        if self.settings.draw_energy_labels:
            self.__draw_energy_scale()
            self.__draw_energy_labels()

        # add labelling to levels
        if self.settings.draw_level_labels:
            self.__draw_level_labels()

        return self

    def export_svg(self, filepath: str):
        """
        Draws the mo diagram according to the setting of the object and exports
        to an svg file

        Parameters
        ----------
        filepath : str
            path to save image to

        """

        self.draw()

        self.image.save_svg(filepath)

        return self

    def __find_core(self):
        """
        Determines the core orbitals based on orbital energy and cutoff
        """
        moe = self.data.moe
        ao1 = self.data.atom1.e
        ao2 = self.data.atom2.e
        core_cutoff = self.settings.core_cutoff

        self.__mo_core = [x for x in moe if x <= core_cutoff]
        self.__mo_outer = [x for x in moe if x > core_cutoff]

        self.__ao1_core = [x for x in ao1 if x <= core_cutoff]
        self.__ao1_outer = [x for x in ao1 if x > core_cutoff]

        self.__ao2_core = [x for x in ao2 if x <= core_cutoff]
        self.__ao2_outer = [x for x in ao2 if x > core_cutoff]

    def __find_locations(self):
        """
        Finds the locations of the energy levels
        """
        outer_height = self.settings.outer_height
        core_height = self.settings.core_height
        margin = self.settings.margin

        nr_a1 = self.data.atom1.nr
        nr_a2 = self.data.atom2.nr

        mo_core = self.__mo_core
        ao1_core = self.__ao1_core
        ao2_core = self.__ao2_core

        mo_outer = self.__mo_outer
        ao1_outer = self.__ao1_outer
        ao2_outer = self.__ao2_outer

        # Finding lowest core orbital
        if len(mo_core) >= 1:
            lwst_mo_c = min(mo_core)
            lwst_ao1_c = min(ao1_core)
            lwst_ao2_c = min(ao2_core)
            lwst_core = min([lwst_mo_c, lwst_ao1_c, lwst_ao2_c])

        # Finding lowest outer orbital
        lwst_mo_o = min(mo_outer)
        lwst_ao1_o = min(ao1_outer)
        lwst_ao2_o = min(ao2_outer)
        lwst_outer = min([lwst_mo_o, lwst_ao1_o, lwst_ao2_o])

        # Finding locations of outer levels
        height_0_outer = outer_height + margin
        height_0_core = (core_height + outer_height + 2*margin)

        # reordering (ro) and scaling (s) orbital levels
        # Molecular orbitals
        ro_mo_outer = [x+abs(lwst_outer) for x in mo_outer]
        s_mo_outer = [x/(max(ro_mo_outer)) * outer_height for x in ro_mo_outer]
        if len(mo_core) == 1:
            ro_mo_core = [abs(x) for x in mo_core]
            s_mo_core = [x/(max(ro_mo_core)) * 0.5 * core_height for x in
                         ro_mo_core]
        else:
            ro_mo_core = [x+abs(lwst_core) for x in mo_core]
            s_mo_core = [x/(max(ro_mo_core)) * core_height for x in ro_mo_core]

        # Atomic orbitals
        # Atomic orbital 1
        ro_ao1_outer = [x+abs(lwst_outer) for x in ao1_outer]
        s_ao1_outer = [x/(max(ro_mo_outer)) * outer_height for x in
                       ro_ao1_outer]
        if len(mo_core) == 1:
            ro_ao1_core = [abs(x) for x in ao1_core]
            s_ao1_core = [x/(max(ro_mo_core)) * 0.5 * core_height for x in
                          ro_ao1_core]
        else:
            ro_ao1_core = [x+abs(lwst_core) for x in ao1_core]
            s_ao1_core = [x/(max(ro_mo_core)) * core_height for x in
                          ro_ao1_core]

        if nr_a1 > 1:
            s_ao1_core = s_ao1_core*nr_a1
            s_ao1_outer = s_ao1_outer*nr_a1

        # Atomic orbital 2
        ro_ao2_outer = [x+abs(lwst_outer) for x in ao2_outer]
        s_ao2_outer = [x/(max(ro_mo_outer)) * outer_height for x in
                       ro_ao2_outer]
        if len(mo_core) == 1:
            ro_ao2_core = [abs(x) for x in ao2_core]
            s_ao2_core = [x/(max(ro_mo_core)) * 0.5 * core_height for x in
                          ro_ao2_core]
        else:
            ro_ao2_core = [x+abs(lwst_core) for x in ao2_core]
            s_ao2_core = [x/(max(ro_mo_core)) * core_height for x in
                          ro_ao2_core]

        if nr_a2 > 1:
            s_ao2_core = s_ao2_core*nr_a2
            s_ao2_outer = s_ao2_outer*nr_a2

        # making dictonaries
        empty_loc_dic = {'xb': [], 'yb': [], 'xe': [], 'ye': [], 'ymb': [],
                         'yme': []}
        mo_loc = empty_loc_dic
        mo_loc = self.__location_dictonary(mo_loc, s_mo_core, 'mo',
                                           height_0_core)
        mo_loc = self.__location_dictonary(mo_loc, s_mo_outer, 'mo',
                                           height_0_outer)

        ao1_loc = empty_loc_dic
        ao1_loc = self.__location_dictonary(ao1_loc, s_ao1_core, 'ao1',
                                            height_0_core)
        ao1_loc = self.__location_dictonary(ao1_loc, s_ao1_outer, 'ao1',
                                            height_0_outer)

        ao2_loc = empty_loc_dic
        ao2_loc = self.__location_dictonary(ao2_loc, s_ao2_core, 'ao2',
                                            height_0_core)
        ao2_loc = self.__location_dictonary(ao2_loc, s_ao2_outer, 'ao2',
                                            height_0_outer)

        self.__mo_loc = mo_loc
        self.__ao1_loc = ao1_loc
        self.__ao2_loc = ao2_loc

    def __location_dictonary(self, loct_dict, s_orbe, column, h0):
        """
        Makes dictionary with x and y begin and end coordinates
        """
        width = self.settings.width
        level_width = self.settings.level_width
        margin = self.settings.margin
        multiplicty_offset = self.settings.multiplicty_offset

        if column == 'mo':
            orbe_x_start = [0.5*width + 0.5*margin - 0.5*level_width for x in
                            s_orbe]
            orbe_x_end = [0.5*width + 0.5*margin + 0.5*level_width for x in
                          s_orbe]
        if column == 'ao1':
            orbe_x_start = [2*margin for x in s_orbe]
            orbe_x_end = [2*margin + level_width for x in s_orbe]
        if column == 'ao2':
            orbe_x_start = [width - (margin + level_width) for x in s_orbe]
            orbe_x_end = [width - margin for x in s_orbe]

        orbe_heights = [h0-x for x in s_orbe]

        # Solving the overlapping multiplicity
        # (only doing it for the outer levels)
        unique_used = []
        unique_levels = [x for x in orbe_heights if x not in unique_used and
                         (unique_used.append(x) or True)]
        occurance = []
        [occurance.append(orbe_heights.count(x)) for x in unique_levels]

        i = 0
        orbe_multiplicity_heights = [0]*len(orbe_heights)

        for o in occurance:
            if o == 1:
                orbe_multiplicity_heights[i] = orbe_heights[i]

                i = i+1
            if o == 2:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i] + \
                    0.5*multiplicty_offset
                i = i+2
            if o == 3:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i]
                orbe_multiplicity_heights[i+2] = orbe_heights[i] + \
                    multiplicty_offset
                i = i+3
            if o == 4:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    1.5*multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+2] = orbe_heights[i] + \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                    1.5*multiplicty_offset
                i = i+4
            if o == 5:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    2*multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                    multiplicty_offset
                orbe_multiplicity_heights[i+2] = orbe_heights[i]
                orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                    multiplicty_offset
                orbe_multiplicity_heights[i+4] = orbe_heights[i] + \
                    2*multiplicty_offset
                i = i+5
            if o == 6:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    2.5*multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                    1.5*multiplicty_offset
                orbe_multiplicity_heights[i+2] = orbe_heights[i] - \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+4] = orbe_heights[i] + \
                    1.5*multiplicty_offset
                orbe_multiplicity_heights[i+5] = orbe_heights[i] + \
                    2.5*multiplicty_offset
                i = i+6

        loct_dict = self.__append_loct_dict(
            loct_dict, orbe_x_start, orbe_x_end, orbe_heights,
            orbe_multiplicity_heights)

        return loct_dict

    def __append_loct_dict(loct_dict, orbe_x_start, orbe_x_end,
                           orbe_heights,
                           orbe_multiplicity_heights):
        """
        Appends location dictonary
        """
        [loct_dict['xb'].append(xb) for xb in orbe_x_start]
        [loct_dict['xe'].append(xe) for xe in orbe_x_end]
        [loct_dict['yb'].append(yb) for yb in orbe_heights]
        [loct_dict['ye'].append(ye) for ye in orbe_heights]
        [loct_dict['ymb'].append(ymb)
         for ymb in orbe_multiplicity_heights]
        [loct_dict['yme'].append(yme)
         for yme in orbe_multiplicity_heights]

        return loct_dict

    def __draw_levels(self):
        """
        Draws the atomic and molecular orbital energy levels
        """
        colors_mo = self.style.mo_color
        colors_ao1 = self.style.ao2_color
        colors_ao2 = self.style.ao2_color

        # Drawing MOs and AOs with multiplicty
        self.__draw_level(self.__mo_loc, colors_mo)
        self.__draw_level(self.__ao1_loc, colors_ao1)
        self.__draw_level(self.__ao2_loc, colors_ao2)

    def __draw_level(self, loc_dict, colors):
        """
        Draws energy levels based on a location library and colors
        """
        line_width = self.settings.line_width

        if len(colors) == 1:
            if isinstance(colors, list):
                for j in range(len(loc_dict['xb'])):
                    self.image.append(draw.Line(loc_dict['xb'][j],
                                                loc_dict['ymb'][j],
                                                loc_dict['xe'][j],
                                                loc_dict['yme'][j],
                                                stroke=colors[0],
                                                stroke_width=line_width))
            elif isinstance(colors, str):
                for j in range(len(loc_dict['xb'])):
                    self.image.append(draw.Line(loc_dict['xb'][j],
                                                loc_dict['ymb'][j],
                                                loc_dict['xe'][j],
                                                loc_dict['yme'][j],
                                                stroke=colors,
                                                stroke_width=line_width))
        else:
            if len(colors) < len(loc_dict['xb']):
                raise ValueError(
                    "Insufficient colors specified. Need at least %i colors."
                    % len(loc_dict['xb']))

            for j in range(len(loc_dict['xb'])):
                self.image.append(draw.Line(loc_dict['xb'][j],
                                            loc_dict['ymb'][j],
                                            loc_dict['xe'][j],
                                            loc_dict['yme'][j],
                                            stroke=colors[j],
                                            stroke_width=line_width))

    def __draw_names(self, names_font_size=14):
        """
        Adds atom and molecules names/labels
        """
        name_mol = self.data.name
        name_a1 = self.data.atom1.name
        name_a2 = self.data.atom2.name
        nr_a1 = self.data.atom1.nr
        nr_a2 = self.data.atom2.nr

        height = self.settings.height
        width = self.settings.width
        margin = self.settings.margin
        level_width = self.settings.level_width

        font_family = self.style.font_family
        color = self.style.name_color

        if nr_a1 == 1:
            self.image.append(draw.Text(
                name_a1, names_font_size,
                (2*margin + 0.5*level_width),
                (height-0.5*margin), center=True,
                font_family=font_family, fill=color))
        else:
            self.image.append(draw.Text(
                (str(nr_a1) + "x" + name_a1),
                names_font_size, (2*margin + 0.5*level_width),
                (height - 0.5*margin), center=True,
                font_family=font_family, fill=color))

        if nr_a2 == 1:
            self.image.append(draw.Text(
                name_a2, names_font_size,
                (width - (margin + 0.5*level_width)),
                (height - 0.5*margin), center=True,
                font_family=font_family, fill=color))
        else:
            self.image.append(draw.Text(
                (str(nr_a2) + "x" + name_a2),
                names_font_size, (width - (margin + 0.5*level_width)),
                (height - 0.5*margin), center=True,
                font_family=font_family, fill=color))

        self.image.append(draw.Text(
            name_mol, names_font_size, (0.5*width + 0.5*margin),
            (height - 0.5*margin), center=True, font_family=font_family,
            fill=color))

    def __draw_configuration(self, configuration_font_size=12):
        """
        Adds configuration of atoms to diagram
        """
        config_a1 = self.data.atom1.configuration
        config_a2 = self.data.atom2.configuration

        height = self.settings.height
        width = self.settings.width
        margin = self.settings.margin
        level_width = self.settings.level_width

        font_family = self.style.font_family
        color = self.style.name_color

        self.image.append(draw.Text(config_a1,
                                    configuration_font_size,
                                    (2*margin + 0.5 * level_width),
                                    (height - 0.25*margin),
                                    center=True,
                                    font_family=font_family,
                                    fill=color))
        self.image.append(draw.Text(config_a2,
                                    configuration_font_size,
                                    (width - (margin + 0.5*level_width)),
                                    (height - 0.25*margin),
                                    center=True,
                                    font_family=font_family,
                                    fill=color))

    def __draw_box(self):
        """
        Adds box arround core
        """
        mo_core = self.__mo_core

        height = self.settings.height
        width = self.settings.width
        core_height = self.settings.core_height
        margin = self.settings.margin

        color = self.style.main_color

        if len(mo_core) != 0:
            self.image.append(draw.Rectangle(
                (2*margin - 20),
                (height - margin - core_height - 23),
                (width - 3*margin+40),
                (core_height + 37), fill_opacity=0, stroke=color))
        else:
            raise Exception("no box around core drawn, no level in core")

    def __draw_occupancies(self, arrow_head_size=6,
                           arrow_color='main color'):
        """
        Draws the occupancy of energy levels with either arrow symbols
        """
        anr_a1 = self.data.atom1.atomic_number
        anr_a2 = self.data.atom2.atomic_number
        nr_a1 = self.data.atom1.nr
        nr_a2 = self.data.atom2.nr

        ao1_loc = self.__ao1_loc
        ao2_loc = self.__ao2_loc
        mo_loc = self.__mo_loc

        width = self.settings.width
        margin = self.settings.margin
        level_width = self.settings.level_width
        multiplicty_offset = self.settings.multiplicty_offset

        # making arrow
        arrow_color = self.style.arrow_color
        arrow = draw.Marker(-0.2, -0.4, 0.6, 0.4,
                            scale=arrow_head_size, orient='auto')
        arrow.append(draw.Lines(-0.2, 0.4, 0, 0, -0.2, -0.4, 0.6, 0,
                                fill=arrow_color, close=True))
        self.__arrow = arrow

        # Drawing the occupancies
        ao1_e_count = anr_a1 * nr_a1
        ao2_e_count = anr_a2 * nr_a2
        mo_e_count = ao1_e_count + ao2_e_count

        # atom 1 levels
        for e in range(len(ao1_loc['ye'])):
            nr_levels = ao1_loc['ye'].count(ao1_loc['ye'][e])
            if (ao1_loc['ye'][e] == ao1_loc['yme'][e]) or ((ao1_loc['ye'][e]) == (ao1_loc['yme'][e]-0.5*multiplicty_offset)):
                if ao1_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = ao1_e_count

                self.__draw_occupancy((2*margin + 0.5*level_width),
                                      ao1_loc['ye'][e], nr_e, nr_levels)
                ao1_e_count = ao1_e_count - nr_e

        # atom 2 levels
        for e in range(len(ao2_loc['ye'])):
            nr_levels = ao2_loc['ye'].count(ao2_loc['ye'][e])
            if ((ao2_loc['ye'][e] == ao2_loc['yme'][e]) or
                (ao2_loc['ye'][e] ==
                 (ao2_loc['yme'][e]-0.5*multiplicty_offset))):
                if ao2_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = ao2_e_count

                self.__draw_occupancy((width - (margin+0.5*level_width)),
                                      ao2_loc['ye'][e], nr_e, nr_levels)
                ao2_e_count = ao2_e_count - nr_e

        # mo levels
        for e in range(len(mo_loc['ye'])):
            nr_levels = mo_loc['ye'].count(mo_loc['ye'][e])
            if ((mo_loc['ye'][e] == mo_loc['yme'][e]) or
                (mo_loc['ye'][e] ==
                 (mo_loc['yme'][e]-0.5*multiplicty_offset))):
                if mo_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = mo_e_count

                self.__draw_occupancy((0.5*width+0.5*margin),
                                      mo_loc['ye'][e], nr_e, nr_levels)
                mo_e_count = mo_e_count - nr_e

    def __draw_occupancy(self, level_loc_x, level_loc_y, nr_elec, nr_levels):
        """
        Draws the occupancy of energy (multiplicity) level(s) based on nr_elec
        and nr_levels
        """
        if nr_elec <= 0:
            # do nothing
            pass
        elif nr_elec == 2*nr_levels:
            # sets of fully filled levels
            if nr_levels == 1:
                self.__draw_arrow_set(self, level_loc_x, level_loc_y)
            elif nr_levels == 2:
                self.__draw_arrow_set(
                    self, level_loc_x+0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-0.5*self.__x_space, level_loc_y)
            elif nr_levels == 3:
                self.__draw_arrow_set(
                    self, level_loc_x+self.__x_space, level_loc_y)
                self.__draw_arrow_set(self, level_loc_x, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-self.__x_space, level_loc_y)
            elif nr_levels == 4:
                self.__draw_arrow_set(
                    self, level_loc_x+1.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x+0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-1.5*self.__x_space, level_loc_y)
        elif nr_elec <= nr_levels:
            # only partial occupied levels
            if nr_elec == 1:
                self.__draw_arrow_single(self, level_loc_x, level_loc_y)
            elif nr_elec == 2:
                self.__draw_arrow_single(self, level_loc_x +
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x -
                                         0.5*self.__x_space, level_loc_y)
            elif nr_levels == 3:
                self.__draw_arrow_single(
                    self, level_loc_x+self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x, level_loc_y)
                self.__draw_arrow_single(
                    self, level_loc_x-self.__x_space, level_loc_y)
            elif nr_levels == 4:
                self.__draw_arrow_single(self, level_loc_x +
                                         1.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x +
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x -
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x -
                                         1.5*self.__x_space, level_loc_y)
        elif nr_elec == nr_levels+1:
            if nr_elec == 3:
                self.__draw_arrow_single(self, level_loc_x +
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-0.5*self.__x_space, level_loc_y)
            elif nr_elec == 4:
                self.__draw_arrow_single(
                    self, level_loc_x+self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-self.__x_space, level_loc_y)
            elif nr_levels == 5:
                self.__draw_arrow_single(self, level_loc_x +
                                         1.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x +
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x -
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-1.5*self.__x_space, level_loc_y)
        elif nr_elec == nr_levels+2:
            if nr_elec == 5:
                self.__draw_arrow_single(
                    self, level_loc_x+self.__x_space, level_loc_y)
                self.__draw_arrow_set(self, level_loc_x, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-self.__x_space, level_loc_y)
            elif nr_levels == 5:
                self.__draw_arrow_single(self, level_loc_x +
                                         1.5*self.__x_space, level_loc_y)
                self.__draw_arrow_single(self, level_loc_x +
                                         0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-1.5*self.__x_space, level_loc_y)
        elif nr_elec == nr_levels+3:
            if nr_levels == 7:
                self.__draw_arrow_single(self, level_loc_x +
                                         1.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x+0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-0.5*self.__x_space, level_loc_y)
                self.__draw_arrow_set(
                    self, level_loc_x-1.5*self.__x_space, level_loc_y)

    def __draw_arrow_set(self, x, y):
        """
        Adds an arrow set (one up one down) at location x,y
        """
        x_space_interset = self.style.x_space_interset
        arrow = self.__arrow
        arrow_color = self.style.arrow_color
        arrow_length = self.style.arrow_length

        self.image.append(draw.Line(x - x_space_interset,
                                    y + 7/12*arrow_length,
                                    x - x_space_interset,
                                    y - 5/12*arrow_length,
                                    stroke=arrow_color,
                                    marker_end=arrow))
        self.image.append(draw.Line(x + x_space_interset,
                                    y - 8/12*arrow_length,
                                    x + x_space_interset,
                                    y + 4/12*arrow_length,
                                    stroke=arrow_color,
                                    marker_end=arrow))

    def __draw_arrow_single(self, x, y, color):
        """
        Adds an single arrow (one up) at location x,y
        """
        arrow = self.__arrow
        arrow_color = self.style.arrow_color
        arrow_length = self.style.arrow_length

        self.image.append(draw.Line(x, y + 7/12*arrow_length,
                                    x, y - 5/12*arrow_length,
                                    stroke=arrow_color,
                                    marker_end=arrow))

    def __draw_contributions(self, abs_cutoff=0.4, print_coeff=False,
                             opacity=0, linestyle='6', color='main color'):
        """
        Draws the contributions of the different atomic orbitals to the
        molecular orbitals
        """
        path_memory = []

        if color == 'main color':
            color = self.color

        for i in range(len(self.orbc[0])):
            for j in range(len(self.orbc[0])):
                if abs(self.orbc[i][j]) >= abs_cutoff:

                    ao1_end_index = len(self.ao1_loc['xb'])-1
                    ao1_len = len(self.ao1_loc['xb'])

                    if (j <= ao1_end_index):
                        p = draw.Line(self.ao1_loc['xe'][j],
                                      self.ao1_loc['ye'][j],
                                      self.mo_loc['xb'][i],
                                      self.mo_loc['yb'][i], stroke=color,
                                      fill_opacity=opacity,
                                      stroke_dasharray=linestyle)
                        path_memory.append(p)
                        if path_memory.count(p) == 1:
                            self.image.append(p)

                        if print_coeff is True:
                            str_coeffs = [str(round(c, 2))
                                          for c in self.orbc[i]]
                            if path_memory.count(p) == 1:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=-0.4, fill=color))
                            elif path_memory.count(p) == 2:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=1, fill=color))
                            elif path_memory.count(p) == 3:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=2, fill=color))
                            elif path_memory.count(p) == 4:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=-1.4, fill=color))
                    elif (j > ao1_end_index):
                        p = draw.Line(self.mo_loc['xe'][i],
                                      self.mo_loc['ye'][i],
                                      self.ao2_loc['xb'][j-ao1_len],
                                      self.ao2_loc['yb'][j-ao1_len],
                                      stroke=color, fill_opacity=opacity,
                                      stroke_dasharray=linestyle)
                        path_memory.append(p)
                        if path_memory.count(p) == 1:
                            self.image.append(p)

                        if print_coeff is True:
                            str_coeffs = [str(round(c, 2))
                                          for c in self.orbc[i]]
                            if path_memory.count(p) == 1:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=-0.4, fill=color))
                            elif path_memory.count(p) == 2:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=1, fill=color))
                            elif path_memory.count(p) == 3:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=2, fill=color))
                            elif path_memory.count(p) == 4:
                                self.image.append(draw.Text(
                                    str_coeffs[j], self.font_size, path=p,
                                    text_anchor='middle',
                                    font_family=self.font_family,
                                    line_offset=-1.4, fill=color))

    def __draw_energy_scale(self, style='mo', labels=None,
                            unit='Hartree'):
        """
        Draws the energy scale with energy labels

        There are different styles:
            - mo : only molecular orbital labels
            - mo_ao : both molecular and atomic orbital labls
            - ao : only atomic orbitals labels
        """

        # Drawing the bar itself
        arrow = draw.Marker(-0.3, -0.4, 0.6, 0.4, scale=10, orient='auto')
        arrow.append(draw.Lines(-0.3, 0.4, 0, 0, -0.3, -0.4, 0.6, 0,
                                fill=self.color, close=True))
        self.image.append(draw.Line(self.margin, self.height-self.margin+14,
                                    self.margin, 0.5*self.margin,
                                    stroke=self.color, marker_end=arrow))

        # Adding energy and unit to bar
        self.image.append(draw.Text('Energy', self.font_size,
                                    3, 20,
                                    center=True, text_anchor='begin',
                                    font_family=self.font_family,
                                    fill=self.color))
        if unit == 'Hartree':
            self.image.append(draw.Text('(Hartree)', self.font_size,
                                        3, 35,
                                        center=True, text_anchor='begin',
                                        font_family=self.font_family,
                                        fill=self.color))
        else:
            raise NotImplementedError("Other units are not yet implemented")

    def __draw_energy_labels(self, labels, style='mo', significant_digits=2):
        """
        Adds energy labels to energy scale
        """
        self.__significant_digits = significant_digits

        if style == 'mo':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                self.__draw_energy_labels(self, self.mo_loc, labels, core=True)
            else:
                self.__draw_energy_labels(
                    self, self.mo_loc, self.moe, core=True)

        elif style == 'mo_ao':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                self.__draw_energy_labels(
                    self, self.mo_loc, labels[0], core=True)
                self.__draw_energy_labels(self, self.ao1_loc, labels[1])
                self.__draw_energy_labels(self, self.ao2_loc, labels[2])
            else:
                if self.molecule.nr_a1 > 1:
                    atom1_energies = self.atom1.energies*self.molecule.nr_a1
                else:
                    atom1_energies = self.atom1.energies
                if self.molecule.nr_a2 > 1:
                    atom2_energies = self.atom2.energies*self.molecule.nr_a2
                else:
                    atom2_energies = self.atom2.energies
                self.__draw_energy_labels(
                    self, self.mo_loc, self.moe, core=True)
                self.__draw_energy_labels(self, self.ao1_loc, atom1_energies)
                self.__draw_energy_labels(self, self.ao2_loc, atom2_energies)

        elif style == 'ao':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                self.__draw_energy_labels(
                    self, self.ao1_loc, labels[0], core=True)
                self.__draw_energy_labels(
                    self, self.ao2_loc, labels[1], core=True)
            else:
                if self.molecule.nr_a1 > 1:
                    atom1_energies = self.atom1.energies*self.molecule.nr_a1
                else:
                    atom1_energies = self.atom1.energies
                if self.molecule.nr_a2 > 1:
                    atom2_energies = self.atom2.energies*self.molecule.nr_a2
                else:
                    atom2_energies = self.atom2.energies
                self.__draw_energy_labels(self, self.ao1_loc,
                                          self.atom1.energies, core=True)
                self.__draw_energy_labels(self, self.ao2_loc,
                                          self.atom2.energies, core=True)
        else:
            raise Exception("An invalid style for energy lables, valid styles"
                            " include 'mo', 'mo_ao' and 'ao'")

    def __draw_energy_label(self, loc_dict, labels, core=False):
        """
        Adds energy labels to energy scale
        """
        text_memory = []
        x = self.margin - 4
        for j in range(len(loc_dict['xb'])):
            t = draw.Text(str(round(labels[j], self.__significant_digits)),
                          self.font_size,
                          x, loc_dict['yb'][j],
                          center=True, text_anchor='end',
                          font_family=self.font_family, fill=self.color)
            text_memory.append(t)
            if core:
                if text_memory.count(t) == 1:
                    self.image.append(t)
                    self.image.append(draw.Line(self.margin,
                                                loc_dict['yb'][j], x+1,
                                                loc_dict['yb'][j],
                                                stroke=self.color))
            else:
                if (round(labels[j], self.__significant_digits) >=
                        self.core_cutoff and text_memory.count(t) == 1):
                    self.image.append(t)
                    self.image.append(draw.Line(self.margin,
                                                loc_dict['yb'][j], x+1,
                                                loc_dict['yb'][j],
                                                stroke=self.color))

    def __draw_level_labels(self, labels_mo=[], style='mo',
                            labels_ao1=['1s', '2s', '2p', '2p',
                                        '2p', '3s', '3p', '3p', '3p'],
                            labels_ao2=['1s', '2s', '2p', '2p', '2p',
                                        '3s', '3p', '3p', '3p']):
        """
        Adds labels to atomic and molecular orbitals
        """
        if style == 'mo':
            self.__draw_mo_labels(self, labels_mo)
        elif style == 'mo_ao':
            self.__draw_mo_labels(self, labels_mo)
            self.__draw_ao1_labels(self, labels_ao1)
            self.__draw_ao2_labels(self, labels_ao2)
        elif style == 'ao':
            self.__draw_ao1_labels(self, labels_ao1)
            self.__draw_ao2_labels(self, labels_ao2)
        else:
            raise Exception("An invalid style for lables, valid styles include"
                            " 'mo', 'mo_ao' and 'ao'")

    def __draw_mo_labels(self, labels):
        """
        Adds labels to molecular orbitals
        """
        label_memory = []
        y_memory = []
        x = self.mo_loc['xe'][0]

        for j in range(len(self.mo_loc['xb'])):
            label = draw.Text(labels[j],
                              self.font_size,
                              x, self.mo_loc['ymb'][j]+10,
                              center=True, text_anchor='end',
                              font_family=self.font_family, fill=self.color)
            label_memory.append(label)
            y = self.mo_loc['yb'][j]
            y_memory.append(y)

        unique_y = []
        for y in y_memory:
            if y not in unique_y:
                unique_y.append(y)

        for y in unique_y:
            if y_memory.count(y) == 1:
                self.image.append(label_memory[y_memory.index(y)])
            if y_memory.count(y) == 2:
                self.image.append(label_memory[y_memory.index(y)])
            if y_memory.count(y) == 3:
                self.image.append(label_memory[y_memory.index(y)+1])
            if y_memory.count(y) == 4:
                self.image.append(label_memory[y_memory.index(y)+1])

    def __draw_ao1_labels(self, labels):
        """
        Adds labels to atomic orbitals of atom 1
        """
        label_memory = []
        x = self.ao1_loc['xb'][0]-2
        for j in range(len(self.ao1_loc['xb'])):
            label = draw.Text(labels[j],
                              self.font_size,
                              x, self.ao1_loc['yb'][j],
                              center=True, text_anchor='end',
                              font_family=self.font_family, fill=self.color)
            label_memory.append(label)
            if label_memory.count(label) == 1:
                self.image.append(label)

    def __draw_ao2_labels(self, labels):
        """
        Adds labels to atomic orbitals of atom 2
        """
        label_memory = []
        x = self.ao2_loc['xe'][0]+2
        for j in range(len(self.ao2_loc['xb'])):
            label = draw.Text(labels[j],
                              self.font_size,
                              x, self.ao2_loc['yb'][j],
                              center=True, text_anchor='begin',
                              font_family=self.font_family, fill=self.color)
            label_memory.append(label)
            if label_memory.count(label) == 1:
                self.image.append(label)
