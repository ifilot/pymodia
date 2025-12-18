import drawsvg as draw
import numpy as np
import os

from typing import Any, Optional
from .data import MoDiaData
from .settings import MoDiaSettings

class MoDia:
    """
    Class responsible for constructing and rendering molecular orbital (MO)
    diagrams using MoDia data containers and visualization settings.
    """

    def __init__(
        self,
        data: MoDiaData,
        **kwargs: Any,
    ) -> None:
        """
        Initialize an MO diagram.

        Parameters
        ----------
        data
            MoDiaData object containing molecular and fragment information
            required to construct the MO diagram.
        settings
            Optional MoDiaSettings object controlling visual appearance
            (colors, cutoffs, rounding, etc.). If not provided, default
            settings are used.
        **kwargs
            Additional keyword arguments used to override specific diagram
            options or settings at initialization time.
        """

        # import data object
        if data:
            self.data = data

        # import settings object
        if 'settings' in kwargs:
            self.settings = kwargs['settings']
        else:
            self.settings = MoDiaSettings()

        # changing settings via kwargs
        allowed_settings_file = open(os.path.join(os.path.dirname(__file__),
                                                  'allowed_settings.txt'), "r")
        allowed_settings = allowed_settings_file.read()
        allowed_settings_file.close()

        self.settings.__dict__.update((k, v) for k, v in kwargs.items()
                                      if k in allowed_settings)

        # rounding energies
        self.data.moe = [round(moe, self.settings.mo_round) for moe
                         in self.data.molecule.state_energies]
        self.data.fragment1.e = [round(e, self.settings.ao_round) for e
                                 in self.data.fragment1.state_energies]
        self.data.fragment2.e = [round(e, self.settings.ao_round) for e
                                 in self.data.fragment2.state_energies]

    def draw(self):
        """
        Draws the mo diagram according to the settings of the object

        """
        font_family = self.settings.font_family

        # initialise image
        self.image = draw.Drawing(
            self.settings.width, self.settings.height, font_family=font_family)

        # embed font from google
        imprt_symbs = "1234567890 ₀₁₂₃₄₅₆₇₈₉ ⁰¹²³⁴⁵⁶⁷⁸⁹\
            ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdsefghiklmnopqrstuvwxyz\
                σ π *"
        self.image.embed_google_font(font_family, text=imprt_symbs)

        # add background
        if self.settings.draw_background:
            self.image.append(draw.Rectangle(0, 0, self.settings.width,
                                             self.settings.height,
                                             fill=self.settings.background_color))

        # find locations to draw levels
        self.__find_core()
        self.__find_locations()
        # print(self.__ao2_loc)

        # adding levels
        self.__draw_levels()

        # adding atom/molecule information at bottom diagram
        self.__draw_names()
        if self.settings.draw_configuration:
            self.__draw_sublabel()

        # add box around core orbitals
        if self.settings.draw_core_box:
            self.__draw_box()

        # add occupancies to drawn levels
        self.__draw_occupancies()

        # draw orbc lines:
        if self.settings.draw_contributions:
            self.__draw_contributions()

        # add energy labels
        self.__draw_energy_scale()
        if self.settings.draw_energy_labels:
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
        ao1 = self.data.fragment1.e
        ao2 = self.data.fragment2.e
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

        nr_a1 = 1
        nr_a2 = 1

        mo_core = self.__mo_core
        ao1_core = self.__ao1_core
        ao2_core = self.__ao2_core
        core_energies = mo_core + ao1_core + ao2_core

        mo_outer = self.__mo_outer
        ao1_outer = self.__ao1_outer
        ao2_outer = self.__ao2_outer

        # Notifying user
        if nr_a1 >= 2 and self.data.fragment1.name != "H":
            print('Number of fragments 1 >= 2, only one set of atomic orbtials is drawn')
        if nr_a2 >= 2 and self.data.fragment2.name != "H":
            print('Number of fragments 2 >= 2, only one set of atomic orbtials is drawn')

        # core scaling
        if len(core_energies) > 0:
            emin = min(core_energies)
            emax = max(core_energies)
            
            # prevent collapse for nearly-degenerate cores
            if abs(emax - emin) < 1e-6:
                emax = emin + 1e-6
        
        def scale_core(e):
            return (e - emin) / (emax - emin) * core_height

        # Finding lowest outer orbital
        lwst_mo_o = min(mo_outer)
        lwst_ao1_o = min(ao1_outer)
        lwst_ao2_o = min(ao2_outer)
        lwst_outer = min([lwst_mo_o, lwst_ao1_o, lwst_ao2_o])

        # Finding locations of outer levels
        height_0_outer = outer_height + margin
        height_0_core = (core_height + outer_height + 2 * margin)

        # reordering (ro) and scaling (s) orbital levels
        # Molecular orbitals
        ro_mo_outer = [x+abs(lwst_outer) for x in mo_outer]
        s_mo_outer = [x/(max(ro_mo_outer)) * outer_height for x in ro_mo_outer]
        s_mo_core  = [scale_core(e) for e in mo_core]

        # Atomic orbitals
        # ---------------
        # Atomic orbital 1
        ro_ao1_outer = [x+abs(lwst_outer) for x in ao1_outer]
        s_ao1_outer = [x/(max(ro_mo_outer)) * outer_height for x in
                       ro_ao1_outer]
                       
        s_ao1_core = [scale_core(e) for e in ao1_core]

        if nr_a1 > 1:
            s_ao1_core = s_ao1_core*nr_a1
            s_ao1_outer = s_ao1_outer*nr_a1

        # Atomic orbital 2
        ro_ao2_outer = [x+abs(lwst_outer) for x in ao2_outer]
        s_ao2_outer = [x/(max(ro_mo_outer)) * outer_height for x in
                       ro_ao2_outer]
                       
        s_ao2_core = [scale_core(e) for e in ao2_core]

        if nr_a2 > 1:
            s_ao2_core = s_ao2_core*nr_a2
            s_ao2_outer = s_ao2_outer*nr_a2

        # making dictonaries
        mo_loc = {'xb': [], 'yb': [], 'xe': [], 'ye': [], 'ymb': [],
                  'yme': []}
        mo_loc = self.__location_dictonary(mo_loc, s_mo_core, 'mo',
                                           height_0_core)
        mo_loc = self.__location_dictonary(mo_loc, s_mo_outer, 'mo',
                                           height_0_outer)

        ao1_loc = {'xb': [], 'yb': [], 'xe': [], 'ye': [], 'ymb': [],
                   'yme': []}
        ao1_loc = self.__location_dictonary(ao1_loc, s_ao1_core, 'ao1',
                                            height_0_core)
        ao1_loc = self.__location_dictonary(ao1_loc, s_ao1_outer, 'ao1',
                                            height_0_outer)

        ao2_loc = {'xb': [], 'yb': [], 'xe': [], 'ye': [], 'ymb': [],
                   'yme': []}
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

        nr_a1 = 1
        nr_a2 = 1

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

        if column == 'ao1' and nr_a1 >= 2 and self.data.fragment1.name != "H":
            occurance = [int(occ/nr_a1) for occ in occurance]
        if column == 'ao2' and nr_a2 >= 2 and self.data.fragment2.name != "H":
            occurance = [int(occ/nr_a1) for occ in occurance]

        for o in occurance:
            if o == 1:
                orbe_multiplicity_heights[i] = orbe_heights[i]

                i = i+1
            elif o == 2:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i] + \
                    0.5*multiplicty_offset
                i = i+2
            elif o == 3:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i]
                orbe_multiplicity_heights[i+2] = orbe_heights[i] + \
                    multiplicty_offset
                i = i+3
            elif o == 4:
                orbe_multiplicity_heights[i] = orbe_heights[i] - \
                    1.5*multiplicty_offset
                orbe_multiplicity_heights[i+1] = orbe_heights[i] - \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+2] = orbe_heights[i] + \
                    0.5*multiplicty_offset
                orbe_multiplicity_heights[i+3] = orbe_heights[i] + \
                    1.5*multiplicty_offset
                i = i+4
            elif o == 5:
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
            elif o == 6:
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
            elif o > 6:
                # print('Multiplicity > 6 not supported, one level drawn')
                orbe_multiplicity_heights[i] = orbe_heights[i]
                i = i+1

        loct_dict = self.__append_loct_dict(loct_dict, orbe_x_start,
                                            orbe_x_end, orbe_heights,
                                            orbe_multiplicity_heights)

        return loct_dict

    def __append_loct_dict(self, loct_dict, orbe_x_start, orbe_x_end,
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
        colors_mo = self.settings.mo_color
        colors_ao1 = self.settings.ao1_color
        colors_ao2 = self.settings.ao2_color

        mo_loc = self.__mo_loc
        ao1_loc = self.__ao1_loc
        ao2_loc = self.__ao2_loc

        # Drawing MOs and AOs with multiplicty
        self.__draw_level(mo_loc, colors_mo)
        self.__draw_level(ao1_loc, colors_ao1)
        self.__draw_level(ao2_loc, colors_ao2)

    def __draw_level(self, loc_dict, colors):
        """
        Draws energy levels based on a location library and colors
        """
        line_width = self.settings.line_width

        if len(colors) == 1:
            if isinstance(colors, list):
                for j in range(len(loc_dict['xb'])):
                    if loc_dict['ymb'][j] == 0:
                        pass
                    else:
                        self.image.append(draw.Line(loc_dict['xb'][j],
                                                    loc_dict['ymb'][j],
                                                    loc_dict['xe'][j],
                                                    loc_dict['yme'][j],
                                                    stroke=colors[0],
                                                    stroke_width=line_width))
            elif isinstance(colors, str):
                for j in range(len(loc_dict['xb'])):
                    if loc_dict['ymb'][j] == 0:
                        pass
                    else:
                        self.image.append(draw.Line(loc_dict['xb'][j],
                                                    loc_dict['ymb'][j],
                                                    loc_dict['xe'][j],
                                                    loc_dict['yme'][j],
                                                    stroke=colors,
                                                    stroke_width=line_width))
        else:
            if len(colors) < len(loc_dict['xb']):
                raise ValueError(
                    'Insufficient colors specified. Need at least %i colors.'
                    % len(loc_dict['xb']))

            for j in range(len(loc_dict['xb'])):
                if loc_dict['ymb'][j] == 0:
                    pass
                else:
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
        name_mol = self.data.molecule.name
        name_a1 = self.data.fragment1.name
        name_a2 = self.data.fragment2.name
        nr_a1 = 1
        nr_a2 = 1

        height = self.settings.height
        width = self.settings.width
        margin = self.settings.margin
        level_width = self.settings.level_width

        color = self.settings.name_color

        if nr_a1 == 1:
            self.image.append(draw.Text(
                name_a1, names_font_size,
                (2*margin + 0.5*level_width),
                (height-0.5*margin), center=True, fill=color))
        else:
            self.image.append(draw.Text(
                (str(nr_a1) + 'x' + name_a1),
                names_font_size, (2*margin + 0.5*level_width),
                (height - 0.5*margin), center=True, fill=color))

        if nr_a2 == 1:
            self.image.append(draw.Text(
                name_a2, names_font_size,
                (width - (margin + 0.5*level_width)),
                (height - 0.5*margin), center=True, fill=color))
        else:
            self.image.append(draw.Text(
                (str(nr_a2) + 'x' + name_a2),
                names_font_size, (width - (margin + 0.5*level_width)),
                (height - 0.5*margin), center=True, fill=color))

        self.image.append(draw.Text(
            name_mol, names_font_size, (0.5*width + 0.5*margin),
            (height - 0.5*margin), center=True, fill=color))

    def __draw_sublabel(self, configuration_font_size=12):
        """
        Adds configuration of atoms to diagram
        """
        height = self.settings.height
        width = self.settings.width
        margin = self.settings.margin
        level_width = self.settings.level_width

        color = self.settings.name_color

        if self.data.fragment1.sublabel is not None:
            self.image.append(draw.Text(self.data.fragment1.sublabel,
                                        configuration_font_size,
                                        (2*margin + 0.5 * level_width),
                                        (height - 0.25*margin),
                                        center=True, fill=color))
        
        if self.data.fragment2.sublabel is not None:
            self.image.append(draw.Text(self.data.fragment2.sublabel,
                                        configuration_font_size,
                                        (width - (margin + 0.5*level_width)),
                                        (height - 0.25*margin),
                                        center=True, fill=color))

    def __draw_box(self):
        """
        Adds box arround core
        """
        mo_core = self.__mo_core

        height = self.settings.height
        width = self.settings.width
        core_height = self.settings.core_height
        margin = self.settings.margin

        color = self.settings.box_color

        if len(mo_core) != 0:
            self.image.append(draw.Rectangle(
                (2*margin - 20),
                (height - margin - core_height - 23),
                (width - 3*margin+40),
                (core_height + 37), fill_opacity=0, stroke=color))
        else:
            print('no box around core drawn, no level in core')

    def __draw_occupancies(self):
        """
        Draws the occupancy of energy levels with either arrow symbols
        """
        nr_a1 = 1
        nr_a2 = 1

        ao1_loc = self.__ao1_loc
        ao2_loc = self.__ao2_loc
        mo_loc = self.__mo_loc

        width = self.settings.width
        margin = self.settings.margin
        level_width = self.settings.level_width
        multiplicty_offset = self.settings.multiplicty_offset

        # making arrow
        arrow_color = self.settings.arrow_color
        arrow_head_size = self.settings.arrow_head_size
        arrow = draw.Marker(-0.2, -0.4, 0.6, 0.4,
                            scale=arrow_head_size, orient='auto')
        arrow.append(draw.Lines(-0.2, 0.4, 0, 0, -0.2, -0.4, 0.6, 0,
                                fill=arrow_color, close=True))
        self.__arrow = arrow

        # Drawing the occupancies
        ao1_e_count = self.data.fragment1.nelec
        ao2_e_count = self.data.fragment2.nelec
        mo_e_count = self.data.molecule.nelec

        # atom 1 levels
        for e in range(len(ao1_loc['ye'])):
            if nr_a1 >= 2 and self.data.fragment1.name != "H":
                nr_levels = int(ao1_loc['ye'].count(ao1_loc['ye'][e])/nr_a1)
            else:
                nr_levels = ao1_loc['ye'].count(ao1_loc['ye'][e])

            if ((ao1_loc['ye'][e] == ao1_loc['yme'][e]) or
                (ao1_loc['ye'][e] ==
                 (ao1_loc['yme'][e]-0.5*multiplicty_offset))):
                if ao1_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = ao1_e_count

                self.__draw_occupancy((2*margin + 0.5*level_width),
                                      ao1_loc['ye'][e], nr_e, nr_levels)
                ao1_e_count = ao1_e_count - nr_e

        # atom 2 levels
        for e in range(len(ao2_loc['ye'])):
            if nr_a2 >= 2 and self.data.fragment2.name != "H":
                nr_levels = int(ao2_loc['ye'].count(ao2_loc['ye'][e])/nr_a2)
            else:
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
                (mo_loc['ye'][e] == (mo_loc['yme'][e]-0.5*multiplicty_offset))):

                # determine how many electrons need to be placed
                if mo_e_count >= 2*nr_levels:
                    nr_e = 2*nr_levels
                else:
                    nr_e = mo_e_count

                self.__draw_occupancy((0.5*width+0.5*margin),
                                      mo_loc['ye'][e], nr_e, nr_levels)
                mo_e_count -= nr_e

    def __draw_occupancy(self, level_loc_x, level_loc_y, nr_elec, nr_levels):
        """
        Draws the occupancy of energy (multiplicity) level(s) based on nr_elec
        and nr_levels
        """
        x_space = self.settings.x_space

        if nr_elec <= 0:
            # do nothing
            pass
        elif nr_elec == 2*nr_levels:
            # sets of fully filled levels
            if nr_levels == 1:
                self.__draw_arrow_set(level_loc_x, level_loc_y)
            elif nr_levels == 2:
                self.__draw_arrow_set(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-0.5*x_space, level_loc_y)
            elif nr_levels == 3:
                self.__draw_arrow_set(level_loc_x+x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x, level_loc_y)
                self.__draw_arrow_set(level_loc_x-x_space, level_loc_y)
            elif nr_levels == 4:
                self.__draw_arrow_set(level_loc_x+1.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-1.5*x_space, level_loc_y)
            elif nr_levels == 5:
                self.__draw_arrow_set(level_loc_x+2*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x+x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x, level_loc_y)
                self.__draw_arrow_set(level_loc_x-x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-2*x_space, level_loc_y)
            elif nr_levels == 6:
                self.__draw_arrow_set(level_loc_x+2.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x+1.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-1.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-2.5*x_space, level_loc_y)
        elif nr_elec <= nr_levels:
            # only partial occupied levels
            if nr_elec == 1:
                self.__draw_arrow_single(level_loc_x, level_loc_y)
            elif nr_elec == 2:
                self.__draw_arrow_single(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x-0.5*x_space, level_loc_y)
            elif nr_levels == 3:
                self.__draw_arrow_single(level_loc_x+x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x, level_loc_y)
                self.__draw_arrow_single(level_loc_x-x_space, level_loc_y)
            elif nr_levels == 4:
                self.__draw_arrow_single(level_loc_x+1.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x-0.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x-1.5*x_space, level_loc_y)
        elif nr_elec == nr_levels+1:
            if nr_elec == 3:
                self.__draw_arrow_single(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-0.5*x_space, level_loc_y)
            elif nr_elec == 4:
                self.__draw_arrow_single(level_loc_x+x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x, level_loc_y)
                self.__draw_arrow_set(level_loc_x-x_space, level_loc_y)
            elif nr_levels == 5:
                self.__draw_arrow_single(level_loc_x+1.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x-0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-1.5*x_space, level_loc_y)
        elif nr_elec == nr_levels+2:
            if nr_elec == 5:
                self.__draw_arrow_single(level_loc_x+x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x, level_loc_y)
                self.__draw_arrow_set(level_loc_x-x_space, level_loc_y)
            elif nr_levels == 5:
                self.__draw_arrow_single(level_loc_x+1.5*x_space, level_loc_y)
                self.__draw_arrow_single(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-1.5*x_space, level_loc_y)
        elif nr_elec == nr_levels+3:
            if nr_levels == 7:
                self.__draw_arrow_single(level_loc_x+1.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x+0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-0.5*x_space, level_loc_y)
                self.__draw_arrow_set(level_loc_x-1.5*x_space, level_loc_y)

    def __draw_arrow_set(self, x, y):
        """
        Adds an arrow set (one up one down) at location x,y
        """
        x_space_interset = self.settings.x_space_interset
        arrow = self.__arrow
        arrow_color = self.settings.arrow_color
        arrow_length = self.settings.arrow_length

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

    def __draw_arrow_single(self, x, y):
        """
        Adds an single arrow (one up) at location x,y
        """
        arrow = self.__arrow
        arrow_color = self.settings.arrow_color
        arrow_length = self.settings.arrow_length

        self.image.append(draw.Line(x, y + 7/12*arrow_length,
                                    x, y - 5/12*arrow_length,
                                    stroke=arrow_color,
                                    marker_end=arrow))

    def __draw_contributions(self):
        """
        Draws the contributions of the different atomic orbitals to the
        molecular orbitals
        """
        abs_cutoff = self.settings.orbc_cutoff
        print_coeff = self.settings.draw_orbc
        opacity = self.settings.orbc_opacity
        linestyle = self.settings.orbc_linestyle
        color = self.settings.orbc_color
        font_size = self.settings.orbc_font_size

        orbc = np.transpose(self.data.molecule.state_coefficients)
        ao1_loc = self.__ao1_loc
        ao2_loc = self.__ao2_loc
        mo_loc = self.__mo_loc

        path_memory = []

        for i in range(len(orbc[0])):
            for j in range(len(orbc[0])):
                if abs(orbc[i][j]) >= abs_cutoff:
                    if j in self.data.fragment1.bf_mapping.keys():
                        bf_id = self.data.fragment1.bf_mapping[j]
                        p = draw.Line(ao1_loc['xe'][bf_id],
                                      ao1_loc['ye'][bf_id],
                                      mo_loc['xb'][i],
                                      mo_loc['yb'][i], stroke=color,
                                      fill_opacity=opacity,
                                      stroke_dasharray=linestyle)
                        path_memory.append(p)
                        if path_memory.count(p) == 1:
                            self.image.append(p)

                        if print_coeff is True:
                            str_coeffs = [str(round(c, 2)) for c in orbc[i]]
                            if path_memory.count(p) == 1:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=-0.4, fill=color))
                            elif path_memory.count(p) == 2:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=1, fill=color))
                            elif path_memory.count(p) == 3:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=2, fill=color))
                            elif path_memory.count(p) == 4:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=-1.4, fill=color))
                    elif j in self.data.fragment2.bf_mapping.keys():
                        bf_id = self.data.fragment2.bf_mapping[j]
                        p = draw.Line(mo_loc['xe'][i],
                                      mo_loc['ye'][i],
                                      ao2_loc['xb'][bf_id],
                                      ao2_loc['yb'][bf_id],
                                      stroke=color, fill_opacity=opacity,
                                      stroke_dasharray=linestyle)
                        path_memory.append(p)
                        if path_memory.count(p) == 1:
                            self.image.append(p)

                        if print_coeff is True:
                            str_coeffs = [str(round(c, 2)) for c in orbc[i]]
                            if path_memory.count(p) == 1:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=-0.4, fill=color))
                            elif path_memory.count(p) == 2:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=1, fill=color))
                            elif path_memory.count(p) == 3:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=2, fill=color))
                            elif path_memory.count(p) == 4:
                                self.image.append(draw.Text(
                                    str_coeffs[j], font_size, path=p,
                                    text_anchor='middle',
                                    line_offset=-1.4, fill=color))

    def __draw_energy_scale(self):
        """
        Draws the energy scale with energy labels

        There are different styles:
            - mo : only molecular orbital labels
            - mo_ao : both molecular and atomic orbital labls
            - ao : only atomic orbitals labels
        """
        margin = self.settings.margin
        height = self.settings.height
        font_size = self.settings.font_size

        unit = self.settings.unit
        color = self.settings.energy_scale_color

        # Drawing the bar itself
        arrow = draw.Marker(-0.3, -0.4, 0.6, 0.4, scale=10, orient='auto')
        arrow.append(draw.Lines(-0.3, 0.4, 0, 0, -0.3, -0.4, 0.6, 0,
                                fill=color, close=True))
        self.image.append(draw.Line(margin, height-margin+14,
                                    margin, 0.5*margin,
                                    stroke=color, marker_end=arrow))

        # Adding energy and unit to bar
        self.image.append(draw.Text('Energy', font_size,
                                    3, 20,
                                    center=True, text_anchor='begin',
                                    fill=color))
        if unit == 'Hartree':
            self.image.append(draw.Text('(Hartree)', font_size,
                                        3, 35,
                                        center=True, text_anchor='begin',
                                        fill=color))
        elif unit == 'Ht':
            self.image.append(draw.Text('(Ht)', font_size,
                                        3, 35,
                                        center=True, text_anchor='begin',
                                        fill=color))
        else:
            raise NotImplementedError('Other units are not yet implemented')

    def __draw_energy_labels(self):
        """
        Adds energy labels to energy scale
        """
        style = self.settings.energy_scale_style
        labels = self.settings.energy_scale_labels

        moe = self.data.moe_labels
        aoe1 = self.data.fragment1.nelec
        aoe2 = self.data.fragment2.nelec
        nr_a1 = 1
        nr_a2 = 1

        mo_loc = self.__mo_loc
        ao1_loc = self.__ao1_loc
        ao2_loc = self.__ao2_loc

        if style == 'mo':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                self.__draw_energy_label(mo_loc, labels, core=True)
            else:
                self.__draw_energy_label(mo_loc, moe, core=True)

        elif style == 'mo_ao':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                self.__draw_energy_label(mo_loc, labels[0], core=True)
                self.__draw_energy_label(ao1_loc, labels[1])
                self.__draw_energy_label(ao2_loc, labels[2])
            else:
                if nr_a1 > 1:
                    aoe1 = aoe1*nr_a1
                else:
                    aoe1 = aoe1
                if nr_a2 > 1:
                    aoe2 = aoe2*nr_a2
                else:
                    aoe2 = aoe2
                self.__draw_energy_label(mo_loc, moe, core=True)
                self.__draw_energy_label(ao1_loc, aoe1)
                self.__draw_energy_label(ao2_loc, aoe2)

        elif style == 'ao':
            if isinstance(labels, list) or isinstance(labels, np.ndarray):
                self.__draw_energy_label(ao1_loc, labels[0], core=True)
                self.__draw_energy_label(ao2_loc, labels[1], core=True)
            else:
                if nr_a1 > 1:
                    aoe1 = aoe1*nr_a1
                else:
                    aoe1 = aoe1
                if nr_a2 > 1:
                    aoe2 = aoe2*nr_a2
                else:
                    aoe2 = aoe2
                self.__draw_energy_label(ao1_loc, aoe1, core=True)
                self.__draw_energy_label(ao2_loc, aoe2, core=True)
        else:
            raise Exception("An invalid style for energy lables, valid styles"
                            " include 'mo', 'mo_ao' and 'ao'")

    def __draw_energy_label(self, loc_dict, labels, core=False):
        """
        Adds energy labels to energy scale
        """

        # core tag is used to only draw labels once, ao energies and
        # mo energies vary a small amount in energy so tags would be draw
        # on top of each other

        margin = self.settings.margin
        core_cutoff = self.settings.core_cutoff
        significant_digits = self.settings.label_significant_digits

        font_size = self.settings.font_size
        color = self.settings.energy_scale_color

        text_memory = []
        x = margin - 4
        for j in range(len(loc_dict['xb'])):
            t = draw.Text(str(round(labels[j], significant_digits)),
                          font_size,
                          x, loc_dict['yb'][j],
                          center=True, text_anchor='end', fill=color)
            text_memory.append(t)
            if core:
                if text_memory.count(t) == 1:
                    self.image.append(t)
                    self.image.append(draw.Line(margin,
                                                loc_dict['yb'][j], x+1,
                                                loc_dict['yb'][j],
                                                stroke=color))
            else:
                if (round(labels[j], significant_digits) >=
                        core_cutoff and text_memory.count(t) == 1):
                    self.image.append(t)
                    self.image.append(draw.Line(margin,
                                                loc_dict['yb'][j], x+1,
                                                loc_dict['yb'][j],
                                                stroke=color))

    def __draw_level_labels(self):
        """
        Adds labels to atomic and molecular orbitals
        """
        style = self.settings.level_labels_style
        labels_mo = self.settings.mo_labels
        labels_ao1 = self.settings.ao1_labels
        labels_ao2 = self.settings.ao2_labels

        if style == 'mo':
            self.__draw_mo_labels(labels_mo)
        elif style == 'mo_ao':
            self.__draw_mo_labels(labels_mo)
            self.__draw_ao1_labels(labels_ao1)
            self.__draw_ao2_labels(labels_ao2)
        elif style == 'ao':
            self.__draw_ao1_labels(labels_ao1)
            self.__draw_ao2_labels(labels_ao2)
        else:
            raise Exception("An invalid style for lables, valid styles include"
                            " 'mo', 'mo_ao' and 'ao'")

    def __draw_mo_labels(self, labels):
        """
        Adds labels to molecular orbitals
        """
        mo_loc = self.__mo_loc
        font_size = self.settings.font_size
        color = self.settings.main_color

        label_memory = []
        y_memory = []
        x = mo_loc['xe'][0]

        for j in range(len(mo_loc['xb'])):
            label = draw.Text(labels[j],
                              font_size,
                              x, mo_loc['ymb'][j]+10,
                              center=True, text_anchor='end', fill=color)
            label_memory.append(label)
            y = mo_loc['yb'][j]
            y_memory.append(y)

        unique_y = []
        for y in y_memory:
            if y not in unique_y:
                unique_y.append(y)

        for y in unique_y:
            count = y_memory.count(y)
            self.image.append(label_memory[y_memory.index(y) + count - 1])

    def __draw_ao1_labels(self, labels):
        """
        Adds labels to atomic orbitals of atom 1
        """
        nr_a1 = 1
        ao1_loc = self.__ao1_loc
        font_size = self.settings.font_size
        color = self.settings.main_color

        lvls = int(len(ao1_loc['xb'])/nr_a1)

        label_memory = []
        x = ao1_loc['xb'][0]-2
        for j in range(lvls):
            label = draw.Text(labels[j],
                              font_size,
                              x, ao1_loc['yb'][j],
                              center=True, text_anchor='end',
                              fill=color)
            label_memory.append(label)
            if label_memory.count(label) == 1:
                self.image.append(label)

    def __draw_ao2_labels(self, labels):
        """
        Adds labels to atomic orbitals of atom 2
        """
        nr_a2 = 1
        ao2_loc = self.__ao2_loc
        font_size = self.settings.font_size
        color = self.settings.main_color

        lvls = int(len(ao2_loc['xb'])/nr_a2)

        label_memory = []
        x = ao2_loc['xe'][0]+2
        for j in range(lvls):
            label = draw.Text(labels[j],
                              font_size,
                              x, ao2_loc['yb'][j],
                              center=True, text_anchor='begin',
                              fill=color)
            label_memory.append(label)
            if label_memory.count(label) == 1:
                self.image.append(label)
