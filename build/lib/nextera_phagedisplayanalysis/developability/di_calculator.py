from nextera_utils.docker_interop import DockerInterop
from nextera_phagedisplayanalysis.developability import predictor_plotter
import pandas as pd
import copy
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.preprocessing import StandardScaler


class DiCalculator(object):
    def __init__(self, scale=False, di_estimation_mode='linear3'):
        self._scale = scale
        self._debug_key = DockerInterop.get_instance().get_debug_key()
        self._m_ab_dis = self._get_m_ab_dis()
        self._m_ab_sequences = self._get_m_ab_sequences()
        self._di_estimation_mode = di_estimation_mode
        self._properties = self._get_properties()
        self._model = None
        self._di_categories = [0.8, 3.2]

    def _get_properties(self):
        if self._di_estimation_mode == 'linear3':
            out = ['SAP_pos_CDRH3', 'SCM_pos_CDRL3', 'SCM_neg_CDRH3']
        elif self._di_estimation_mode == 'linear4':
            out = ['SAP_pos_CDRH3', 'SCM_pos_CDRL1', 'SCM_pos_CDR', 'SCM_pos_Hv']
        elif self._di_estimation_mode == 'linear30':
            out = ['SAP_pos_CDRH3', 'SAP_pos_CDRH2','SAP_pos_CDRH1',
                   'SAP_pos_CDRL3', 'SAP_pos_CDRL2', 'SAP_pos_CDRL1', 'SAP_pos_CDR',
                   'SAP_pos_Hv', 'SAP_pos_Lv', 'SAP_pos_Fv',
                   'SCM_pos_CDRH3', 'SCM_pos_CDRH2', 'SCM_pos_CDRH1',
                   'SCM_pos_CDRL3', 'SCM_pos_CDRL2', 'SCM_pos_CDRL1', 'SCM_pos_CDR',
                   'SCM_pos_Hv', 'SCM_pos_Lv', 'SCM_pos_Fv',
                   'SCM_neg_CDRH3', 'SCM_neg_CDRH2', 'SCM_neg_CDRH1',
                   'SCM_neg_CDRL3', 'SCM_neg_CDRL2', 'SCM_neg_CDRL1', 'SCM_neg_CDR',
                   'SCM_neg_Hv', 'SCM_neg_Lv', 'SCM_neg_Fv']
        elif self._di_estimation_mode == 'svr3':
            out = ['SCM_pos_CDRH3', 'SCM_neg_CDRH2', 'SCM_neg_Fv']
        elif self._di_estimation_mode == 'svr4':
            out = ['SCM_pos_CDRH3', 'SCM_neg_CDRH2', 'SCM_neg_CDRL2', 'SCM_neg_Fv']
        elif self._di_estimation_mode == 'randomForest3':
            out = ['SAP_pos_Hv', 'SCM_pos_CDRH3', 'SCM_neg_Fv']
        elif self._di_estimation_mode == 'randomForest4':
            out = ['SAP_pos_Hv', 'SCM_pos_CDRH3', 'SCM_pos_Lv', 'SCM_neg_Fv']
        else:
            raise NotImplementedError()
        return out

    def _get_m_ab_dis(self):
        m_abs = []
        m_abs.append(0.534)
        m_abs.append(0.628)
        m_abs.append(0.416)
        m_abs.append(3.171)
        m_abs.append(0.754)
        m_abs.append(0.573)
        m_abs.append(0.471)
        m_abs.append(0.463)
        m_abs.append(1.209)
        m_abs.append(0.455)
        m_abs.append(0.550)
        m_abs.append(0.605)
        m_abs.append(1.892)
        m_abs.append(0.573)
        m_abs.append(0.636)
        m_abs.append(0.667)
        m_abs.append(1.476)
        m_abs.append(0.597)
        m_abs.append(0.432)
        m_abs.append(0.534)
        m_abs.append(1.028)
        return m_abs
    
    def _get_m_ab_sequences(self):
        out=[]
        mAb1_heavy = 'QVQLQESGPGLVRPSQTLSLTCTVSGYSITSDHAWSWVRQPPGRGLEWIGYISYSGITTYNPSLKSRVTMLRDTSKNQFSLRLSSVTAADTAVYYCARSLARTTAMDYWGQGSLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSRDELTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPG'
        mAb1_light = 'DIQMTQSPSSLSASVGDRVTITCRASQDISSYLNWYQQKPGKAPKLLIYYTSRLHSGVPSRFSGSGSGTDFTFTISSLQPEDIATYYCQQGNTLPYTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb1_light, mAb1_heavy))
        mAb2_heavy ='EVQLVESGGGLVQPGRSLRLSCAASGFTFNDYAMHWVRQAPGKGLEWVSTISWNSGSIGYADSVKGRFTISRDNAKKSLYLQMNSLRAEDTALYYCAKDIQYGNYYYGMDVWGQGTTVTVSSASTKGPSVFPLAPGSSKSTSGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb2_light ='EIVLTQSPATLSLSPGERATLSCRASQSVSSYLAWYQQKPGQAPRLLIYDASNRATGIPARFSGSGSGTDFTLTISSLEPEDFAVYYCQQRSNWPITFGQGTRLEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb2_light, mAb2_heavy))
        mAb3_heavy ='QVQLQESGPGLVKPSETLSLTCTVSGGSVSSGDYYWTWIRQSPGKGLEWIGHIYYSGNTNYNPSLKSRLTISIDTSKTQFSLKLSSVTAADTAIYYCVRDRVTGAFDIWGQGTMVTVSSASTKGPSVFPLAPCSRSTSESTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSNFGTQTYTCNVDHKPSNTKVDKTVERKCCVECPPCPAPPVAGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVQFNWYVDGVEVHNAKTKPREEQFNSTFRVVSVLTVVHQDWLNGKEYKCKVSNKGLPAPIEKTISKTKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPMLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb3_light ='DIQMTQSPSSLSASVGDRVTITCQASQDISNYLNWYQQKPGKAPKLLIYDASNLETGVPSRFSGSGSGTDFTFTISSLQPEDIATYFCQHFDHLPLAFGGGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb3_light, mAb3_heavy))
        mAb4_heavy ='EVQLVESGGGLVQPGGSLRLSCAASGYTFTNYGMNWVRQAPGKGLEWVGWINTYTGEPTYAADFKRRFTFSLDTSKSTAYLQMNSLRAEDTAVYYCAKYPHYYGSSHWYFDVWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb4_light ='DIQMTQSPSSLSASVGDRVTITCSASQDISNYLNWYQQKPGKAPKVLIYFTSSLHSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQYSTVPWTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb4_light, mAb4_heavy))
        mAb5_heavy ='EVQLVESGGGLVQPGRSLRLSCAASGFTFDDYAMHWVRQAPGKGLEWVSAITWNSGHIDYADSVEGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCAKVSYLSTASSLDYWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb5_light ='DIQMTQSPSSLSASVGDRVTITCRASQGIRNYLAWYQQKPGKAPKLLIYAASTLQSGVPSRFSGSGSGTDFTLTISSLQPEDVATYYCQRYNRAPYTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb5_light, mAb5_heavy))
        mAb6_heavy ='EVQLVQSGGGLVKPGGSLRLSCAASGFTFSSYSMNWVRQAPGKGLEWVSSISSSSSYIYYADSVKGRFTISRDNAKNSLYLQMNSLRAEDTAVYYCARVTDAFDIWGQGTMVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb6_light ='DIQMTQSPSSVSASIGDRVTITCRASQGIDNWLGWYQQKPGKAPKLLIYDASNLDTGVPSRFSGSGSGTYFTLTISSLQAEDFAVYFCQQAKAFPPTFGGGTKVDIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb6_light, mAb6_heavy))
        mAb7_heavy ='EVQLVESGGGLVQPGGSLRLSCAASGFDFSRYWMSWVRQAPGKGLEWIGEINPDSSTINYAPSLKDKFIISRDNAKNSLYLQMNSLRAEDTAVYYCARPDGNYWYFDVWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSRDELTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb7_light ='DIQMTQSPSSLSASVGDRVTITCKASQDVGIAVAWYQQKPGKVPKLLIYWASTRHTGVPDRFSGSGSGTDFTLTISSLQPEDVATYYCQQYSSYPYTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb7_light, mAb7_heavy))
        mAb8_heavy ='QVQLVESGGGVVQPGRSLRLDCKASGITFSNSGMHWVRQAPGKGLEWVAVIWYDGSKRYYADSVKGRFTISRDNSKNTLFLQMNSLRAEDTAVYYCATNDDYWGQGTLVTVSSASTKGPSVFPLAPCSRSTSESTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTKTYTCNVDHKPSNTKVDKRVESKYGPPCPPCPAPEFLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSQEDPEVQFNWYVDGVEVHNAKTKPREEQFNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKGLPSSIEKTISKAKGQPREPQVYTLPPSQEEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSRLTVDKSRWQEGNVFSCSVMHEALHNHYTQKSLSLSLGK'
        mAb8_light ='EIVLTQSPATLSLSPGERATLSCRASQSVSSYLAWYQQKPGQAPRLLIYDASNRATGIPARFSGSGSGTDFTLTISSLEPEDFAVYYCQQSSNWPRTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb8_light, mAb8_heavy))
        mAb9_heavy ='EVQLVESGGGLVQPGGSLRLSCAASGFTFTDYTMDWVRQAPGKGLEWVADVNPNSGGSIYNQRFKGRFTLSVDRSKNTLYLQMNSLRAEDTAVYYCARNLGPSFYFDYWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPG'
        mAb9_light ='DIQMTQSPSSLSASVGDRVTITCKASQDVSIGVAWYQQKPGKAPKLLIYSASYRYTGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQYYIYPYTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb9_light, mAb9_heavy))
        mAb10_heavy ='EVQLVESGGGLVQPGGSLRLSCAASGFNIKDTYIHWVRQAPGKGLEWVARIYPTNGYTRYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCSRWGGDGFYAMDYWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb10_light ='DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb10_light, mAb10_heavy))
        mAb11_heavy ='QVTLRESGPALVKPTQTLTLTCTVSGFSLTSYSVHWVRQPPGKGLEWLGVIWASGGTDYNSALMSRLSISKDTSRNQVVLTMTNMDPVDTATYYCARDPPSSLLRLDYWGRGTPVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb11_light ='DIVMTQSPDSLAVSLGERATINCKSSQSLLNSGNQKNYLAWYQQKPGQPPKLLIYGASTRESGVPDRFSGSGSGTDFTLTISSLQAEDVAVYYCQNVHSFPFTFGGGTKLEIKRADAAPTVSIFPPSSEQLTSGGASVVCFLNNFYPRDINVKWKIDGSERQNGVLNSWTDQDSKDSTYSMSSTLTLTKDEYERHNSYTCEATHKTSTSPIVKSFNRNEC'
        out.append((mAb11_light, mAb11_heavy))
        mAb12_heavy ='EVQLLESGGGLVQPGGSLRLSCAASGFTFSSYAMSWVRQAPGKGLEWVSGITGSGGSTYYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCAKDPGTTVIMSWFDPWGQGTLVTVSSASTKGPSVFPLAPCSRSTSESTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSNFGTQTYTCNVDHKPSNTKVDKTVERKCCVECPPCPAPPVAGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVQFNWYVDGVEVHNAKTKPREEQFNSTFRVVSVLTVVHQDWLNGKEYKCKVSNKGLPAPIEKTISKTKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPMLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb12_light ='EIVLTQSPGTLSLSPGERATLSCRASQSVRGRYLAWYQQKPGQAPRLLIYGASSRATGIPDRFSGSGSGTDFTLTISRLEPEDFAVFYCQQYGSSPRTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb12_light, mAb12_heavy))
        mAb13_heavy ='EVKLEESGGGLVQPGGSMKLSCVASGFIFSNHWMNWVRQSPEKGLEWVAEIRSKSINSATHYAESVKGRFTISRDDSKSAVYLQMTDLRTEDTGVYYCSRNYYGSTYDYWGQGTTLTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSRDELTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb13_light ='DILLTQSPAILSVSPGERVSFSCRASQFVGSSIHWYQQRTNGSPRLLIKYASESMSGIPSRFSGSGSGTDFTLSINTVESEDIADYYCQQSHSWPFTFGSGTNLEVKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb13_light, mAb13_heavy))
        mAb14_heavy ='EVQLVESGGKLLKPGGSLKLSCAASGFTFSSFAMSWFRQSPEKRLEWVAEISSGGSYTYYPDTVTGRFTISRDNAKNTLYLEMSSLRSEDTAMYYCARGLWGYYALDYWGQGTSVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSRDELTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb14_light ='QIVLIQSPAIMSASPGEKVTMTCSASSSVSYMYWYQQKPGSSPRLLIYDTSNLASGVPVRFSGSGSGTSYSLTISRMEAEDAATYYCQQWSGYPYTFGGGTKLEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb14_light, mAb14_heavy))
        mAb15_heavy ='QVQLQQPGAELVKPGASVKMSCKASGYTFTSYNMHWVKQTPGRGLEWIGAIYPGNGDTSYNQKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARSTYYGGDWYFNVWGAGTTVTVSAASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb15_light ='QIVLSQSPAILSASPGEKVTMTCRASSSVSYIHWFQQKPGSSPKPWIYATSNLASGVPVRFSGSGSGTSYSLTISRVEAEDAATYYCQQWTSNPPTFGGGTKLEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb15_light, mAb15_heavy))
        mAb16_heavy ='EVQLVQSGAEVKKPGASVKVSCKASGYTLTSYGISWVRQAPGQGLEWMGWVSFYNGNTNYAQKLQGRGTMTTDPSTSTAYMELRSLRSDDTAVYYCARGYGMDVWGQGTTVTVSSASTKGPSVFPLAPCSRSTSESTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSNFGTQTYTCNVDHKPSNTKVDKTVERKCCVECPPCPAPPVAGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVQFNWYVDGVEVHNAKTKPREEQFNSTFRVVSVLTVVHQDWLNGKEYKCKVSNKGLPAPIEKTISKTKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPMLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb16_light ='ESALTQPASVSGSPGQSITISCTGTSSDVGGYNSVSWYQQHPGKAPKLMIYEVSNRPSGVSNRFSGSKSGNTASLTISGLQAEDEADYYCNSYTSTSMVFGGGTKLTVLGQPKAAPSVTLFPPSSEELQANKATLVCLISDFYPGAVTVAWKADSSPVKAGVETTTPSKQSNNKYAASSYLSLTPEQWKSHRSYSCQVTHEGSTVEKTVAPTECS'
        out.append((mAb16_light, mAb16_heavy))
        mAb17_heavy ='QVQLVESGGGVVQPGRSLRLSCAASGFIFSSYAMHWVRQAPGNGLEWVAFMSYDGSNKKYADSVKGRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARDRGIAAGGNYYYYGMDVWGQGTTVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb17_light ='EIVLTQSPATLSLSPGERATLSCRASQSVYSYLAWYQQKPGQAPRLLIYDASNRATGIPARFSGSGSGTDFTLTISSLEPEDFAVYYCQQRSNWPPFTFGPGTKVDIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb17_light, mAb17_heavy))
        mAb18_heavy ='EVQLVESGGGLVQPGGSLRLSCAVSGYSITSGYSWNWIRQAPGKGLEWVASITYDGSTNYNPSVKGRITISRDDSKNTFYLQMNSLRAEDTAVYYCARGSHYFGHWHFAVWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb18_light ='DIQLTQSPSSLSASVGDRVTITCRASQSVDYDGDSYMNWYQQKPGKAPKLLIYAASYLESGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSHEDPYTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb18_light, mAb18_heavy))
        mAb19_heavy ='QVQLVQSGAEVKKPGSSVKVSCKASGYAFSYSWINWVRQAPGQGLEWMGRIFPGDGDTDYNGKFKGRVTITADKSTSTAYMELSSLRSEDTAVYYCARNVFDGYWLVYWGQGTLVTVSSASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSRDELTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPG'
        mAb19_light ='DIVMTQTPLSLPVTPGEPASISCRSSKSLLHSNGITYLYWYLQKPGQSPQLLIYQMSNLVSGVPDRFSGSGSGTDFTLKISRVEAEDVGVYYCAQNLELPYTFGGGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb19_light, mAb19_heavy))
        mAb20_heavy ='QVQLVQSGAEVKKPGASVKVSCKASGYIFSNYWIQWVRQAPGQGLEWMGEILPGSGSTEYTENFKDRVTMTRDTSTSTVYMELSSLRSEDTAVYYCARYFFGSSPNWYFDVWGQGTLVTVSSASTKGPSVFPLAPCSRSTSESTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSNFGTQTYTCNVDHKPSNTKVDKTVERKCCVECPPCPAPPVAGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSQEDPEVQFNWYVDGVEVHNAKTKPREEQFNSTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPSSIEKTISKAKGQPREPQVYTLPPSQEEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSRLTVDKSRWQEGNVFSCSVMHEALHNHYTQKSLSLSLGK'
        mAb20_light ='DIQMTQSPSSLSASVGDRVTITCGASENIYGALNWYQQKPGKAPKLLIYGATNLADGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQNVLNTPLTFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb20_light, mAb20_heavy))
        mAb21_heavy ='EVQLVESGGGLVQPGGSLRLSCAASGFTFSDSWIHWVRQAPGKGLEWVAWISPYGGSTYYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCARRHWPGGFDYWGQGTLVTVSAASTKGPSVFPLAPSSKSTSGGTAALGCLVKDYFPEPVTVSWNSGALTSGVHTFPAVLQSSGLYSLSSVVTVPSSSLGTQTYICNVNHKPSNTKVDKKVEPKSCDKTHTCPPCPAPELLGGPSVFLFPPKPKDTLMISRTPEVTCVVVDVSHEDPEVKFNWYVDGVEVHNAKTKPREEQYASTYRVVSVLTVLHQDWLNGKEYKCKVSNKALPAPIEKTISKAKGQPREPQVYTLPPSREEMTKNQVSLTCLVKGFYPSDIAVEWESNGQPENNYKTTPPVLDSDGSFFLYSKLTVDKSRWQQGNVFSCSVMHEALHNHYTQKSLSLSPGK'
        mAb21_light ='DIQMTQSPSSLSASVGDRVTITCRASQDVSTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQYLYHPATFGQGTKVEIKRTVAAPSVFIFPPSDEQLKSGTASVVCLLNNFYPREAKVQWKVDNALQSGNSQESVTEQDSKDSTYSLSSTLTLSKADYEKHKVYACEVTHQGLSSPVTKSFNRGEC'
        out.append((mAb21_light, mAb21_heavy))
        return out

    def train(self):
        mab_df = self._create_training_df(self._m_ab_sequences)
        X = self._calculate_deepsp_values(mab_df)
        X.set_index('Name', inplace=True)
        X = X[self._properties]
        y = self._m_ab_dis
        if self._scale:
            sc_X = StandardScaler()
            sc_y = StandardScaler()
            X = sc_X.fit_transform(X)
            y = sc_y.fit_transform(y)
        if (self._di_estimation_mode == 'linear3') or (self._di_estimation_mode == 'linear4') \
                                                   or (self._di_estimation_mode == 'linear30'):
            return self._train_linear_regression(X, y)
        elif (self._di_estimation_mode == 'svr3') or (self._di_estimation_mode == 'svr4'):
            return self._train_svr_regression(X, y)
        elif (self._di_estimation_mode == 'randomForest3') or (self._di_estimation_mode == 'randomForest4'):
            return self._train_random_forest_regression(X, y)
        else:
            raise NotImplementedError()
        return out

    def _train_linear_regression(self, X, y):
        self._model = LinearRegression()
        self._model.fit(X, y)
        sc = self._model.score(X, y)
        predictions = self._model.predict(X)
        mse =  mean_squared_error(y, predictions)
        mae =  mean_absolute_error(y, predictions)
        return mse, mae

    def _train_svr_regression(self, X, y):
        self._model = SVR(kernel="rbf", C=15, epsilon=0.1, gamma="auto")
        self._model.fit(X, y)
        predictions = self._model.predict(X)
        mse =  mean_squared_error(y, predictions)
        mae =  mean_absolute_error(y, predictions)
        return mse, mae

    def _train_random_forest_regression(self, X, y):
        self._model = RandomForestRegressor(max_depth=6)
        self._model.fit(X, y)
        predictions = self._model.predict(X)
        mse = mean_squared_error(y, predictions)
        mae = mean_absolute_error(y, predictions)
        return mse, mae

    def _create_training_df(self, sequences):
        tmp = {}
        tmp['Id'] = []
        tmp['Heavy_Chain'] = []
        tmp['Light_Chain'] = []
        for i in range(0, len(sequences), 1):
            tmp['Id'].append(str(i))
            s_h=sequences[i][1]
            s_l = sequences[i][0]
            tmp['Heavy_Chain'].append(s_h)
            tmp['Light_Chain'].append(s_l)
        df = pd.DataFrame.from_dict(tmp)
        return df

    def _calculate_deepsp_values(self, df):
        predictor = predictor_plotter.PredictorPlotter(df)
        values = predictor.calculate_developability()
        if self._debug_key is not None:
            print('Creating dummy DI values...')
            values = self._create_dummy_developability_values(values)
        return values

    def _create_dummy_developability_values(self, template):
        out=copy.deepcopy(template)
        for i in range(0, len(self._m_ab_sequences)-1, 1):
            out = out.append(template.iloc[0])
        out.reset_index(drop=True, inplace=True)
        for i in range(0, len(out), 1):
            s = str(i)
            out.iat[i, 0] = s
        return out

    def predict(self, df, out_fn):
        X = df
        X.set_index('Name', inplace=True)
        X = X[self._properties]
        y = self._m_ab_dis
        if self._scale:
            sc_X = StandardScaler()
            sc_y = StandardScaler()
            X = sc_X.fit_transform(X)
            y = sc_y.fit_transform(y)
        predictions = self._model.predict(X)
        out_df = pd.DataFrame(predictions, columns=['DI'])
        ids=list(df.index)
        out_df.insert(loc=0, column='Id', value=ids)
        categories=self._get_categories(predictions)
        out_df.insert(loc=1, column='DI category', value=categories)
        if self._debug_key is None:
            if out_fn is not None:
                out_df.to_csv(out_fn, index=False, sep ='\t')
        else:
            print(out_df)

    def _get_categories(self, dis):
        out = []
        for di in dis:
            if di > self._di_categories[1]:
                out.append(3)
            elif di > self._di_categories[0]:
                out.append(2)
            else:
                out.append(1)
        return out
