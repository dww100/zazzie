# -*- coding: utf-8 -*-
"""
Preprocessor to finalize system description after PDB Scan, this is the first
step in PDB Rx

    SASSIE: Copyright (C) 2011 Joseph E. Curtis, Ph.D.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import json

import sassie.build.pdbscan.pdbscan.pdbscan_utils as pdbscan_utils

#import sassie.build.pdbrx.pdbrx.segname_utils as segname_utils
#import sassie.build.pdbrx.pdbrx.fasta_utils as fasta_utils
#import sassie.build.pdbrx.pdbrx.biomt_utils as biomt_utils

from . import segname_utils as segname_utils
from . import fasta_utils as fasta_utils
from . import biomt_utils as biomt_utils

from . import sassie_web_editor as sassie_web_editor

def get_user_segmentation(other_self, mol):
    """
    Get new segmentation from user
    @rtype :  dictionary
    @return:  Keys = atom index of start of segment,
                  Value = segname
    """

    #ui_output = sassie_web_editor.SegnameEditor(
    #        mol.segnames(), other_self.resid_descriptions, json, logger).get_segment_starts()

    ui_output = False
    
    if ui_output:
        segname_starts = json.loads(
                ui_output, object_hook = segname_utils.convert_segname_start)
    else:
        segname_starts = {}

    return segname_starts

def handle_sassie_web_user_input(other_self, mol, pdbscan_report):

    """
    Present user with options to edit segmentation, sequence and BIOMT from
    the commandline.

    @return:
    """

    mvars = other_self.mvars
    log = other_self.log

    process_segment_input(other_self, mol)

def process_segment_input(other_self, mol):

    mvars = other_self.mvars
    log = other_self.log

    accepted_segmentation = False

    log.info('UI_TYPE = ' + mvars.user_interface)
            
    sassie_query_object  = sassie_web_editor.SegnameEditor(\
                mol.segnames(), other_self.resid_descriptions, other_self.json, pdbscan_report, log)
        
    choice = sassie_query_object.answer["_response"]["button"]
            
    if choice == 'yes':
        choice = 'no'

    if choice == 'no':
        accepted_segmentation = True

    while not accepted_segmentation:

        if choice in ['y', 'yes']:

            segname_starts = get_user_segmentation()

            if segname_starts:
                segname_utils.redefine_segments(mol, segname_starts)
                mol.check_segname_simulation_preparedness()

            accepted_segmentation = True

        elif choice in ['n', 'no']:

            accepted_segmentation = True

        accepted_sequences = False
       
        seq_segnames = mol.segname_info.sequence.keys()

        sequence_report = segname_utils.create_sequence_report(mol, seq_segnames) 

    return