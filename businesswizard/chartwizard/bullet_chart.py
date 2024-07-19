import pandas_flavor as pf
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
from typing import List, Tuple

@pf.register_dataframe_method
def bullet_graph(
    df: pd.DataFrame,
    category_column: str,
    category_value_column: str,
    target_value_column: str,
    limits: List[int] = [20, 40, 80, 100],
    labels: List[str] = ['Poor', 'Ok', 'Good', 'Excellent'],
    axis_label: str = 'Metric',
    title: str = 'Bullet Graph',
    size: Tuple[int] = (5, 3),
    palette_color: str = 'green',
    formatter: str = None,
    target_color: str = "gray",
    bar_color: str = "black",
    label_color: str = "black"
):
   
    """
    Create bullet chart based on dataframe values.

            Examples:
                Functional usage

                >>> import pandas as pd
                >>> from bizwiz import charter
                >>> df.bullet_graph(
                ... category_column = 'category', 
                ... category_value_column='category_val', 
                ... target_value_column='target_val', 
                ... limits=[20, 40, 80, 100]
                ... )  # doctest: +SKIP


            Args:
                df: dataframe containing chart data
                category_column: Column name of the category value
                category_value_column: Column name of the values associated with the category
                target_value_column: Column name of the values that are targeted for the category column
                limits: List of x axis values. e.g. [100, 120, 140, 150]
                labels: List of values associated with what the limits mean. e.g. [Poor, ok, good, excellent]
                axis_label: X axis label name. Default is Metric.
                title: Chart title
                size: Size of chart
                palette_color: Diverging color to apply to the chart. Default is green. Lighter to Darker.
                formatter: formats tick as string
                target_color: Color of the target variable
                bar_color: Color of the bars
                label_color: Color of the labelss

            Returns:
                Matplot Chart object
    """

    # Convert dataframe to a list of tuples for code to run.
    dt = list(df[[category_column, category_value_column, target_value_column]].itertuples(index=False, name=None))

    # Determine the max value for adjusting the bar height
    h = limits[-1] / 10

    # Use the 
    palette = sns.light_palette(palette_color, len(limits), reverse=False)

    # Must be able to handle one or many data sets via multiple subplots
    if len(dt) == 1:
        fig, ax = plt.subplots(figsize=size, sharex=True)
    else:
        fig, axarr = plt.subplots(len(dt), figsize=size, sharex=True)

        # Add each bullet graph bar to a subplot
    for idx, item in enumerate(dt):

        # Get the axis from the array of axes returned when the plot is created
        if len(dt) > 1:
            ax = axarr[idx]

            # Formatting to get rid of extra marking clutter
            ax.set_aspect('equal')
            ax.set_yticklabels([item[0]])
            ax.set_yticks([1])
            ax.spines['bottom'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)

            prev_limit = 0
            for idx2, lim in enumerate(limits):
                # Draw the bar
                ax.barh([1], lim - prev_limit, left=prev_limit, height=h,
                        color=palette[idx2])
                prev_limit = lim
            rects = ax.patches
            # The last item in the list is the value we're measuring
            # Draw the value we're measuring
            ax.barh([1], item[1], height=(h / 3), color=bar_color)

            # Need the ymin and max in order to make sure the target marker
            # fits
            ymin, ymax = ax.get_ylim()
            ax.vlines(
                item[2], ymin * .9, ymax * .9, linewidth=1.5, color=target_color)

        # Now make some labels
        if labels is not None:
            for rect, label in zip(rects, labels):
                height = rect.get_height()
                ax.text(
                    rect.get_x() + rect.get_width() / 2,
                    -height * .4,
                    label,
                    ha='center',
                    va='bottom',
                    color=label_color)
        if formatter:
            ax.xaxis.set_major_formatter(formatter)
        if axis_label:
            ax.set_xlabel(axis_label)
        if title:
            fig.suptitle(title, fontsize=14)
        g = fig.subplots_adjust(hspace=0)

        return g
