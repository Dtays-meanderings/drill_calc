# -*- coding: utf-8 -*-
"""
This is drilling a torque chart for WFL M65 S1 spindle
TODO:All of it...
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import math

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        dcc.Graph(id="graph-output"),
        # Top row
        html.Div([
            html.Div([dcc.Markdown('Feed in mmpr  \n fn'),dcc.Input(id="fn_feed", value="0.15", size="5",type="number")]),
            html.Div([dcc.Markdown('Cutting speed  \n Vc'),dcc.Input(id="Vc_mpm", value="120", size="5",type="number")]),
            html.Div([dcc.Markdown('Material coeff  \n Mc'),dcc.Input(id="Mc_tmod", value="0.25", size="5",type="number")]),
            html.Div([dcc.Markdown('Drill Ø  \n Dc'),dcc.Input(id="Dc_dia", value="80", size="5",type="number")]),
            html.Div([dcc.Markdown('Specific cut force  \n Kc'),dcc.Input(id="Kc_Cforce", value="1500", size="5",type="number")]),
        ],style=dict(display='flex', width=400,verticalAlign = "middle")),
        # Bottom row
        html.Div([
            html.Div([dcc.Markdown('Machine efficiency  \n Meff'),dcc.Input(id="mach_eff", value="0.75", size="5",type="number")]),
            html.Div([dcc.Markdown('Number of teeth   \n fz'),dcc.Input(id="fz_tno", value="2", size="5",type="number")]),
            html.Div([dcc.Markdown('Drill tip angle  \n KAPR'),dcc.Input(id="KAPR", value="59", size="5",type="number")]),
            html.Div([dcc.Markdown('Cut edge rake angle  \n Yo'),dcc.Input(id="Yo_ang", value="15", size="5",type="number")]),
        ],style=dict(display='flex', width=400,verticalAlign = "middle")),
        html.Div(id="number-output"),
    ]
)


@app.callback(
    Output("number-output", "children"),
    Output("graph-output", "figure"),
    [Input("fn_feed", "value"),
    Input("Vc_mpm", "value"),
    Input("Mc_tmod", "value"),
    Input("Dc_dia", "value"),
    Input("Kc_Cforce", "value"),
    Input("mach_eff", "value"),
    Input("fz_tno", "value"),
    Input("KAPR", "value"),
    Input("Yo_ang", "value"),
    ],
)


def update_output(_fn, _Vc, _Mc, _Dc, _Kc, _Meff, _fz, _KAPR, _Yo):
#setup    
    #Redef to float
    fn   = float(_fn)
    Vc   = float(_Vc)
    Mc   = float(_Mc)
    Dc   = float(_Dc)
    Kc   = float(_Kc)
    Meff = float(_Meff)
    fz   = float(_fz)
    KAPR = float(_KAPR)
    Yo   = float(_Yo) 
    
    #extra vars
    Z_daN       = 3000  #@param {type: "number"} #Force available @ Z
    X_daN       = 2000  #@param {type: "number"} #Force available @ X
    HB          = 210   #@param {type: "number"} #Hardness in brinell(Sumitool spec)

#Calculate Power & Force
    pi=math.pi
    #rpm @ mmpm
    rpm1=(Vc*1000)/(Dc*pi)

    #Accurate specific cutting force per Sandvik
    Kc1 = Kc * (fz * math.sin(KAPR))**Mc * (1 - Yo / 100)
    #print('Accurate specific cutting force per Sandvik[N/mm^2]')
    
    #kw consumption per Sandvik
    pkw1 = (( fn * Vc * Dc * Kc1 ) / (240 * 10**3)) * fz * Meff
    #print('\nPower consumption per Sandvik[kw]')
    
    #tiddy numbers
    rpm1=round(rpm1)
    pkw1=round(pkw1,2)

    #S1 motor data - pkw = Y axis | rpm = X axis
    pkw_range_l = [2.5,63, 63]
    rpm_range_l = [8,205, 3150]
    pkw_range_h = [3.15, 80, 80]
    rpm_range_h = [8,205, 3150]
    m42_pkw_range_l = [2.5,63]
    m42_rpm_range_l = [31.5,810]
    m42_pkw_range_h = [3.15,80]
    m42_rpm_range_h = [31.5,810]

    figure = go.Figure(go.Scatter(# add calculated input here
                         x=[0,rpm1,rpm1], y=[pkw1,pkw1,0], name='Ø(RPM, kW)',
                         line=dict(color='LightSkyBlue', width=4, dash='dot')))
                         #Trace power @ motor
    figure.add_trace(go.Scatter(# M1=41 info low range
                             x=rpm_range_h, y=pkw_range_h, name='M41 40% Duty',
                             line = dict(color='firebrick', width=4, dash='dot')))
    figure.add_trace(go.Scatter(x=rpm_range_l, y=pkw_range_l, name='M41 100% Duty',
                             line=dict(color='royalblue', width=4)))

    figure.add_trace(go.Scatter(# M1=42 info high range
                             x=m42_rpm_range_h, y=m42_pkw_range_h, name='M42 40% Duty',
                             line = dict(color='firebrick', width=4, dash='dot')))
    figure.add_trace(go.Scatter(x=m42_rpm_range_l, y=m42_pkw_range_l, name='M42 100% Duty',
                         line=dict(color='royalblue', width=4)))
    
    #Update layout to logarithmic scale and resize
    pkw_map = [2.5,3.15,4,5,6.3,8,10,12.5,16,20,25,31.5,40,50,63,80,100] #tickvals maps axis data
    rpms_map = [8,10,12.5,16,20,25,31.5,40,50,63,80,100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000]

    figure.update_layout(
        autosize=True,
        yaxis=dict(
            type="log",
            tickvals=pkw_map,
            autorange=True
        )
    )
    figure.update_layout(
        autosize=True,
        # width = 1000,
        height = 800,
        xaxis=dict(
            type="log",
            tickvals=rpms_map,
            autorange=True
        )
    )

    num1 = [_fn, _Vc, _Mc, _Dc, _Kc, _Meff, _fz, _KAPR, _Yo, Kc1]
    numout = " | ".join((str(val) for val in num1 if val))

    return numout, figure

app.run_server(debug=True, use_reloader=False) 
