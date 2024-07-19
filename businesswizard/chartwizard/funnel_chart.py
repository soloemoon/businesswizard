import pandas_flavor as pf
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns


@pf.register_dataframe_method
def funnel_chart(
    df,
    x_axis_column: str, 
    label_column: str,
    title: str ='Funnel Chart',
    xmin: int=0,
    xmax: int=100,  
    bar_color: str ='#808B96', 
    text_color: str ='#2A2A2A', 
    fill_color: str='grey'
    ):
    
    """Create bullet chart based on dataframe values.

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import charter
                >>> df.funnel_graph(
                ... x_axis_column = 'value1', 
                ... label_column='category', 
                ... title = 'Chart Title Here'
                ... )  # doctest: +SKIP


            Args:
                df: dataframe containing chart data
                x_axis_column: Column name of the x axis
                label_column: Column name of the labels
                title: Chart title
                xmin: x axis minimum. Default is 0.
                xmax: x axis maximum. Default is 100.
                bar_color: Bar color
                text_color: Text color
                fill_color: Fill color
                
            Returns:
                Matplot Chart object
    """

    x_list = df[x_axis_column].values.tolist()
    y = [*range(1, len(x_list)+1)]
    y.reverse()

    labels = df[label_column].values.tolist()
    x_range = xmax - xmin

    fig, ax = plt.subplots(1, figsize=(12,6))
    for idx, val in enumerate(x_list):
        left = (x_range - val)/2
        plt.barh(y[idx], x_list[idx], left = left, color=bar_color, height=.8)
        # label
        plt.text(50, y[idx]+0.1, labels[idx], ha='center', fontsize=16, color=text_color)
        # value
        plt.text(50, y[idx]-0.3, x_list[idx], ha='center', fontsize=16, color=text_color)
            
        if idx != len(x_list)-1:
            next_left = (x_range - x_list[idx+1])/2
            shadow_x = [left, next_left, 100-next_left, 100-left, left]
                
            shadow_y = [y[idx]-0.4, y[idx+1]+0.4, y[idx+1]+0.4, y[idx]-0.4, y[idx]-0.4]
            plt.fill(shadow_x, shadow_y, color=fill_color, alpha=0.6)
        plt.xlim(xmin, xmax)
        plt.axis('off')
        plt.title(title, loc='center', fontsize=24, color=text_color)
        plt.show()
