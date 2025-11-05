from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize app with Bootstrap theme
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css'])

server = app.server

# Add custom CSS for checkbox styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            
            /* Custom checkbox styling */
            .custom-checkbox input[type="checkbox"] {
                width: 14px;
                height: 14px;
                margin-right: 4px;
                accent-color: #002E79;
                cursor: pointer;
            }
            
            .custom-checkbox label {
                cursor: pointer;
                transition: color 0.2s ease;
                font-weight: 500;
                color: #495057;
            }
            
            .custom-checkbox label:hover {
                color: #002E79;
            }
            
            /* Checked state styling */
            .custom-checkbox input[type="checkbox"]:checked + label {
                color: #002E79;
                font-weight: 600;
            }
            
            /* Filter section headers */
            .filter-header {
                border-bottom: 2px solid #dee2e6;
                padding-bottom: 3px;
                font-size: 11px;
                margin: 0 0 5px 0;
                font-weight: 600;
                color: #495057;
                letter-spacing: 0.5px;
            }
            
            /* Sidebar styling */
            .sidebar-filters {
                background-color: #f5f5f5;
                border-right: 2px solid #000;
            }
            
            /* Checkbox container styling */
            .filter-group {
                background-color: white;
                padding: 8px;
                border-radius: 0px;
                margin-bottom: 8px;
                border-top: 2px solid #000;
                border-bottom: 2px solid #000;
                border-left: 1px solid #ccc;
                border-right: 1px solid #ccc;
            }
            
            /* Box styling */
            .chart-box {
                background-color: white;
                border: 2px solid #000;
                padding: 0;
                height: 100%;
            }
            
            .box-header {
                text-align: center !important;
                padding: 8px !important;
                margin: 0 !important;
            }
            
            /* Source box styling */
            .source-box {
                background-color: white;
                border: 2px solid #000;
                padding: 8px;
                text-align: center;
                font-size: 9px;
                line-height: 1.4;
            }
            
            .source-box a {
                color: #002E79;
                text-decoration: none;
                font-weight: 600;
            }
            
            .source-box a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Load data from CSV
df = pd.read_csv('international students data.csv')

# Extract unique values for filters
states = df['State'].unique() if 'State' in df.columns else ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
industries = df['Industry'].unique() if 'Industry' in df.columns else ['Health', 'STEM', 'Social Sc.', 'Design', 'Business', 'Education', 'Prof. Serv', 'Services']
years = sorted(df['Year'].unique()) if 'Year' in df.columns else [2022, 2023, 2024]

# Dashboard layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('INTERNATIONAL STUDENT EMPLOYABILITY DASHBOARD - AUSTRALIA',
                style={'textAlign': 'center', 'color': 'white', 'margin': '0', 'padding': '12px',
                       'backgroundColor': '#002E79', 'fontSize': '22px', 'fontWeight': '700'})
    ]),
    
    # Visa Funnel Section
    html.Div([
        html.H2('OVERALL VISA FUNNEL - BREAKDOWN',
                style={'textAlign': 'center', 'backgroundColor': '#5288E0', 'color': 'white',
                       'margin': '0', 'padding': '8px', 'fontSize': '15px', 'fontWeight': '600'})
    ]),
    
    # KPI Cards Row
    html.Div([
        html.Div([
            html.Div('STUDENT VISA APPLICATIONS', style={'fontSize': '9px', 'marginBottom': '2px', 'color': '#666', 'fontWeight': '600'}),
            html.Div(id='kpi-visa-apps', style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#002E79'})
        ], style={'width': '19%', 'display': 'inline-block', 'textAlign': 'center', 
                  'padding': '8px', 'margin': '2px', 'backgroundColor': 'white', 'border': '2px solid #000'}),
        
        html.Div([
            html.Div('POST-STUDY WORK', style={'fontSize': '9px', 'marginBottom': '2px', 'color': '#666', 'fontWeight': '600'}),
            html.Div(id='kpi-post-study', style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#002E79'})
        ], style={'width': '19%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '8px', 'margin': '2px', 'backgroundColor': 'white', 'border': '2px solid #000'}),
        
        html.Div([
            html.Div('JOB PLACEMENT', style={'fontSize': '9px', 'marginBottom': '2px', 'color': '#666', 'fontWeight': '600'}),
            html.Div(id='kpi-job-placement', style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#002E79'})
        ], style={'width': '19%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '8px', 'margin': '2px', 'backgroundColor': 'white', 'border': '2px solid #000'}),
        
        html.Div([
            html.Div('SKILLED VISA APPLICATIONS', style={'fontSize': '9px', 'marginBottom': '2px', 'color': '#666', 'fontWeight': '600'}),
            html.Div(id='kpi-skilled-visa', style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#002E79'})
        ], style={'width': '19%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '8px', 'margin': '2px', 'backgroundColor': 'white', 'border': '2px solid #000'}),
        
        html.Div([
            html.Div('PR GRANT', style={'fontSize': '9px', 'marginBottom': '2px', 'color': '#666', 'fontWeight': '600'}),
            html.Div(id='kpi-pr-grant', style={'fontSize': '26px', 'fontWeight': 'bold', 'color': '#002E79'})
        ], style={'width': '19%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '8px', 'margin': '2px', 'backgroundColor': 'white', 'border': '2px solid #000'}),
    ], style={'textAlign': 'center', 'marginBottom': '5px', 'marginTop': '3px'}),
    
    # Main Content Row
    html.Div([
        # Left Sidebar - Filters
        html.Div([
            # Location Filter
            html.Div([
                html.H4('LOCATION', className='filter-header'),
                html.Div([
                    dcc.Checklist(
                        id='location-filter',
                        options=[{'label': 'ALL', 'value': 'ALL'}] + 
                                [{'label': state, 'value': state} for state in ['TAS', 'VIC', 'NSW', 'NT', 'SA', 'WA', 'QLD', 'ACT']],
                        value=['ALL'],
                        labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                        className='custom-checkbox'
                    ),
                ]),
            ], className='filter-group'),
            
            # Industries Filter
            html.Div([
                html.H4('INDUSTRIES', className='filter-header'),
                html.Div([
                    dcc.Checklist(
                        id='industry-filter-all',
                        options=[{'label': 'ALL', 'value': 'ALL'}],
                        value=['ALL'],
                        labelStyle={'display': 'inline-block', 'marginRight': '10px', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='industry-filter1',
                        options=[{'label': ind, 'value': ind} for ind in ['Health', 'STEM']],
                        value=[],
                        labelStyle={'display': 'inline-block', 'marginRight': '10px', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='industry-filter2',
                        options=[{'label': ind, 'value': ind} for ind in ['Social Sc.', 'Design']],
                        value=[],
                        labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='industry-filter3',
                        options=[{'label': ind, 'value': ind} for ind in ['Business', 'ED.']],
                        value=[],
                        labelStyle={'display': 'inline-block', 'marginRight': '10px', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='industry-filter4',
                        options=[{'label': ind, 'value': ind} for ind in ['Prof. Serv', 'SERV.']],
                        value=[],
                        labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                        className='custom-checkbox'
                    ),
                ]),
            ], className='filter-group'),
            
            # Study Level Filter
            html.Div([
                html.H4('STUDY LEVEL', className='filter-header'),
                html.Div([
                    dcc.Checklist(
                        id='study-filter',
                        options=[
                            {'label': 'ALL', 'value': 'ALL'},
                            {'label': 'UG', 'value': 'UG'}
                        ],
                        value=['ALL'],
                        labelStyle={'display': 'inline-block', 'marginRight': '10px', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='study-filter2',
                        options=[
                            {'label': 'PG - COURSEWORK', 'value': 'PG-C'}
                        ],
                        value=[],
                        labelStyle={'display': 'block', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='study-filter3',
                        options=[
                            {'label': 'PG - RESEARCH', 'value': 'PG-R'}
                        ],
                        value=[],
                        labelStyle={'display': 'block', 'fontSize': '10px'},
                        className='custom-checkbox'
                    ),
                ]),
            ], className='filter-group'),
            
            # Employment Type Filter
            html.Div([
                html.H4('EMPLOYMENT TYPE', className='filter-header'),
                html.Div([
                    dcc.Checklist(
                        id='employment-filter',
                        options=[
                            {'label': 'ALL', 'value': 'ALL'},
                            {'label': 'FULL-TIME', 'value': 'FT'}
                        ],
                        value=['ALL'],
                        labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                        className='custom-checkbox',
                        style={'marginBottom': '2px'}
                    ),
                    dcc.Checklist(
                        id='employment-filter2',
                        options=[
                            {'label': 'PART-TIME', 'value': 'PT'},
                            {'label': 'CASUAL', 'value': 'CAS'}
                        ],
                        value=[],
                        labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                        className='custom-checkbox'
                    ),
                ]),
            ], className='filter-group'),
            
            # Year Filter
            html.Div([
                html.H4('YEAR', className='filter-header'),
                dcc.Checklist(
                    id='year-filter',
                    options=[{'label': 'ALL', 'value': 'ALL'}] +
                            [{'label': str(year), 'value': str(year)} for year in years],
                    value=['ALL'],
                    labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                    className='custom-checkbox'
                ),
            ], className='filter-group'),
            
        ], className='sidebar-filters', style={'width': '13%', 'display': 'inline-block', 'verticalAlign': 'top',
                  'padding': '8px', 'height': '610px', 'overflowY': 'auto'}),
        
        # Middle Section - Maps
        html.Div([
            # Regional Split
            html.Div([
                html.H3('REGIONAL SPLIT - NO. OF INTL. STUDENTS',
                       className='box-header',
                       style={'backgroundColor': '#5288E0', 'color': 'white', 
                              'fontSize': '11px', 'fontWeight': '600'}),
                html.Div([
                    dcc.Graph(id='australia-map', style={'height': '530px'}, config={'displayModeBar': False})
                ], style={'padding': '0px', 'height': '530px'})
            ], className='chart-box', style={'height': '555px', 'marginBottom': '3px'}),
            
        ], style={'width': '36%', 'display': 'inline-block', 'verticalAlign': 'top', 'paddingLeft': '5px'}),
        
        # Middle-Right Section - Nationality
        html.Div([
            html.H3('JOB ACHIEVED - NATIONALITY SPLIT (TOP 10)',
                   className='box-header',
                   style={'backgroundColor': '#5288E0', 'color': 'white',
                          'fontSize': '11px', 'fontWeight': '600'}),
            html.Div([
                dcc.Graph(id='nationality-chart', style={'height': '530px'}, config={'displayModeBar': False})
            ], style={'padding': '0px', 'height': '530px'})
        ], className='chart-box', style={'width': '23%', 'display': 'inline-block', 
                 'verticalAlign': 'top', 'marginLeft': '5px', 'height': '555px'}),
        
        # Right Section - Salary and Demographics
        html.Div([
            # Salary Cards
            html.Div([
                html.Div([
                    html.Div('Median Salary', style={'fontSize': '9px', 'color': 'white', 'marginBottom': '2px', 'fontWeight': '600'}),
                    html.Div(id='median-salary', style={'fontSize': '16px', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'width': '100%', 'backgroundColor': '#002E79',
                         'padding': '5px', 'textAlign': 'center', 'marginBottom': '3px'}),
                
                html.Div([
                    html.Div('Mean Salary', style={'fontSize': '9px', 'color': 'white', 'marginBottom': '2px', 'fontWeight': '600'}),
                    html.Div(id='mean-salary', style={'fontSize': '16px', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'width': '100%', 'backgroundColor': '#5288E0',
                         'padding': '5px', 'textAlign': 'center'}),
            ], style={'marginBottom': '4px', 'border': '2px solid #000'}),
            
            # Employment Rate and Gender Ratio
            html.Div([
                html.Div([
                    html.H3('EMPLOYMENT RATE', className='box-header', 
                           style={'backgroundColor': '#5288E0', 'color': 'white',
                           'padding': '5px', 'margin': '0', 'fontSize': '10px', 'fontWeight': '600'}),
                    html.Div([
                        dcc.Graph(id='employment-rate', style={'height': '140px'}, config={'displayModeBar': False})
                    ], style={'padding': '3px'})
                ], className='chart-box', style={'width': '48%', 'display': 'inline-block', 
                         'verticalAlign': 'top'}),
                
                html.Div([
                    html.H3('GENDER RATIO', className='box-header',
                           style={'backgroundColor': '#5288E0', 'color': 'white',
                           'padding': '5px', 'margin': '0', 'fontSize': '10px', 'fontWeight': '600'}),
                    html.Div([
                        dcc.Graph(id='gender-ratio', style={'height': '140px'}, config={'displayModeBar': False})
                    ], style={'padding': '3px'})
                ], className='chart-box', style={'width': '48%', 'display': 'inline-block', 
                         'verticalAlign': 'top', 'marginLeft': '4%'}),
            ], style={'marginBottom': '4px'}),
            
            # Migration Reasons
            html.Div([
                html.H3('GRADUATES LEAVING AUSTRALIA%',
                       className='box-header',
                       style={'backgroundColor': '#5288E0', 'color': 'white', 'padding': '5px',
                              'margin': '0', 'fontSize': '10px', 'fontWeight': '600'}),
                html.Div([
                    dcc.Graph(id='migration-reasons', style={'height': '340px'}, config={'displayModeBar': False})
                ], style={'padding': '3px'})
            ], className='chart-box'),
            
        ], style={'width': '27%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '5px'}),
    ], style={'marginTop': '5px'}),
    
    # Source Box - Below all three sections
    html.Div([
        html.Div([
            html.Div('Source: Graduate Outcomes Survey (2024)', 
                    style={'marginBottom': '6px', 'fontWeight': '700', 'color': '#002E79', 'fontSize': '14px'}),
            html.A('Link for in-depth report', 
                   href='https://qilt.edu.au/docs/default-source/default-document-library/2024-gos-international-report.pdf?sfvrsn=168c5da_1',
                   target='_blank',
                   style={'fontSize': '13px', 'color': '#002E79', 'textDecoration': 'none', 'fontWeight': '600'})
        ], className='source-box', style={'width': '86%', 'marginLeft': '0', 'marginTop': '0', 
                                          'padding': '15px', 'textAlign': 'center'})
    ]),
    
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ffffff', 'margin': '0', 'padding': '0', 'height': '100vh', 'overflow': 'hidden'})


# Helper function to combine filter values
def combine_filters(filter_values_list):
    """Combine multiple filter checkbox values"""
    combined = []
    for values in filter_values_list:
        if values:
            combined.extend(values)
    return combined if combined else []


# Helper function to filter data
def filter_data(locations, industries_filter, study_levels, employment_types, years_filter):
    filtered_df = df.copy()
    
    if 'ALL' not in locations and 'State' in df.columns:
        filtered_df = filtered_df[filtered_df['State'].isin(locations)]
    
    if 'ALL' not in industries_filter and 'Industry' in df.columns:
        filtered_df = filtered_df[filtered_df['Industry'].isin(industries_filter)]
    
    if 'ALL' not in study_levels and 'Study_Level' in df.columns:
        filtered_df = filtered_df[filtered_df['Study_Level'].isin(study_levels)]
    
    if 'ALL' not in employment_types and 'Employment_Type' in df.columns:
        filtered_df = filtered_df[filtered_df['Employment_Type'].isin(employment_types)]
    
    if 'ALL' not in years_filter and 'Year' in df.columns:
        years_int = [int(y) for y in years_filter if y != 'ALL']
        filtered_df = filtered_df[filtered_df['Year'].isin(years_int)]
    
    return filtered_df


# Callbacks for KPIs
@app.callback(
    [Output('kpi-visa-apps', 'children'),
     Output('kpi-post-study', 'children'),
     Output('kpi-job-placement', 'children'),
     Output('kpi-skilled-visa', 'children'),
     Output('kpi-pr-grant', 'children')],
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_kpis(loc_all, ind_all, ind1, ind2, ind3, ind4, 
                study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'Visa_Applications' in filtered_df.columns:
        visa_apps_sum = filtered_df['Visa_Applications'].sum()
        if visa_apps_sum >= 1000:
            visa_apps = f"{visa_apps_sum/1000:.0f}K"
        else:
            visa_apps = f"{visa_apps_sum:.0f}"
    else:
        visa_apps = "100K"
    
    if 'Post_Study_Work' in filtered_df.columns:
        post_study_sum = filtered_df['Post_Study_Work'].sum()
        if post_study_sum >= 1000:
            post_study = f"{post_study_sum/1000:.0f}K"
        else:
            post_study = f"{post_study_sum:.0f}"
    else:
        post_study = "30K"
    
    if 'Job_Placement' in filtered_df.columns:
        job_placement_sum = filtered_df['Job_Placement'].sum()
        if job_placement_sum >= 1000:
            job_placement = f"{job_placement_sum/1000:.0f}K"
        else:
            job_placement = f"{job_placement_sum:.0f}"
    else:
        job_placement = "21K"
    
    if 'Skilled_Visa' in filtered_df.columns:
        skilled_visa_sum = filtered_df['Skilled_Visa'].sum()
        if skilled_visa_sum >= 1000:
            if skilled_visa_sum/1000 < 10 and (skilled_visa_sum/1000) % 1 != 0:
                skilled_visa = f"{skilled_visa_sum/1000:.1f}K"
            else:
                skilled_visa = f"{skilled_visa_sum/1000:.0f}K"
        else:
            skilled_visa = f"{skilled_visa_sum:.0f}"
    else:
        skilled_visa = "7.5K"
    
    if 'PR_Grant' in filtered_df.columns:
        pr_grant_sum = filtered_df['PR_Grant'].sum()
        if pr_grant_sum >= 1000:
            pr_grant = f"{pr_grant_sum/1000:.0f}K"
        else:
            pr_grant = f"{pr_grant_sum:.0f}"
    else:
        pr_grant = "7K"
    
    return visa_apps, post_study, job_placement, skilled_visa, pr_grant


# Callback for Australia map
@app.callback(
    Output('australia-map', 'figure'),
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_map(loc_all, ind_all, ind1, ind2, ind3, ind4, 
               study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'State' in filtered_df.columns and 'Student_Count' in filtered_df.columns:
        state_data = filtered_df.groupby('State')['Student_Count'].sum().reset_index()
    else:
        state_data = pd.DataFrame({
            'State': ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'NT', 'ACT'],
            'Student_Count': [15000, 12000, 8000, 6000, 3000, 1500, 1000, 2000]
        })
    
    state_coords = {
        'NSW': (-33.8688, 151.2093), 'VIC': (-37.8136, 144.9631),
        'QLD': (-27.4698, 153.0251), 'WA': (-31.9505, 115.8605),
        'SA': (-34.9285, 138.6007), 'TAS': (-42.8821, 147.3272),
        'NT': (-12.4634, 130.8456), 'ACT': (-35.2809, 149.1300)
    }
    state_data['lat'] = state_data['State'].map(lambda x: state_coords.get(x, (0, 0))[0])
    state_data['lon'] = state_data['State'].map(lambda x: state_coords.get(x, (0, 0))[1])
    
    fig = px.scatter_geo(state_data,
                         lat='lat',
                         lon='lon',
                         size='Student_Count',
                         hover_name='State',
                         hover_data={'Student_Count': True, 'lat': False, 'lon': False},
                         color='Student_Count',
                         color_continuous_scale=['#FFC977', '#F8BD3C', '#E9631D', '#D53223'],
                         size_max=60)
    
    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor='#FFF8E7',
        coastlinecolor='#666',
        projection_type="mercator",
        lonaxis_range=[110, 160],
        lataxis_range=[-45, -10],
        bgcolor='white'
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='white',
        coloraxis_showscale=False,
        height=530
    )
    
    return fig


# Callback for nationality chart
@app.callback(
    Output('nationality-chart', 'figure'),
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_nationality(loc_all, ind_all, ind1, ind2, ind3, ind4, 
                       study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'Nationality' in filtered_df.columns and 'Job_Achieved_Pct' in filtered_df.columns:
        nationality_data = filtered_df.groupby('Nationality')['Job_Achieved_Pct'].mean().reset_index()
        nationality_data = nationality_data.sort_values('Job_Achieved_Pct', ascending=False).head(10)
        nationality_data = nationality_data.sort_values('Job_Achieved_Pct', ascending=True)
    else:
        nationality_data = pd.DataFrame({
            'Nationality': ['Brazil', 'Thailand', 'Malaysia', 'Pakistan', 'South Korea', 
                          'Indonesia', 'Nepal', 'Italy', 'China', 'India'],
            'Job_Achieved_Pct': [62, 62, 62, 63, 63, 63, 69, 69, 72, 75]
        })
    
    fig = px.bar(nationality_data, 
                 x='Job_Achieved_Pct', 
                 y='Nationality',
                 orientation='h',
                 color='Job_Achieved_Pct',
                 color_continuous_scale=['#9BC1FF', '#5288E0', '#002E79'],
                 text='Job_Achieved_Pct')
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='inside', 
                     textfont=dict(size=11, color='white', weight='bold'))
    fig.update_layout(
        xaxis_title='% of Job Achieved',
        yaxis_title='',
        showlegend=False,
        margin=dict(l=5, r=5, t=0, b=20),
        height=530,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(gridcolor='lightgray', title_font=dict(size=10), range=[0, 100], tickfont=dict(size=9)),
        yaxis=dict(tickfont=dict(size=10)),
        coloraxis_showscale=False
    )
    
    return fig


# Callback for salary metrics
@app.callback(
    [Output('median-salary', 'children'),
     Output('mean-salary', 'children')],
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_salary(loc_all, ind_all, ind1, ind2, ind3, ind4, 
                  study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'Salary' in filtered_df.columns and len(filtered_df) > 0:
        median_sal = filtered_df['Salary'].median()
        mean_sal = filtered_df['Salary'].mean()
        median_sal_str = f"${median_sal:,.0f}"
        mean_sal_str = f"${mean_sal:,.0f}"
    else:
        median_sal_str = "$98,000"
        mean_sal_str = "$75,000"
    
    return median_sal_str, mean_sal_str


# Callback for employment rate
@app.callback(
    Output('employment-rate', 'figure'),
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_employment_rate(loc_all, ind_all, ind1, ind2, ind3, ind4, 
                           study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'Employment_Rate' in filtered_df.columns and len(filtered_df) > 0:
        emp_rate = filtered_df['Employment_Rate'].mean()
    else:
        emp_rate = 85
    
    donut_data = pd.DataFrame({
        'Category': ['Employed', 'Unemployed'],
        'Value': [emp_rate, 100 - emp_rate]
    })
    
    fig = px.pie(donut_data, 
                 values='Value', 
                 names='Category',
                 hole=0.7,
                 color='Category',
                 color_discrete_map={'Employed': '#002E79', 'Unemployed': '#e6e6e6'})
    
    fig.update_traces(textinfo='none', showlegend=False)
    
    fig.add_annotation(
        text=f'{emp_rate:.0f}%',
        x=0.5, y=0.5,
        font=dict(size=32, color='#002E79', weight='bold'),
        showarrow=False,
        xref='paper',
        yref='paper'
    )
    
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        height=140,
        paper_bgcolor='white'
    )
    
    return fig


# Callback for gender ratio
@app.callback(
    Output('gender-ratio', 'figure'),
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_gender_ratio(loc_all, ind_all, ind1, ind2, ind3, ind4, 
                        study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'Gender' in filtered_df.columns and 'Student_Count' in filtered_df.columns and len(filtered_df) > 0:
        gender_data = filtered_df.groupby('Gender')['Student_Count'].sum().reset_index()
        gender_data.columns = ['Gender', 'Count']
        all_genders = pd.DataFrame({'Gender': ['Male', 'Female', 'Others']})
        gender_data = all_genders.merge(gender_data, on='Gender', how='left').fillna(0)
        gender_data = gender_data[gender_data['Count'] > 0]
    else:
        gender_data = pd.DataFrame({
            'Gender': ['Male', 'Female', 'Others'],
            'Count': [53.2, 33.4, 13.4]
        })
    
    fig = px.pie(gender_data, 
                 values='Count', 
                 names='Gender',
                 color='Gender',
                 color_discrete_map={'Male': '#002E79', 'Female': '#9BC1FF', 'Others': '#5288E0'})
    
    fig.update_traces(textposition='inside', textinfo='label+percent', 
                     textfont=dict(size=10, color='white', weight='bold'))
    fig.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        showlegend=False,
        height=140,
        paper_bgcolor='white'
    )
    
    return fig


# Callback for migration reasons
@app.callback(
    Output('migration-reasons', 'figure'),
    [Input('location-filter', 'value'),
     Input('industry-filter-all', 'value'),
     Input('industry-filter1', 'value'),
     Input('industry-filter2', 'value'),
     Input('industry-filter3', 'value'),
     Input('industry-filter4', 'value'),
     Input('study-filter', 'value'),
     Input('study-filter2', 'value'),
     Input('study-filter3', 'value'),
     Input('employment-filter', 'value'),
     Input('employment-filter2', 'value'),
     Input('year-filter', 'value')])
def update_migration_reasons(loc_all, ind_all, ind1, ind2, ind3, ind4, 
                             study1, study2, study3, emp1, emp2, years_filter):
    
    locations = loc_all if loc_all else ['ALL']
    if not locations or 'ALL' in locations:
        locations = ['ALL']
    
    industries_filter = combine_filters([ind_all, ind1, ind2, ind3, ind4])
    if not industries_filter or 'ALL' in ind_all:
        industries_filter = ['ALL']
    
    study_levels = combine_filters([study1, study2, study3])
    if not study_levels or 'ALL' in study1:
        study_levels = ['ALL']
    
    employment_types = combine_filters([emp1, emp2])
    if not employment_types or 'ALL' in emp1:
        employment_types = ['ALL']
    
    filtered_df = filter_data(locations, industries_filter, study_levels, employment_types, years_filter)
    
    if 'Migration_Reason' in filtered_df.columns and 'Gender' in filtered_df.columns and 'Student_Count' in filtered_df.columns:
        migration_data = filtered_df.groupby(['Migration_Reason', 'Gender'])['Student_Count'].sum().reset_index()
        migration_data.columns = ['Migration_Reason', 'Gender', 'Count']
        migration_pivot = migration_data.pivot(index='Migration_Reason', columns='Gender', values='Count').fillna(0)
    else:
        migration_pivot = pd.DataFrame({
            'Male': [35, 30, 25, 20, 15],
            'Female': [40, 35, 30, 25, 20]
        }, index=['Migration Pathway Issues', 'Lack of Job Opportunities', 'Financial Pressures', 
                  'Visa Issues', 'Job Opportunities in Home Country'])
    
    migration_pivot['Total'] = migration_pivot.sum(axis=1)
    total_students = migration_pivot['Total'].sum()
    
    reasons = migration_pivot.index.tolist()
    male_data = migration_pivot['Male'].values if 'Male' in migration_pivot.columns else [35, 30, 25, 20, 15]
    female_data = migration_pivot['Female'].values if 'Female' in migration_pivot.columns else [40, 35, 30, 25, 20]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Male',
        y=reasons,
        x=male_data,
        orientation='h',
        marker=dict(color='#002E79'),
        text=[f'{val/total_students*100:.1f}%' if total_students > 0 else '0%' for val in male_data],
        textposition='inside',
        textfont=dict(size=10, color='white', weight='bold'),
        hovertemplate='%{y}<br>Male: %{x}<br>%{text}<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='Female',
        y=reasons,
        x=female_data,
        orientation='h',
        marker=dict(color='#9BC1FF'),
        text=[f'{val/total_students*100:.1f}%' if total_students > 0 else '0%' for val in female_data],
        textposition='inside',
        textfont=dict(size=10, color='#000', weight='bold'),
        hovertemplate='%{y}<br>Female: %{x}<br>%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title='Number of Students',
        yaxis_title='',
        margin=dict(l=5, r=5, t=5, b=30),
        height=340,
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation='h', 
            yanchor='bottom', 
            y=1.01, 
            xanchor='right', 
            x=1, 
            font=dict(size=10)
        ),
        yaxis=dict(autorange='reversed', tickfont=dict(size=10)),
        xaxis=dict(tickfont=dict(size=9), gridcolor='lightgray', title_font=dict(size=10))
    )
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)
