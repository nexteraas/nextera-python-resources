# Adapted from https://github.com/Lailabcode/DeepSP
# Import libraries
from builtins import object
import numpy as np
import pandas as pd
from holoviews import output
from keras.models import model_from_json
import inspect
import os
from deep_sp.anarci_proxy import AnarciProxy


class DeepSP(object):

    def __init__(self, sap_pos_json=None, sap_pos_h5=None, scm_pos_json=None, scm_pos_h5=None,
                 scm_neg_json=None, scm_neg_h5=None):
        self._sap_pos_json = sap_pos_json
        self._sap_pos_h5 = sap_pos_h5
        self._scm_pos_json = scm_pos_json
        self._scm_pos_h5 = scm_pos_h5
        self._scm_neg_json = scm_neg_json
        self._scm_neg_h5 = scm_neg_h5
        loc = inspect.getfile(inspect.currentframe())
        loc = os.path.dirname(loc)
        if self._sap_pos_json is None:
            self._sap_pos_json = os.path.join(loc, 'Conv1D_regressionSAPpos.json')
        if self._sap_pos_h5 is None:
            self._sap_pos_h5 = os.path.join(loc, 'Conv1D_regression_SAPpos.h5')
        if self._scm_pos_json is None:
            self._scm_pos_json = os.path.join(loc, 'Conv1D_regressionSCMpos.json')
        if self._scm_pos_h5 is None:
            self._scm_pos_h5 = os.path.join(loc, 'Conv1D_regression_SCMpos.h5')
        if self._scm_neg_json is None:
            self._scm_neg_json = os.path.join(loc, 'Conv1D_regressionSCMneg.json')
        if self._scm_neg_h5 is None:
            self._scm_neg_h5 = os.path.join(loc, 'Conv1D_regression_SCMneg.h5')
        self._H_inclusion_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                                  '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                                  '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                                  '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
                                  '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
                                  '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
                                  '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
                                  '91', '92', '93', '94', '95', '96', '97', '98', '99', '100',
                                  '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
                                  '111', '111A', '111B', '111C', '111D', '111E', '111F', '111G', '111H',
                                  '112I', '112H', '112G', '112F', '112E', '112D', '112C', '112B', '112A', '112',
                                  '113', '114', '115', '116', '117', '118', '119', '120',
                                  '121', '122', '123', '124', '125', '126', '127', '128']
        self._L_inclusion_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                                  '21', '22', '23', '24', '25', '26', '27', '28', '29', '30',
                                  '31', '32', '33', '34', '35', '36', '37', '38', '39', '40',
                                  '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                                  '51', '52', '53', '54', '55', '56', '57', '58', '59', '60',
                                  '61', '62', '63', '64', '65', '66', '67', '68', '69', '70',
                                  '71', '72', '73', '74', '75', '76', '77', '78', '79', '80',
                                  '81', '82', '83', '84', '85', '86', '87', '88', '89', '90',
                                  '91', '92', '93', '94', '95', '96', '97', '98', '99', '100',
                                  '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
                                  '111', '112', '113', '114', '115', '116', '117', '118', '119', '120',
                                  '121', '122', '123', '124', '125', '126', '127']
        self._H_dict = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9,
                        '11': 10, '12': 11, '13': 12, '14': 13, '15': 14, '16': 15, '17': 16, '18': 17, '19': 18,
                        '20': 19,
                        '21': 20, '22': 21, '23': 22, '24': 23, '25': 24, '26': 25, '27': 26, '28': 27, '29': 28,
                        '30': 29,
                        '31': 30, '32': 31, '33': 32, '34': 33, '35': 34, '36': 35, '37': 36, '38': 37, '39': 38,
                        '40': 39,
                        '41': 40, '42': 41, '43': 42, '44': 43, '45': 44, '46': 45, '47': 46, '48': 47, '49': 48,
                        '50': 49,
                        '51': 50, '52': 51, '53': 52, '54': 53, '55': 54, '56': 55, '57': 56, '58': 57, '59': 58,
                        '60': 59,
                        '61': 60, '62': 61, '63': 62, '64': 63, '65': 64, '66': 65, '67': 66, '68': 67, '69': 68,
                        '70': 69,
                        '71': 70, '72': 71, '73': 72, '74': 73, '75': 74, '76': 75, '77': 76, '78': 77, '79': 78,
                        '80': 79,
                        '81': 80, '82': 81, '83': 82, '84': 83, '85': 84, '86': 85, '87': 86, '88': 87, '89': 88,
                        '90': 89,
                        '91': 90, '92': 91, '93': 92, '94': 93, '95': 94, '96': 95, '97': 96, '98': 97, '99': 98,
                        '100': 99,
                        '101': 100, '102': 101, '103': 102, '104': 103, '105': 104, '106': 105, '107': 106, '108': 107,
                        '109': 108, '110': 109,
                        '111': 110, '111A': 111, '111B': 112, '111C': 113, '111D': 114, '111E': 115, '111F': 116,
                        '111G': 117,
                        '111H': 118,
                        '112I': 119, '112H': 120, '112G': 121, '112F': 122, '112E': 123, '112D': 124, '112C': 125,
                        '112B': 126, '112A': 127, '112': 128,
                        '113': 129, '114': 130, '115': 131, '116': 132, '117': 133, '118': 134, '119': 135, '120': 136,
                        '121': 137, '122': 138, '123': 139, '124': 140, '125': 141, '126': 142, '127': 143, '128': 144}
        self._L_dict = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, '9': 8, '10': 9,
                        '11': 10, '12': 11, '13': 12, '14': 13, '15': 14, '16': 15, '17': 16, '18': 17, '19': 18,
                        '20': 19,
                        '21': 20, '22': 21, '23': 22, '24': 23, '25': 24, '26': 25, '27': 26, '28': 27, '29': 28,
                        '30': 29,
                        '31': 30, '32': 31, '33': 32, '34': 33, '35': 34, '36': 35, '37': 36, '38': 37, '39': 38,
                        '40': 39,
                        '41': 40, '42': 41, '43': 42, '44': 43, '45': 44, '46': 45, '47': 46, '48': 47, '49': 48,
                        '50': 49,
                        '51': 50, '52': 51, '53': 52, '54': 53, '55': 54, '56': 55, '57': 56, '58': 57, '59': 58,
                        '60': 59,
                        '61': 60, '62': 61, '63': 62, '64': 63, '65': 64, '66': 65, '67': 66, '68': 67, '69': 68,
                        '70': 69,
                        '71': 70, '72': 71, '73': 72, '74': 73, '75': 74, '76': 75, '77': 76, '78': 77, '79': 78,
                        '80': 79,
                        '81': 80, '82': 81, '83': 82, '84': 83, '85': 84, '86': 85, '87': 86, '88': 87, '89': 88,
                        '90': 89,
                        '91': 90, '92': 91, '93': 92, '94': 93, '95': 94, '96': 95, '97': 96, '98': 97, '99': 98,
                        '100': 99,
                        '101': 100, '102': 101, '103': 102, '104': 103, '105': 104, '106': 105, '107': 106, '108': 107,
                        '109': 108, '110': 109,
                        '111': 110, '112': 111, '113': 112, '114': 113, '115': 114, '116': 115, '117': 116, '118': 117,
                        '119': 118, '120': 119,
                        '121': 120, '122': 121, '123': 122, '124': 123, '125': 124, '126': 125, '127': 126, '128': 127}
        self._features = ['Name', 'SAP_pos_CDRH1', 'SAP_pos_CDRH2', 'SAP_pos_CDRH3', 'SAP_pos_CDRL1', 'SAP_pos_CDRL2',
                          'SAP_pos_CDRL3', 'SAP_pos_CDR', 'SAP_pos_Hv', 'SAP_pos_Lv', 'SAP_pos_Fv',
                          'SCM_pos_CDRH1', 'SCM_pos_CDRH2', 'SCM_pos_CDRH3', 'SCM_pos_CDRL1', 'SCM_pos_CDRL2',
                          'SCM_pos_CDRL3', 'SCM_pos_CDR', 'SCM_pos_Hv', 'SCM_pos_Lv', 'SCM_pos_Fv',
                          'SCM_neg_CDRH1', 'SCM_neg_CDRH2', 'SCM_neg_CDRH3', 'SCM_neg_CDRL1', 'SCM_neg_CDRL2',
                          'SCM_neg_CDRL3', 'SCM_neg_CDR', 'SCM_neg_Hv', 'SCM_neg_Lv', 'SCM_neg_Fv']

    def run(self, dataset):
        names = dataset['Id'].to_list()
        ds_heavy_seqs = dataset['Heavy_Chain'].to_list()
        ds_light_seqs = dataset['Light_Chain'].to_list()
        heavy_seqs = self._format_sequences(names, ds_heavy_seqs)
        light_seqs = self._format_sequences(names, ds_light_seqs)
        h_sequences, h_numbered, h_alignment_details, h_hit_tables = AnarciProxy.run_anarci(heavy_seqs, h_chain=True)
        l_sequences, l_numbered, l_alignment_details, l_hit_tables = AnarciProxy.run_anarci(light_seqs, h_chain=False)
        aligned_seqs = self._seq_preprocessing(h_sequences, h_numbered, l_numbered)
        name_list = list(aligned_seqs.keys())
        X = list(aligned_seqs.values())
        X = [self._one_hot_encoder(s=x) for x in X]
        X = np.transpose(np.asarray(X), (0, 2, 1))
        X = np.asarray(X)
        loaded_model = self._load_model(self._sap_pos_json, self._sap_pos_h5)
        sap_pos = loaded_model.predict(X)
        loaded_model = self._load_model(self._scm_pos_json, self._scm_pos_h5)
        scm_pos = loaded_model.predict(X)
        loaded_model = self._load_model(self._scm_neg_json, self._scm_neg_h5)
        scm_neg = loaded_model.predict(X)
        df = pd.concat([pd.DataFrame(name_list), pd.DataFrame(sap_pos), pd.DataFrame(scm_pos), pd.DataFrame(scm_neg)],
                       ignore_index=True, axis=1)
        df.columns = self._features
        # if output is not None:
        #     df.to_csv(out_fn, index=False, sep ='\t')
        #     print(df)
        return df

    def _format_sequences(self, names, seqs):
        out = []
        for i in range(len(names)):
            seq_name = names[i]
            seq = seqs[i].upper()
            out.append((seq_name, seq))
        return out

    def _seq_preprocessing(self, names, h_numbered, l_numbered):
        out = {}
        for i in range(len(h_numbered)):
            H_tmp = 145 * ['-']
            L_tmp = 127 * ['-']
            num_h = h_numbered[i][0][0]
            num_l = l_numbered[i][0][0]
            self._enter_aas(num_h, H_tmp, self._H_dict)
            self._enter_aas(num_l, L_tmp, self._L_dict)
            aa_string = ''
            for aa in H_tmp + L_tmp:
                aa_string += aa
            out[names[i][0]] = aa_string
        return out

    def _enter_aas(self, nums, tmp, dct):
        for j in range(0, len(nums)):
            val = nums[j]
            code = val[0]
            aa = val[1]
            pos = code[0]
            pos_x = code[1]
            dict_key = str(pos) + pos_x
            dict_key = dict_key.strip()
            tmp[dct[dict_key]] = aa

    def _one_hot_encoder(self, s):
        d = {'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7, 'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12,
             'Q': 13, 'R': 14, 'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19, '-': 20}
        x = np.zeros((len(d), len(s)))
        x[[d[c] for c in s], range(len(s))] = 1
        return x

    def _load_model(self, model_fn, weights_fn):
        json_file = open(model_fn, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(weights_fn)
        loaded_model.compile(optimizer='adam', loss='mae', metrics=['mae'])
        return loaded_model


class Quartiles(object):
    def __init__(self, fn=None):
        if fn is None:
            loc = inspect.getfile(inspect.currentframe())
            loc = os.path.dirname(loc)
            fn = os.path.join(loc, 'tblS5.csv')
        self._df = pd.read_csv(fn, sep='\t', index_col=0)

    def get_quartile(self, property, value):
        p = self._df.loc[property]
        if value > p['Q3']:
            return 4
        if value > p['Q2']:
            return 3
        if value > p['Q1']:
            return 2
        return 1
