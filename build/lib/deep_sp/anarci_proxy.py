from setuptools.command.alias import alias

from nextera_utils.docker_interop import DockerInterop


class AnarciProxy(object):

    @staticmethod
    def run_anarci(seqs, scheme=None, allow=None, allowed_species=None, h_chain=True, assign_germline=False):
        sequences, numbered, alignment_details, hit_tables = None, None, None, None
        debug_key = DockerInterop.get_instance().get_debug_key()
        if debug_key is None:
            import anarci as a
            if (scheme is None and allow is None and allowed_species is None):
                sequences, numbered, alignment_details, hit_tables = a.run_anarci(seqs, scheme='imgt',  assign_germline=assign_germline)
            else:
                sequences, numbered, alignment_details, hit_tables = a.run_anarci(seqs, scheme=scheme,
                                                                                  allow=allow,
                                                                                  allowed_species=allowed_species,
                                                                                  assign_germline=assign_germline)
        else:
            if h_chain:
                sequences, numbered = AnarciProxy._create_h_chain_dummies()
            else:
                sequences, numbered = AnarciProxy._create_l_chain_dummies()
            pass
        return sequences, numbered, alignment_details, hit_tables

    # @staticmethod
    # def run_anarci(seqs, h_chain=True):
    #     sequences, numbered, alignment_details, hit_tables = None, None, None, None
    #     debug_key = DockerInterop.get_instance().get_debug_key()
    #     if debug_key is None:
    #         import anarci as a
    #         sequences, numbered, alignment_details, hit_tables = a.run_anarci(seqs, scheme='imgt')
    #     else:
    #         if h_chain:
    #             sequences, numbered  = AnarciProxy._create_h_chain_dummies()
    #         else:
    #             sequences, numbered = AnarciProxy._create_l_chain_dummies()
    #         pass
    #     return sequences, numbered, alignment_details, hit_tables

    @staticmethod
    def _create_h_chain_dummies():
        seqs=[('mAb1', 'EVQLVESGGGLVQPGRSLRLSCAASGFTFDDYAMHWVRQAPGKGLEWVSAITWNSGHIDYADSVEGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCAKVSYLSTASSLDYWGQGTLVTVSS')]
        numbers = [[([((1, ' '), 'E'), ((2, ' '), 'V'), ((3, ' '), 'Q'), ((4, ' '), 'L'), ((5, ' '), 'V'), ((6, ' '), 'E'), ((7, ' '), 'S'), ((8, ' '), 'G'), ((9, ' '), 'G'), ((10, ' '), '-'), ((11, ' '), 'G'), ((12, ' '), 'L'), ((13, ' '), 'V'), ((14, ' '), 'Q'), ((15, ' '), 'P'), ((16, ' '), 'G'), ((17, ' '), 'R'), ((18, ' '), 'S'), ((19, ' '), 'L'), ((20, ' '), 'R'), ((21, ' '), 'L'), ((22, ' '), 'S'), ((23, ' '), 'C'), ((24, ' '), 'A'), ((25, ' '), 'A'), ((26, ' '), 'S'), ((27, ' '), 'G'), ((28, ' '), 'F'), ((29, ' '), 'T'), ((30, ' '), 'F'), ((31, ' '), '-'), ((32, ' '), '-'), ((33, ' '), '-'), ((34, ' '), '-'), ((35, ' '), 'D'), ((36, ' '), 'D'), ((37, ' '), 'Y'), ((38, ' '), 'A'), ((39, ' '), 'M'), ((40, ' '), 'H'), ((41, ' '), 'W'), ((42, ' '), 'V'), ((43, ' '), 'R'), ((44, ' '), 'Q'), ((45, ' '), 'A'), ((46, ' '), 'P'), ((47, ' '), 'G'), ((48, ' '), 'K'), ((49, ' '), 'G'), ((50, ' '), 'L'), ((51, ' '), 'E'), ((52, ' '), 'W'), ((53, ' '), 'V'), ((54, ' '), 'S'), ((55, ' '), 'A'), ((56, ' '), 'I'), ((57, ' '), 'T'), ((58, ' '), 'W'), ((59, ' '), 'N'), ((60, ' '), '-'), ((61, ' '), '-'), ((62, ' '), 'S'), ((63, ' '), 'G'), ((64, ' '), 'H'), ((65, ' '), 'I'), ((66, ' '), 'D'), ((67, ' '), 'Y'), ((68, ' '), 'A'), ((69, ' '), 'D'), ((70, ' '), 'S'), ((71, ' '), 'V'), ((72, ' '), 'E'), ((73, ' '), '-'), ((74, ' '), 'G'), ((75, ' '), 'R'), ((76, ' '), 'F'), ((77, ' '), 'T'), ((78, ' '), 'I'), ((79, ' '), 'S'), ((80, ' '), 'R'), ((81, ' '), 'D'), ((82, ' '), 'N'), ((83, ' '), 'A'), ((84, ' '), 'K'), ((85, ' '), 'N'), ((86, ' '), 'S'), ((87, ' '), 'L'), ((88, ' '), 'Y'), ((89, ' '), 'L'), ((90, ' '), 'Q'), ((91, ' '), 'M'), ((92, ' '), 'N'), ((93, ' '), 'S'), ((94, ' '), 'L'), ((95, ' '), 'R'), ((96, ' '), 'A'), ((97, ' '), 'E'), ((98, ' '), 'D'), ((99, ' '), 'T'), ((100, ' '), 'A'), ((101, ' '), 'V'), ((102, ' '), 'Y'), ((103, ' '), 'Y'), ((104, ' '), 'C'), ((105, ' '), 'A'), ((106, ' '), 'K'), ((107, ' '), 'V'), ((108, ' '), 'S'), ((109, ' '), 'Y'), ((110, ' '), 'L'), ((111, ' '), 'S'), ((112, 'A'), 'T'), ((112, ' '), 'A'), ((113, ' '), 'S'), ((114, ' '), 'S'), ((115, ' '), 'L'), ((116, ' '), 'D'), ((117, ' '), 'Y'), ((118, ' '), 'W'), ((119, ' '), 'G'), ((120, ' '), 'Q'), ((121, ' '), 'G'), ((122, ' '), 'T'), ((123, ' '), 'L'), ((124, ' '), 'V'), ((125, ' '), 'T'), ((126, ' '), 'V'), ((127, ' '), 'S'), ((128, ' '), 'S')], 0, 120)]]
        return seqs, numbers

    @staticmethod
    def _create_l_chain_dummies():
        seqs = [('mAb1', 'DIQMTQSPSSLSASVGDRVTITCRASQGIRNYLAWYQQKPGKAPKLLIYAASTLQSGVPSRFSGSGSGTDFTLTISSLQPEDVATYYCQRYNRAPYTFGQGTKVEIK')]
        numbers = [[([((1, ' '), 'D'), ((2, ' '), 'I'), ((3, ' '), 'Q'), ((4, ' '), 'M'), ((5, ' '), 'T'), ((6, ' '), 'Q'), ((7, ' '), 'S'), ((8, ' '), 'P'), ((9, ' '), 'S'), ((10, ' '), 'S'), ((11, ' '), 'L'), ((12, ' '), 'S'), ((13, ' '), 'A'), ((14, ' '), 'S'), ((15, ' '), 'V'), ((16, ' '), 'G'), ((17, ' '), 'D'), ((18, ' '), 'R'), ((19, ' '), 'V'), ((20, ' '), 'T'), ((21, ' '), 'I'), ((22, ' '), 'T'), ((23, ' '), 'C'), ((24, ' '), 'R'), ((25, ' '), 'A'), ((26, ' '), 'S'), ((27, ' '), 'Q'), ((28, ' '), 'G'), ((29, ' '), 'I'), ((30, ' '), '-'), ((31, ' '), '-'), ((32, ' '), '-'), ((33, ' '), '-'), ((34, ' '), '-'), ((35, ' '), '-'), ((36, ' '), 'R'), ((37, ' '), 'N'), ((38, ' '), 'Y'), ((39, ' '), 'L'), ((40, ' '), 'A'), ((41, ' '), 'W'), ((42, ' '), 'Y'), ((43, ' '), 'Q'), ((44, ' '), 'Q'), ((45, ' '), 'K'), ((46, ' '), 'P'), ((47, ' '), 'G'), ((48, ' '), 'K'), ((49, ' '), 'A'), ((50, ' '), 'P'), ((51, ' '), 'K'), ((52, ' '), 'L'), ((53, ' '), 'L'), ((54, ' '), 'I'), ((55, ' '), 'Y'), ((56, ' '), 'A'), ((57, ' '), 'A'), ((58, ' '), '-'), ((59, ' '), '-'), ((60, ' '), '-'), ((61, ' '), '-'), ((62, ' '), '-'), ((63, ' '), '-'), ((64, ' '), '-'), ((65, ' '), 'S'), ((66, ' '), 'T'), ((67, ' '), 'L'), ((68, ' '), 'Q'), ((69, ' '), 'S'), ((70, ' '), 'G'), ((71, ' '), 'V'), ((72, ' '), 'P'), ((73, ' '), '-'), ((74, ' '), 'S'), ((75, ' '), 'R'), ((76, ' '), 'F'), ((77, ' '), 'S'), ((78, ' '), 'G'), ((79, ' '), 'S'), ((80, ' '), 'G'), ((81, ' '), '-'), ((82, ' '), '-'), ((83, ' '), 'S'), ((84, ' '), 'G'), ((85, ' '), 'T'), ((86, ' '), 'D'), ((87, ' '), 'F'), ((88, ' '), 'T'), ((89, ' '), 'L'), ((90, ' '), 'T'), ((91, ' '), 'I'), ((92, ' '), 'S'), ((93, ' '), 'S'), ((94, ' '), 'L'), ((95, ' '), 'Q'), ((96, ' '), 'P'), ((97, ' '), 'E'), ((98, ' '), 'D'), ((99, ' '), 'V'), ((100, ' '), 'A'), ((101, ' '), 'T'), ((102, ' '), 'Y'), ((103, ' '), 'Y'), ((104, ' '), 'C'), ((105, ' '), 'Q'), ((106, ' '), 'R'), ((107, ' '), 'Y'), ((108, ' '), 'N'), ((109, ' '), 'R'), ((110, ' '), '-'), ((111, ' '), '-'), ((112, ' '), '-'), ((113, ' '), '-'), ((114, ' '), 'A'), ((115, ' '), 'P'), ((116, ' '), 'Y'), ((117, ' '), 'T'), ((118, ' '), 'F'), ((119, ' '), 'G'), ((120, ' '), 'Q'), ((121, ' '), 'G'), ((122, ' '), 'T'), ((123, ' '), 'K'), ((124, ' '), 'V'), ((125, ' '), 'E'), ((126, ' '), 'I'), ((127, ' '), 'K')], 0, 106)]]
        return seqs, numbers
