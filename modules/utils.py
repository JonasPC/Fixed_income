import pandas as pd


def to_latex_table(file_name, df, directory=None, index=False):
    """
    Parameters
    ==========
    file_name : name of table (without .tex)
    df : pandas.DataFrame (object) which has to be rendered to latex
    index : should the index of the DataFrame be shown
    """

    if directory is None:
        with open('{}.tex'.format(file_name), 'w') as tf:
            tf.write(df.to_latex(index=index))
    else:
        with open('{}//{}.tex'.format(directory, file_name), 'w') as tf:
            tf.write(df.to_latex(index=index))
