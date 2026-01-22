from nextera_phagedisplayanalysis.abpred import benchmark as b
import pandas as pd


class Ranks:
    def __init__(self, benchmark, platform_map, vs_original=True, rank_type='min', normalize_ranks=True, round_ranks=True):
        self._benchmark = benchmark
        self._vs_original =  vs_original
        self._rank_type = rank_type
        self._normalize_ranks = normalize_ranks
        self._round_ranks = round_ranks
        self._map = platform_map
        # self._map['AS']='ACCSTAB'
        # self._map['AC'] = 'ACSINS'
        # self._map['BVP'] = 'BVPELISA'
        # self._map['CSI'] = 'CSIBLI'
        self._inverse_ranks = []
        self._inverse_ranks.append('SGAC')
        self._inverse_ranks.append('HEK')
        self._inverse_ranks.append('DSF')
        self._transformed_platforms=[]
        self._transformed_platforms.append('AC')
        self._transformed_platforms.append('CSI')
        self._transformed_platforms.append('CIC')
        self._transformed_platforms.append('SMAC')
        self._threshold = {}
        self._threshold['PSR'] = 0.27
        self._threshold['AC'] = 11.2
        self._threshold['CSI'] = 0.01
        self._threshold['CIC'] = 10.1
        self._threshold['HIC'] = 11.7
        self._threshold['SMAC'] = 12.8
        self._threshold['SGAC'] = 370
        self._threshold['BVP'] = 4.3
        self._threshold['ELISA'] = 1.9
        self._threshold['AS'] = 0.08

    def calculate(self, predicitions_df):
        out=[]
        platforms=self._benchmark.get_data()['label'].unique()
        abs = predicitions_df['Ab'].unique()
        for platform in platforms:
            inc_rank = False
            if platform in self._inverse_ranks:
                inc_rank=True
            for ab in abs:
                # if platform=='CIC' and ab=='Dupixent':
                #     ffg=""
                pred_value, rank = self._calculate(platform, ab, predicitions_df, invert_rank=inc_rank,
                                       normalize=self._normalize_ranks, round_to_int=self._round_ranks)
                if rank is not None:
                    warning = self._get_warning(platform, pred_value)
                    result=[ab, platform, rank, warning]
                    out.append(result)
        out = pd.DataFrame(out, columns=['Name', 'Platform', 'Rank', 'Comment'])
        return out

    def _calculate(self, platform, ab, predicitions_df, invert_rank=False, normalize=False, round_to_int=False):
        df=self._benchmark.get_data()
        mask = df['label'] == platform
        filtered_df = df[mask]
        if self._map.get(platform) is None:
            pred_platform=platform
        else:
            pred_platform = self._map[platform]
        pred_df = predicitions_df[predicitions_df['Ab'] == ab]
        pred_df = pred_df[pred_df['Platform']==pred_platform]
        if len(pred_df)==0:
            return None, None
        filtered_df = filtered_df.copy()
        pred_value = pred_df['Prediction'].iloc[0]
        new_row_data = [ab, ab, pred_value, pred_value, pred_value, platform]
        new_rows_df = pd.Series(new_row_data, index=df.columns)
        new_rows_df = pd.DataFrame([new_rows_df])
        filtered_df = pd.concat([filtered_df, new_rows_df], ignore_index=True)
        last_index = filtered_df.index[-1]
        if platform in self._transformed_platforms:
            rank_col = 'pred'
        else:
            if self._vs_original:
                rank_col = 'original'
            else:
                rank_col = 'pred'
        ranks = filtered_df[rank_col].rank(method=self._rank_type).astype(int)
        out = ranks[last_index]
        if invert_rank:
            out = (max(ranks)+1) -out
        if normalize:
            out = (out/max(ranks)) * 100
        if round_to_int:
            out = round(out)
        return pred_value, out

    def _get_warning(self, platform, value):
        out = None
        if self._threshold.get(platform) is None:
            out = ''
        else:
            t = self._threshold.get(platform)
            if platform in self._transformed_platforms:
                out = ''
            else:
                if platform in self._inverse_ranks:
                    if value <= t:
                        out = 'Warning'
                    else:
                        out = 'Safe'
                else:
                    if value >= t:
                        out = 'Warning'
                    else:
                        out = 'Safe'
        return out

