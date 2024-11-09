import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import sys
import matplotlib as mpl


BINDING_RATIO_TEXT='Binding ratio'

def merge_data(s_d_df, d_df, b_r_df):
    ids = s_d_df['Sequence id'].unique()
    tmp = {}
    for id in ids:
        values = []
        row = s_d_df.loc[s_d_df['Sequence id'] == id]
        a = row.get('Samples').values[0]
        row = d_df.loc[d_df['Sequence id'] == id]
        b = row['Frequency'].values[0]
        row = b_r_df.loc[b_r_df['Sequence id'] == id]
        c = row.get('Value').values[0]
        values.append(a)
        values.append(b)
        values.append(c)
        tmp[id] = values
    df=pd.DataFrame.from_dict(tmp, orient='index', columns=['Samples','Frequency','Binding ratio'])
    df['Sequence id'] = df.index
    df['Seq id'] = df['Sequence id'].str.slice(0, 4) + '...'
    return df

def plot_barplot(df, palette_name, title):
    df=df.sort_values('Samples', ascending=False)
    fig = plt.figure(figsize=(8, 6))
    ax = sns.barplot(x='Seq id', y='Samples', data=df, palette=palette_name, hue='Binding ratio', dodge=False)
    plt.xticks(rotation=90, fontfamily='Courier New')
    ax.legend_.remove()
    plt.yscale('log')
    ax.set_title(title)
    plt.ylabel("No. of colonies")
    plt.xlabel("Sequences")
    vmax = max(df['Binding ratio'])
    vmin = min(df['Binding ratio'])
    mappable = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin, vmax), cmap=palette_name)
    fig.colorbar(mappable, ax=ax, orientation='vertical', label=BINDING_RATIO_TEXT)
    ax.set_ylim([0, 100000])
    spacing = 0.2
    fig.subplots_adjust(bottom=spacing)
    plt.show()

def plot_scatterplot(df, palette_name):
    fig=plt.figure()
    ax=sns.scatterplot(x="Binding ratio", y="Frequency", data=df,
                       palette=palette_name, hue='Binding ratio')
    vmax = max(df['Binding ratio'])
    vmin = min(df['Binding ratio'])
    mappable = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin, vmax), cmap=palette_name)
    fig.colorbar(mappable, ax=ax, orientation='vertical', label=BINDING_RATIO_TEXT)
    plt.yscale('log')
    ax.legend_.remove()
    ax.set_ylim([0.0001, 1])
    plt.ylabel("Clone frequency")
    plt.show()

def main(sampling_depth, frequencies, binding_ratios, palette_name='rocket', title=''):
    s_d_df = pd.read_csv(sampling_depth, sep='\t')
    d_df=pd.read_csv(frequencies, sep='\t')
    b_r_df=pd.read_csv(binding_ratios, sep='\t')
    df = merge_data(s_d_df, d_df, b_r_df)
    plot_barplot(df, palette_name, title)
    plot_scatterplot(df, palette_name)


if __name__ == "__main__":
    debug=True
    if debug :
        sampling_depth = 'C:/temp/python/sampling_depth.txt'
        frequencies = 'C:/temp/python/frequencies.txt'
        binding_ratios = 'C:/temp/python/binding_ratios.txt'
        palette_name = 'rocket'
        title = 'MAGE binders (a=0.99)'
        main(sampling_depth, frequencies, binding_ratios, palette_name, title)
    elif len(sys.argv)<2:
        print('Usage: python colony_count_figures.py <sampling_depth.csv> <frequency.csv> <binding_ratio.csv> <palette name> <"Figure title">')
        print('For instance: python colony_count_figures.py sampling_depth.txt frequencies.txt binding_ratios.txt cool "some title"')
        print('For palette names, see: https://matplotlib.org/stable/users/explain/colors/colormaps.html')
        print('or: https://seaborn.pydata.org/tutorial/color_palettes.html')
    else:
        sampling_depth = sys.argv[1]
        frequencies = sys.argv[2]
        binding_ratios = sys.argv[3]
        palette_name=sys.argv[4]
        title=sys.argv[5]
        main(sampling_depth, frequencies, binding_ratios, palette_name, title)

