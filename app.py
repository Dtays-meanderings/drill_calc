import plotly.graph_objects as go

#torque data
pkw_range_h = [3.15, 80, 80]
rpm_range_h = [8,205, 3150]
pkw_range_l = [2.5,63, 63]
rpm_range_l = [8,205, 3150]

#tickvals
pkw_map = [0,2.5,3.15,4,5,6.3,8,10,12.5,16,20,25,31.5,40,50,63,80,100]
rpms_map = [0,8,10,12.5,16,20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000]


fig = go.Figure()
# Create and style traces
fig.add_trace(go.Scatter(x=rpm_range_h, y=pkw_range_h, name=' 40% Duty',
                         line = dict(color='firebrick', width=4, dash='dot')))
fig.add_trace(go.Scatter(x=rpm_range_l, y=pkw_range_l, name='100% Duty',
                         line=dict(color='royalblue', width=4)))
#Add line
fig.add_shape( # add "target" line
    type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    x0=0, x1=4, xref="x", y0=0, y1=70, yref="y"
)

fig.update_layout(
    autosize=True,
    yaxis=dict(
        type="log",
        range=[0,100],
        tickvals=pkw_map,
        nticks=8,
        autorange=True
    )
)
fig.update_layout(
    autosize=True,
    xaxis=dict(
        type="log",
        range=[0,5000],
        tickvals=rpms_map,
        nticks=8,
        autorange=True
    )
)
# Edit the layout
fig.update_layout(template= "plotly_dark", title='Torque',
                   xaxis_title='M65 S1 - RPM',
                   yaxis_title='Power [kw]')


# Add image
fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/Dtays-meanderings/drill_calc/master/Tool%201.png",
        xref="paper", yref="paper",
        name="Single Flute",
        x=1.25, y=.05,
        sizex=0.5, sizey=0.5,
        xanchor="right", yanchor="bottom"
    )
)

fig.show()
