
import plotly.graph_objs as go
import plotly.offline as opy
import pandas as pd
from models import *
from datetime import timedelta, datetime


def job_search_funnel_plot(user_id):
    """
    Creates a funnel chart showing the status of a user's job search

    Args:
    - user_id: the id of the user

    Returns:
    - a string containing the HTML code for the funnel chart
    """
    # Get the count of jobs in each status category for the user
    wishlist_count = Job.query.filter(
        Job.status == 'Wishlist', Job.user_id == user_id).count()
    applied_count = Job.query.filter(
        Job.status == 'Applied', Job.user_id == user_id).count()
    interview_count = Job.query.filter(
        Job.status == 'Interview', Job.user_id == user_id).count()
    offer_count = Job.query.filter(
        Job.status == 'Offer', Job.user_id == user_id).count()
    rejected_count = Job.query.filter(
        Job.status == 'Rejected', Job.user_id == user_id).count()

    # Create the funnel chart data
    data = [go.Funnel(x=[wishlist_count, applied_count, interview_count, offer_count, rejected_count],
                      y=['Wishlist', 'Applied', 'Interview', 'Offer', 'Rejected'], opacity=0.65, marker={
        "color": ["#efcf1c", "#f37236", "#16b3b9", "#62aa5a", "#f45c64"]})]

    # Create the layout
    layout = go.Layout(title='Funnel Chart', xaxis_title='Count')

    # Create the figure
    fig = go.Figure(data=data, layout=layout,)

    # Plot the figure using plotly.offline.plot
    plot_html = opy.plot(fig, auto_open=False, output_type='div')

    return plot_html


def job_time_bar(jobs, frequency):
    """
    Generate a bar chart of the number of jobs created over time.

    Args:
        jobs (list): A list of Job objects.
        frequency (str): The frequency of the time intervals to use for grouping the jobs.
            Valid values are 'daily', 'weekly', 'monthly', or 'yearly'.

    Returns:
        str: An HTML string containing the plotly graph.

    Raises:
        ValueError: If the frequency argument is not one of the expected values.

    """
    print(jobs[0].created_at)
    # Get the created_at dates
    created_at_dates = [job.created_at for job in jobs]
    # print('************careated_at', type(created_at_dates[0]))
    # Check if created_at_dates is empty
    if not created_at_dates:
        return None

    # Check if the frequency argument is valid
    if frequency not in ['daily', 'weekly', 'monthly', 'yearly']:
        raise ValueError(
            f"Invalid frequency argument: {frequency}. Valid values are 'daily', 'weekly', 'monthly', or 'yearly'.")

    # # Convert the times to datetime objects
    # times = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    #          for t in created_at_dates]

    # Create a DataFrame to store the jobs and times
    df = pd.DataFrame({'jobs': jobs, 'times': created_at_dates})
    df['times'] = pd.to_datetime(df['times'])

    # Define the layout of the graph
    layout = go.Layout(
        title='Jobs Created Over Time',
        xaxis=dict(title='Time Interval', tickformat='%Y-%m-%d',
                   showgrid=True, zeroline=False, type="date",),
        yaxis=dict(title='Number of Jobs')
    )

    # Define the traces for the different time intervals
    daily_trace = go.Bar(x=df['times'].dt.strftime('%Y-%m-%d').value_counts().index,
                         y=df['times'].dt.strftime(
                             '%Y-%m-%d').value_counts().values,
                         name='Daily',
                         visible=True,
                         showlegend=False
                         )
    weekly_trace = go.Bar(x=df['times'].dt.dayofweek.apply(lambda x: df['times'].min() - pd.Timedelta(days=x)).dt.strftime('%Y-%m-%d').value_counts().index,
                          y=df['times'].dt.strftime(
                              '%Y-%m-%d').value_counts().values,
                          name='Weekly',
                          visible=False,
                          showlegend=False
                          )
    monthly_trace = go.Bar(x=df['times'].dt.strftime('%Y-%m').value_counts().index,
                           y=df['times'].dt.strftime(
                               '%Y-%m').value_counts().values,
                           name='Monthly',
                           visible=False,
                           showlegend=False
                           )
    yearly_trace = go.Bar(x=df['times'].dt.year.value_counts().index,
                          y=df['times'].dt.year.value_counts().values,
                          name='Yearly',
                          showlegend=False,
                          visible=False,
                          )

    # Define the data for the graph and the buttons to switch between traces
    data = [daily_trace, weekly_trace, monthly_trace, yearly_trace]

    updatemenus = list([
        dict(type='buttons',
             showactive=True,
             direction='right',
             buttons=list([
                 dict(label='Daily',
                      method='update',
                      args=[{'visible': [True, False, False, False]}]),
                 dict(label='Weekly',
                      method='update',
                      args=[{'visible': [False, True, False, False]}]),
                 dict(label='Monthly',
                      method='update',
                      args=[{'visible': [False, False, True, False]}]),
                 dict(label='Yearly',
                      method='update',
                      args=[{'visible': [False, False, False, True]}])
             ]),
             x=0.1,
             y=1.15,
             xanchor='left',
             yanchor='top'
             )
    ])

    layout['updatemenus'] = updatemenus
    # Create the figure
    fig = go.Figure(data=data, layout=layout)

    # Generate the HTML code for the plot using plotly.offline.plot
    plot_html = opy.plot({'data': data, 'layout': layout},
                         auto_open=False, output_type='div')

    return plot_html
