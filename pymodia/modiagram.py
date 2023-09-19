import drawsvg as draw
import numpy as np


class PyMoDia():
    """
    Class to draw Molecular Orbital diagrams
    """

    def __init__(self, molecule, molecular_orbital_energies,
                 orbital_coefficients, core_cutoff=-10, width=550, height=600,
                 margin=50, core_height=50, outer_height=400, level_width=55,
                 line_width=1.5, multiplicty_offset=3, font_family='Noto Sans',
                 font_size=10, main_color='#000000', draw_background=True,
                 background_color='#ffffff'):
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
        self.moe = molecular_orbital_energies
        self.orbc = np.transpose(orbital_coefficients)

        self.image = draw.Drawing(self.width, self.height)

        self.image.embed_google_font(font_family)

        if self.draw_background is True:
            self.image.append(draw.Rectangle(0, 0, self.width, self.height,
                                             fill=self.background_color))

        def find_core(self, core_cutoff):
            """
            Determines the core orbitals based on orbital energy and cutoff
            """
            mo_core = [x for x in self.moe if x <= core_cutoff]
            mo_outer = [x for x in self.moe if x > core_cutoff]

            ao1_core = [x for x in self.atom1.energies if x <= core_cutoff]
            ao1_outer = [x for x in self.atom1.energies if x > core_cutoff]

            ao2_core = [x for x in self.atom2.energies if x <= core_cutoff]
            ao2_outer = [x for x in self.atom2.energies if x > core_cutoff]

            return mo_core, mo_outer, ao1_core, ao1_outer, ao2_core, ao2_outer

        def find_locations(self, mo_core, mo_outer, ao1_core, ao1_outer,
                           ao2_core, ao2_outer):
            """
            Finds the locations of the energy levels
            """
            # Finding locations of outer levels
            height_0_outer = self.outer_height + self.margin
            height_0_core = (self.core_height + self.outer_height +
                             2*self.margin)

            # reordering (ro) and scaling (s) orbital levels
            # Molecular orbitals
            ro_mo_outer = [x+abs(min(mo_outer)) for x in mo_outer]
            s_mo_outer = [x/(max(ro_mo_outer)) *
                          self.outer_height for x in ro_mo_outer]
            if len(mo_core) == 1:
                ro_mo_core = [abs(x) for x in mo_core]
                s_mo_core = [x/(max(ro_mo_core))*0.5 *
                             self.core_height for x in ro_mo_core]
            else:
                ro_mo_core = [x+abs(min(mo_core)) for x in mo_core]
                s_mo_core = [x/(max(ro_mo_core)) *
                             self.core_height for x in ro_mo_core]

            # Atomic orbitals
            # Atomic orbital 1
            ro_ao1_outer = [x+abs(min(mo_outer)) for x in ao1_outer]
            s_ao1_outer = [x/(max(ro_mo_outer)) *
                           self.outer_height for x in ro_ao1_outer]
            if len(mo_core) == 1:
                ro_ao1_core = [abs(x) for x in ao1_core]
                s_ao1_core = [x/(max(ro_mo_core))*0.5 *
                              self.core_height for x in ro_ao1_core]
            else:
                ro_ao1_core = [x+abs(min(mo_core)) for x in ao1_core]
                s_ao1_core = [x/(max(ro_mo_core)) *
                              self.core_height for x in ro_ao1_core]

            if self.molecule.nr_a1 > 1:
                s_ao1_outer = s_ao1_core*self.molecule.nr_a1
                s_ao1_outer = s_ao1_outer*self.molecule.nr_a1

            # Atomic orbital 2
            ro_ao2_outer = [x+abs(min(mo_outer)) for x in ao2_outer]
            s_ao2_outer = [x/(max(ro_mo_outer)) *
                           self.outer_height for x in ro_ao2_outer]
            if len(mo_core) == 1:
                ro_ao2_core = [abs(x) for x in ao2_core]
                s_ao2_core = [x/(max(ro_mo_core))*0.5 *
                              self.core_height for x in ro_ao2_core]
            else:
                ro_ao2_core = [x+abs(min(mo_core)) for x in ao2_core]
                s_ao2_core = [x/(max(ro_mo_core)) *
                              self.core_height for x in ro_ao2_core]

            if self.molecule.nr_a2 > 1:
                s_ao2_core = s_ao2_core*self.molecule.nr_a2
                s_ao2_outer = s_ao2_outer*self.molecule.nr_a2

            def location_dictonary(self, loct_dict, s_orbe, column, h0):
                """
                Makes dictionary with x and y begin and end coordinates
                """
                if column == 'mo':
                    orbe_x_start = [0.5*self.width+0.5*self.margin -
                                    0.5*self.level_width for x in s_orbe]
                    orbe_x_end = [0.5*self.width+0.5*self.margin +
                                  0.5*self.level_width for x in s_orbe]
                if column == 'ao1':
                    orbe_x_start = [2*self.margin for x in s_orbe]
                    orbe_x_end = [2*self.margin +
                                  self.level_width for x in s_orbe]
                if column == 'ao2':
                    orbe_x_start = [self.width -
                                    (self.margin + self.level_width)
                                    for x in s_orbe]
                    orbe_x_end = [self.width - self.margin for x in s_orbe]

                orbe_heights = [h0-x for x in s_orbe]

                def append_loct_dict(loct_dict, orbe_x_start, orbe_x_end,
                                     orbe_heights,
                                     orbe_multiplicity_heights=orbe_heights):
                    [loct_dict['xb'].append(xb) for xb in orbe_x_start]
                    [loct_dict['xe'].append(xe) for xe in orbe_x_end]
                    [loct_dict['yb'].append(yb) for yb in orbe_heights]
                    [loct_dict['ye'].append(ye) for ye in orbe_heights]
                    [loct_dict['ymb'].append(ymb)
                     for ymb in orbe_multiplicity_heights]
                    [loct_dict['yme'].append(yme)
                     for yme in orbe_multiplicity_heights]
                    return loct_dict

                # Solving the overlapping multiplicity
                # (only doing it for the outer levels)
                unique_used = []
                unique_levels = [x for x in orbe_heights if x not in
                                 unique_used and
                                 (unique_used.append(x) or True)]
                occurance = []
                [occurance.append(orbe_heights.count(x))
                 for x in unique_levels]

                i = 0
                orbe_multiplicity_heights = [0]*len(orbe_heights)

                for o in occurance:
                    if o == 1:
                        orbe_multiplicity_heights[i] = orbe_heights[i]

                        i = i+1
                    if o == 2:
                        orbe_multiplicity_heights[i] = orbe_heights[i] - \
                            0.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+1] = orbe_heights[i] + \
                            0.5*self.multiplicty_offset
                        i = i+2
                    if o == 3:
                        orbe_multiplicity_heights[i] = orbe_heights[i] - \
                            self.multiplicty_offset
                        orbe_multiplicity_heights[i+1] = orbe_heights[i]
                        orbe_multiplicity_heights[i+2] = orbe_heights[i] + \
                            self.multiplicty_offset
                        i = i+3
                    if o == 4:
                        orbe_multiplicity_heights[i] = orbe_heights[i] - \
                            1.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                            0.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+2] = orbe_heights[i] + \
                            0.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                            1.5*self.multiplicty_offset
                        i = i+4
                    if o == 5:
                        orbe_multiplicity_heights[i] = orbe_heights[i] - \
                            2*self.multiplicty_offset
                        orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                            self.multiplicty_offset
                        orbe_multiplicity_heights[i+2] = orbe_heights[i]
                        orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                            self.multiplicty_offset
                        orbe_multiplicity_heights[i+4] = orbe_heights[i] + \
                            2*self.multiplicty_offset
                        i = i+5
                    if o == 6:
                        orbe_multiplicity_heights[i] = orbe_heights[i] - \
                            2.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                            1.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+2] = orbe_heights[i] - \
                            0.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                            0.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+4] = orbe_heights[i] + \
                            1.5*self.multiplicty_offset
                        orbe_multiplicity_heights[i+5] = orbe_heights[i] + \
                            2.5*self.multiplicty_offset
                        i = i+6

                loct_dict = append_loct_dict(
                    loct_dict, orbe_x_start, orbe_x_end, orbe_heights,
                    orbe_multiplicity_heights)

                return loct_dict

            mo_loc = {'xb': [], 'yb': [], 'xe': [],
                      'ye': [], 'ymb': [], 'yme': []}
            mo_loc = location_dictonary(
                self, mo_loc, s_mo_core, 'mo', height_0_core)
            mo_loc = location_dictonary(
                self, mo_loc, s_mo_outer, 'mo', height_0_outer)
            ao1_loc = {'xb': [], 'yb': [], 'xe': [],
                       'ye': [], 'ymb': [], 'yme': []}
            ao1_loc = location_dictonary(
                self, ao1_loc, s_ao1_core, 'ao1', height_0_core)
            ao1_loc = location_dictonary(
                self, ao1_loc, s_ao1_outer, 'ao1', height_0_outer)
            ao2_loc = {'xb': [], 'yb': [], 'xe': [],
                       'ye': [], 'ymb': [], 'yme': []}
            ao2_loc = location_dictonary(
                self, ao2_loc, s_ao2_core, 'ao2', height_0_core)
            ao2_loc = location_dictonary(
                self, ao2_loc, s_ao2_outer, 'ao2', height_0_outer)

            return mo_loc, ao1_loc, ao2_loc

        # Finding locations of MOs and AOs
        mo_core, mo_outer, ao1_core, ao1_outer, ao2_core, ao2_outer = \
            find_core(self, core_cutoff)
        mo_loc, ao1_loc, ao2_loc = \
            find_locations(self, mo_core, mo_outer, ao1_core, ao1_outer,
                           ao2_core, ao2_outer)

        self.mo_core = mo_core
        self.mo_loc = mo_loc
        self.ao1_loc = ao1_loc
        self.ao2_loc = ao2_loc

    def draw_levels(self, colors_mo='main color', colors_ao1='main color',
                    colors_ao2='main color', draw_atom_names=True,
                    draw_core_box=True, draw_configuration=True,
                    atom_font_size=14):
        """
        Draws the atomic and molecular orbital energy levels and their names
        """
        # change base colors of levels to main color
        if colors_mo == 'main color':
            colors_mo = [self.color]
        if colors_ao1 == 'main color':
            colors_ao1 = [self.color]
        if colors_ao2 == 'main color':
            colors_ao2 = [self.color]

        def draw_level(self, loc_dict, colors):
            """
            Draws energy levels based on a location library and colors
            """
            if len(colors) == 1:
                for j in range(len(loc_dict['xb'])):
                    self.image.append(draw.Line(loc_dict['xb'][j],
                                                loc_dict['ymb'][j],
                                                loc_dict['xe'][j],
                                                loc_dict['yme'][j],
                                                stroke=colors[0],
                                                stroke_width=self.line_width))
            else:
                for j in range(len(loc_dict['xb'])):
                    self.image.append(draw.Line(loc_dict['xb'][j],
                                                loc_dict['ymb'][j],
                                                loc_dict['xe'][j],
                                                loc_dict['yme'][j],
                                                stroke=colors[j],
                                                stroke_width=self.line_width))

        # Drawing MOs and AOs with multiplicty
        draw_level(self, self.mo_loc, colors_mo)
        draw_level(self, self.ao1_loc, colors_ao1)
        draw_level(self, self.ao2_loc, colors_ao2)

        # Drawing atom and molecule names
        if draw_atom_names is True:
            if self.molecule.nr_a1 == 1:
                self.image.append(draw.Text(
                    self.atom1.name, atom_font_size,
                    (2*self.margin+0.5*self.level_width),
                    (self.height-0.5*self.margin), center=True,
                    font_family=self.font_family, fill=self.color))
            else:
                self.image.append(draw.Text(
                    (str(self.molecule.nr_a1)+"x"+self.atom1.name),
                    atom_font_size, (2*self.margin + 0.5*self.level_width),
                    (self.height-0.5*self.margin), center=True,
                    font_family=self.font_family, fill=self.color))
            if self.molecule.nr_a2 == 1:
                self.image.append(draw.Text(
                    self.atom2.name, atom_font_size,
                    (self.width-(self.margin+0.5 * self.level_width)),
                    (self.height-0.5*self.margin), center=True,
                    font_family=self.font_family, fill=self.color))
            else:
                self.image.append(draw.Text(
                    (str(self.molecule.nr_a2)+"x"+self.atom2.name),
                    atom_font_size, (self.width-(self.margin+0.5 *
                                                 self.level_width)),
                    (self.height-0.5*self.margin), center=True,
                    font_family=self.font_family, fill=self.color))
            self.image.append(draw.Text(
                self.molecule.name, atom_font_size,
                (0.5*self.width+0.5*self.margin),
                (self.height-0.5*self.margin), center=True,
                font_family=self.font_family, fill=self.color))

        # Drawing box around core
        if len(self.mo_core) != 0:
            if draw_core_box is True:
                self.image.append(draw.Rectangle(
                    (2*self.margin-20),
                    (self.height-self.margin-self.core_height-23),
                    (self.width-3*self.margin+40),
                    (self.core_height+37), fill_opacity=0, stroke=self.color))

        # Draw configuration
        if draw_configuration is True:
            self.image.append(draw.Text(self.atom1.configuration,
                                        self.font_size,
                                        (2*self.margin+0.5 * self.level_width),
                                        (self.height-0.25*self.margin),
                                        center=True,
                                        font_family=self.font_family,
                                        fill=self.color))
            self.image.append(draw.Text(self.atom2.configuration,
                                        self.font_size,
                                        (self.width -
                                         (self.margin + 0.5*self.level_width)),
                                        (self.height-0.25*self.margin),
                                        center=True,
                                        font_family=self.font_family,
                                        fill=self.color))

        return self

    def draw_occupancies(self, arrow_head_size=6, x_space=12,
                         x_space_interset=2, arrow_length=15,
                         color='main color'):
        """
        Draws the occupancy of energy levels with either harpoon or arrow
        symbols
        """
        if color == 'main color':
            color = self.color

        arrow = draw.Marker(-0.2, -0.4, 0.6, 0.4,
                            scale=arrow_head_size, orient='auto')
        arrow.append(draw.Lines(-0.2, 0.4, 0, 0, -0.2, -0.4, 0.6, 0,
                                fill=color, close=True))

        def draw_arrow_set(self, x, y):
            self.image.append(draw.Line(x-x_space_interset,
                                        y+7/12*arrow_length,
                                        x-x_space_interset,
                                        y-5/12*arrow_length,
                                        stroke=color, marker_end=arrow))
            self.image.append(draw.Line(x+x_space_interset,
                                        y-8/12*arrow_length,
                                        x+x_space_interset,
                                        y+4/12*arrow_length,
                                        stroke=color, marker_end=arrow))

        def draw_arrow_single(self, x, y):
            self.image.append(draw.Line(x, y+7/12*arrow_length,
                                        x, y-5/12*arrow_length,
                                        stroke=color, marker_end=arrow))

        def draw_occupancy(self, level_loc_x, level_loc_y, nr_elec, nr_levels):
            if nr_elec == 2*nr_levels:
                # sets of fully filled levels
                if nr_levels == 1:
                    draw_arrow_set(self, level_loc_x, level_loc_y)
                elif nr_levels == 2:
                    draw_arrow_set(self, level_loc_x+0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-0.5*x_space, level_loc_y)
                elif nr_levels == 3:
                    draw_arrow_set(self, level_loc_x+x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x, level_loc_y)
                    draw_arrow_set(self, level_loc_x-x_space, level_loc_y)
                elif nr_levels == 4:
                    draw_arrow_set(self, level_loc_x+1.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x+0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-1.5*x_space, level_loc_y)
            elif nr_elec <= nr_levels:
                # only partial occupied levels
                if nr_elec == 1:
                    draw_arrow_single(self, level_loc_x, level_loc_y)
                elif nr_elec == 2:
                    draw_arrow_single(self, level_loc_x +
                                      0.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x -
                                      0.5*x_space, level_loc_y)
                elif nr_levels == 3:
                    draw_arrow_single(self, level_loc_x+x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x, level_loc_y)
                    draw_arrow_single(self, level_loc_x-x_space, level_loc_y)
                elif nr_levels == 4:
                    draw_arrow_single(self, level_loc_x +
                                      1.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x +
                                      0.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x -
                                      0.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x -
                                      1.5*x_space, level_loc_y)
            elif nr_elec == nr_levels+1:
                if nr_elec == 3:
                    draw_arrow_single(self, level_loc_x +
                                      0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-0.5*x_space, level_loc_y)
                elif nr_elec == 4:
                    draw_arrow_single(self, level_loc_x+x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x, level_loc_y)
                    draw_arrow_set(self, level_loc_x-x_space, level_loc_y)
                elif nr_levels == 5:
                    draw_arrow_single(self, level_loc_x +
                                      1.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x +
                                      0.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x -
                                      0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-1.5*x_space, level_loc_y)
            elif nr_elec == nr_levels+2:
                if nr_elec == 5:
                    draw_arrow_single(self, level_loc_x+x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x, level_loc_y)
                    draw_arrow_set(self, level_loc_x-x_space, level_loc_y)
                elif nr_levels == 5:
                    draw_arrow_single(self, level_loc_x +
                                      1.5*x_space, level_loc_y)
                    draw_arrow_single(self, level_loc_x +
                                      0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-1.5*x_space, level_loc_y)
            elif nr_elec == nr_levels+3:
                if nr_levels == 7:
                    draw_arrow_single(self, level_loc_x +
                                      1.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x+0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-0.5*x_space, level_loc_y)
                    draw_arrow_set(self, level_loc_x-1.5*x_space, level_loc_y)

        # Drawing the occupancies
        ao1_e_count = self.atom1.atomic_number*self.molecule.nr_a1
        ao2_e_count = self.atom2.atomic_number*self.molecule.nr_a2
        mo_e_count = ao1_e_count + ao2_e_count

        for e in range(len(self.ao1_loc['ye'])):
            nr_levels = self.ao1_loc['ye'].count(self.ao1_loc['ye'][e])
            if ((self.ao1_loc['ye'][e] == self.ao1_loc['yme'][e]) or
                (self.ao1_loc['ye'][e] ==
                 (self.ao1_loc['yme'][e]-0.5*self.multiplicty_offset))):
                if ao1_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = ao1_e_count

                draw_occupancy(self, (2*self.margin+0.5*self.level_width),
                               self.ao1_loc['ye'][e], nr_e, nr_levels)
                ao1_e_count = ao1_e_count - nr_e

        for e in range(len(self.ao2_loc['ye'])):
            nr_levels = self.ao2_loc['ye'].count(self.ao2_loc['ye'][e])
            if ((self.ao2_loc['ye'][e] == self.ao2_loc['yme'][e]) or
                (self.ao2_loc['ye'][e] ==
                 (self.ao2_loc['yme'][e]-0.5*self.multiplicty_offset))):
                if ao2_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = ao2_e_count

                draw_occupancy(self,
                               (self.width-(self.margin+0.5*self.level_width)),
                               self.ao2_loc['ye'][e], nr_e, nr_levels)
                ao2_e_count = ao2_e_count - nr_e

        for e in range(len(self.mo_loc['ye'])):
            nr_levels = self.mo_loc['ye'].count(self.mo_loc['ye'][e])
            if ((self.mo_loc['ye'][e] == self.mo_loc['yme'][e]) or
                (self.mo_loc['ye'][e] ==
                 (self.mo_loc['yme'][e]-0.5*self.multiplicty_offset))):
                if mo_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels

                else:
                    nr_e = mo_e_count

                draw_occupancy(self, (0.5*self.width+0.5*self.margin),
                               self.mo_loc['ye'][e], nr_e, nr_levels)
                mo_e_count = mo_e_count - nr_e

        return self

    def draw_contributions(self, abs_cutoff=0.4, print_coeff=False, opacity=0,
                           linestyle='6', color='main color'):
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

        return self

    def draw_labels(self, labels_mo=[], style='mo',
                    labels_ao1=['1s', '2s', '2p', '2p',
                                '2p', '3s', '3p', '3p', '3p'],
                    labels_ao2=['1s', '2s', '2p', '2p', '2p',
                                '3s', '3p', '3p', '3p']):
        """
        Adds labels to atomic and molecular orbitals
        """
        color = self.color

        def draw_mo_labels(self, labels):
            label_memory = []
            y_memory = []
            x = self.mo_loc['xe'][0]

            for j in range(len(self.mo_loc['xb'])):
                label = draw.Text(labels[j],
                                  self.font_size,
                                  x, self.mo_loc['ymb'][j]+10,
                                  center=True, text_anchor='end',
                                  font_family=self.font_family, fill=color)
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

        def draw_ao1_labels(self, labels):
            label_memory = []
            x = self.ao1_loc['xb'][0]-2
            for j in range(len(self.ao1_loc['xb'])):
                label = draw.Text(labels[j],
                                  self.font_size,
                                  x, self.ao1_loc['yb'][j],
                                  center=True, text_anchor='end',
                                  font_family=self.font_family, fill=color)
                label_memory.append(label)
                if label_memory.count(label) == 1:
                    self.image.append(label)

        def draw_ao2_labels(self, labels):
            label_memory = []
            x = self.ao2_loc['xe'][0]+2
            for j in range(len(self.ao2_loc['xb'])):
                label = draw.Text(labels[j],
                                  self.font_size,
                                  x, self.ao2_loc['yb'][j],
                                  center=True, text_anchor='begin',
                                  font_family=self.font_family, fill=color)
                label_memory.append(label)
                if label_memory.count(label) == 1:
                    self.image.append(label)

        if style == 'mo':
            draw_mo_labels(self, labels_mo)
        elif style == 'mo_ao':
            draw_mo_labels(self, labels_mo)
            draw_ao1_labels(self, labels_ao1)
            draw_ao2_labels(self, labels_ao2)
        elif style == 'ao':
            draw_ao1_labels(self, labels_ao1)
            draw_ao2_labels(self, labels_ao2)
        else:
            print(
                "This is not a valid style for the energy scale."
                " Valid styles include 'mo', 'mo_ao' and 'ao'")

        return self

    def draw_energy_scale(self, style='mo', significant_digits=2, labels=None,
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
            print("Other units are not yet implemented")

        def draw_energy_labels(self, loc_dict, labels, core=None):
            text_memory = []
            x = self.margin - 4
            for j in range(len(loc_dict['xb'])):
                t = draw.Text(str(round(labels[j], significant_digits)),
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
                    if (round(labels[j], significant_digits) >=
                            self.core_cutoff and text_memory.count(t) == 1):
                        self.image.append(t)
                        self.image.append(draw.Line(self.margin,
                                                    loc_dict['yb'][j], x+1,
                                                    loc_dict['yb'][j],
                                                    stroke=self.color))

        if style == 'mo':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                draw_energy_labels(self, self.mo_loc, labels, core=True)
            else:
                draw_energy_labels(self, self.mo_loc, self.moe, core=True)
        elif style == 'mo_ao':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                draw_energy_labels(self, self.mo_loc, labels[0], core=True)
                draw_energy_labels(self, self.ao1_loc, labels[1])
                draw_energy_labels(self, self.ao2_loc, labels[2])
            else:
                draw_energy_labels(self, self.mo_loc, self.moe, core=True)
                draw_energy_labels(self, self.ao1_loc, self.atom1.energies)
                draw_energy_labels(self, self.ao2_loc, self.atom2.energies)
        elif style == 'ao':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                draw_energy_labels(self, self.ao1_loc, labels[0], core=True)
                draw_energy_labels(self, self.ao2_loc, labels[1], core=True)
            else:
                draw_energy_labels(self, self.ao1_loc,
                                   self.atom1.energies, core=True)
                draw_energy_labels(self, self.ao2_loc,
                                   self.atom2.energies, core=True)
        else:
            print(
                "This is not a valid style for the energy scale."
                " Valid styles include 'mo', 'mo_ao' and 'ao'")

        return self
