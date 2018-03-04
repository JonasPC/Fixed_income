import pandas as pd


def to_latex_table(file_name, df, index=False):
    """
    Parameters
    ==========
    file_name : name of table (without .tex)
    df : pandas.DataFrame (object) which has to be rendered to latex
    index : should the index of the DataFrame be shown
    """

    with open('{}.tex'.format(file_name), 'w') as tf:
        tf.write(df.to_latex(index=index))
