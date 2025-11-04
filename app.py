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
            /* Custom checkbox styling */
            .custom-checkbox input[type="checkbox"] {
                width: 14px;
                height: 14px;
                margin-right: 4px;
                accent-color: #1e3a5f;
                cursor: pointer;
            }
            
            .custom-checkbox label {
                cursor: pointer;
                transition: color 0.2s ease;
                font-weight: 500;
                color: #495057;
            }
            
            .custom-checkbox label:hover {
                color: #1e3a5f;
            }
            
            /* Checked state styling */
            .custom-checkbox input[type="checkbox"]:checked + label {
                color: #1e3a5f;
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
                background: linear-gradient(to bottom, #f8f9fa, #e9ecef);
                border-right: 1px solid #dee2e6;
                box-shadow: 2px 0 5px rgba(0,0,0,0.05);
            }
            
            /* Checkbox container styling */
            .filter-group {
                background-color: white;
                padding: 8px;
                border-radius: 4px;
                margin-bottom: 10px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            }
            
            /* Hover effect for filter groups */
            .filter-group:hover {
                box-shadow: 0 2px 5px rgba(0,0,0,0.12);
            }
            
            /* Box headers centered */
            .box-header {
                text-align: center !important;
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
df = pd.read_csv('/mnt/project/international_students_data.csv')

# Extract unique values for filters
states = df['State'].unique() if 'State' in df.columns else ['NSW', 'VIC', 'QLD', 'WA', 'SA', 'TAS', 'ACT', 'NT']
industries = df['Industry'].unique() if 'Industry' in df.columns else ['Health', 'STEM', 'Social Sc.', 'Design', 'Business', 'Education', 'Prof. Serv', 'Services']
years = sorted(df['Year'].unique()) if 'Year' in df.columns else [2022, 2023, 2024]

# Dashboard layout
app.layout = html.Div([
    # Header - Changed to navy blue
    html.Div([
        html.H1('INTERNATIONAL STUDENT EMPLOYABILITY DASHBOARD - AUSTRALIA',
                style={'textAlign': 'center', 'color': 'white', 'margin': '0', 'padding': '15px',
                       'backgroundColor': '#1e3a5f', 'fontSize': '24px', 'fontWeight': '600'})
    ]),
    
    # Visa Funnel Section
    html.Div([
        html.H2('OVERALL VISA FUNNEL - BREAKDOWN',
                style={'textAlign': 'center', 'backgroundColor': '#5a9bd5', 'color': 'white',
                       'margin': '0', 'padding': '10px', 'fontSize': '16px', 'fontWeight': '500'})
    ]),
    
    # KPI Cards Row - All 5 cards in one line
    html.Div([
        html.Div([
            html.Div('STUDENT VISA APPLICATIONS', style={'fontSize': '10px', 'marginBottom': '3px', 'color': '#6c757d'}),
            html.Div(id='kpi-visa-apps', style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1e3a5f'})
        ], className='border rounded shadow-sm', style={'width': '18%', 'display': 'inline-block', 'textAlign': 'center', 
                  'padding': '10px', 'margin': '5px', 'backgroundColor': 'white'}),
        
        html.Div([
            html.Div('POST-STUDY WORK', style={'fontSize': '10px', 'marginBottom': '3px', 'color': '#6c757d'}),
            html.Div(id='kpi-post-study', style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1e3a5f'})
        ], className='border rounded shadow-sm', style={'width': '18%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '10px', 'margin': '5px', 'backgroundColor': 'white'}),
        
        html.Div([
            html.Div('JOB PLACEMENT', style={'fontSize': '10px', 'marginBottom': '3px', 'color': '#6c757d'}),
            html.Div(id='kpi-job-placement', style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1e3a5f'})
        ], className='border rounded shadow-sm', style={'width': '18%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '10px', 'margin': '5px', 'backgroundColor': 'white'}),
        
        html.Div([
            html.Div('SKILLED VISA APPLICATIONS', style={'fontSize': '10px', 'marginBottom': '3px', 'color': '#6c757d'}),
            html.Div(id='kpi-skilled-visa', style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1e3a5f'})
        ], className='border rounded shadow-sm', style={'width': '18%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '10px', 'margin': '5px', 'backgroundColor': 'white'}),
        
        html.Div([
            html.Div('PR GRANT', style={'fontSize': '10px', 'marginBottom': '3px', 'color': '#6c757d'}),
            html.Div(id='kpi-pr-grant', style={'fontSize': '28px', 'fontWeight': 'bold', 'color': '#1e3a5f'})
        ], className='border rounded shadow-sm', style={'width': '18%', 'display': 'inline-block', 'textAlign': 'center',
                  'padding': '10px', 'margin': '5px', 'backgroundColor': 'white'}),
    ], style={'textAlign': 'center', 'marginBottom': '10px'}),
    
    # Main Content Row
    html.Div([
        # Left Sidebar - Filters
        html.Div([
            # Location Filter
            html.Div([
                html.H4('LOCATION', className='filter-header'),
                html.Div([
                    html.Div([
                        dcc.Checklist(
                            id='location-filter',
                            options=[{'label': 'ALL', 'value': 'ALL'}],
                            value=['ALL'],
                            labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                            className='custom-checkbox',
                            style={'marginBottom': '2px'}
                        ),
                        dcc.Checklist(
                            id='location-states',
                            options=[{'label': state, 'value': state} for state in ['TAS', 'VIC', 'NSW']],
                            value=[],
                            labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                            className='custom-checkbox',
                            style={'marginBottom': '2px'}
                        ),
                    ]),
                    html.Div([
                        dcc.Checklist(
                            id='location-states2',
                            options=[{'label': state, 'value': state} for state in ['SA', 'WA', 'QLD']],
                            value=[],
                            labelStyle={'display': 'inline-block', 'marginRight': '8px', 'fontSize': '10px'},
                            className='custom-checkbox'
                        ),
                    ]),
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
                  'padding': '12px', 'height': '600px', 'overflowY': 'auto', 'marginRight': '1%'}),
        
        # Middle Section - Maps and Charts with improved alignment
        html.Div([
            # Regional Split
            html.Div([
                html.H3('REGIONAL SPLIT - NO. OF INTL. STUDENTS',
                       className='box-header',
                       style={'backgroundColor': '#2d5b8b', 'color': 'white', 'padding': '8px',
                              'margin': '0', 'fontSize': '12px', 'textAlign': 'center'}),
                html.Div([
                    dcc.Graph(id='australia-map', style={'height': '520px'}, config={'displayModeBar': False})
                ], style={'backgroundColor': 'white', 'border': '1px solid #dee2e6', 'padding': '10px', 'height': '540px'})
            ], className='shadow-sm rounded', style={'width': '49%', 'display': 'inline-block', 
                     'verticalAlign': 'top', 'marginRight': '2%', 'backgroundColor': 'white', 'height': '580px'}),
            
            # Job Achievement
            html.Div([
                html.H3('JOB ACHIEVED - NATIONALITY SPLIT (TOP 10)',
                       className='box-header',
                       style={'backgroundColor': '#2d5b8b', 'color': 'white', 'padding': '8px',
                              'margin': '0', 'fontSize': '12px', 'textAlign': 'center'}),
                html.Div([
                    dcc.Graph(id='nationality-chart', style={'height': '520px'}, config={'displayModeBar': False})
                ], style={'backgroundColor': 'white', 'border': '1px solid #dee2e6', 'padding': '10px', 'height': '540px'})
            ], className='shadow-sm rounded', style={'width': '49%', 'display': 'inline-block', 
                     'verticalAlign': 'top', 'backgroundColor': 'white', 'height': '580px'}),
            
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        
        # Right Section - Salary and Demographics with better spacing
        html.Div([
            # Salary Cards - Both cards same color now
            html.Div([
                html.Div([
                    html.Div('Median Salary', style={'fontSize': '10px', 'color': 'white', 'marginBottom': '3px'}),
                    html.Div(id='median-salary', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'width': '100%', 'backgroundColor': '#4a90e2',
                         'padding': '8px', 'textAlign': 'center', 'marginBottom': '5px', 'borderRadius': '4px'}),
                
                html.Div([
                    html.Div('Mean Salary', style={'fontSize': '10px', 'color': 'white', 'marginBottom': '3px'}),
                    html.Div(id='mean-salary', style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'white'})
                ], style={'width': '100%', 'backgroundColor': '#4a90e2',
                         'padding': '8px', 'textAlign': 'center', 'borderRadius': '4px'}),
            ], className='shadow-sm rounded', style={'marginBottom': '10px', 'backgroundColor': 'white', 'padding': '8px'}),
            
            # Employment Rate and Gender Ratio
            html.Div([
                html.Div([
                    html.H3('EMPLOYMENT RATE', className='box-header', 
                           style={'backgroundColor': '#2d5b8b', 'color': 'white',
                           'padding': '6px', 'margin': '0', 'fontSize': '10px', 'textAlign': 'center'}),
                    html.Div([
                        dcc.Graph(id='employment-rate', style={'height': '160px'}, config={'displayModeBar': False})
                    ], style={'backgroundColor': 'white', 'border': '1px solid #dee2e6', 'padding': '5px'})
                ], className='shadow-sm rounded', style={'width': '48%', 'display': 'inline-block', 
                         'verticalAlign': 'top', 'backgroundColor': 'white'}),
                
                html.Div([
                    html.H3('GENDER RATIO', className='box-header',
                           style={'backgroundColor': '#2d5b8b', 'color': 'white',
                           'padding': '6px', 'margin': '0', 'fontSize': '10px', 'textAlign': 'center'}),
                    html.Div([
                        dcc.Graph(id='gender-ratio', style={'height': '160px'}, config={'displayModeBar': False})
                    ], style={'backgroundColor': 'white', 'border': '1px solid #dee2e6', 'padding': '5px'})
                ], className='shadow-sm rounded', style={'width': '48%', 'display': 'inline-block', 
                         'verticalAlign': 'top', 'marginLeft': '2%', 'backgroundColor': 'white'}),
            ], style={'marginBottom': '10px'}),
            
            # Migration Reasons - Larger to fill space
            html.Div([
                html.H3('GRADUATES LEAVING AUSTRALIA%',
                       className='box-header',
                       style={'backgroundColor': '#2d5b8b', 'color': 'white', 'padding': '6px',
                              'margin': '0', 'fontSize': '10px', 'textAlign': 'center'}),
                html.Div([
                    dcc.Graph(id='migration-reasons', style={'height': '280px'}, config={'displayModeBar': False})
                ], style={'backgroundColor': 'white', 'border': '1px solid #dee2e6', 'padding': '10px'})
            ], className='shadow-sm rounded', style={'backgroundColor': 'white'}),
            
        ], style={'width': '29%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': '1%'}),
    ], style={'marginTop': '10px'}),
    
], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#ffffff', 'margin': '0', 'padding': '0', 'height': '100vh', 'overflowY': 'auto'})


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
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_kpis(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
                study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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


# Callback for Australia map - Changed to yellow-red heat map
@app.callback(
    Output('australia-map', 'figure'),
    [Input('location-filter', 'value'),
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_map(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
               study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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
                         color_continuous_scale=['#ffffe0', '#ffcc00', '#ff9900', '#ff6600', '#ff0000'],  # Yellow to Red gradient
                         size_max=50)
    
    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        landcolor='#f0f8ff',
        coastlinecolor='#4a90e2',
        projection_type="mercator",
        lonaxis_range=[110, 160],
        lataxis_range=[-45, -10],
        bgcolor='white'
    )
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='white',
        coloraxis_showscale=False,
        height=500
    )
    
    return fig


# Callback for nationality chart - Changed to navy blue shades for contrast
@app.callback(
    Output('nationality-chart', 'figure'),
    [Input('location-filter', 'value'),
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_nationality(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
                       study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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
                 color_continuous_scale=['#e6f2ff', '#9bc3ff', '#5a9bd5', '#2d5b8b', '#1e3a5f'],  # Navy blue gradient with high contrast
                 text='Job_Achieved_Pct')
    
    fig.update_traces(texttemplate='%{text:.0f}', textposition='inside', textfont=dict(size=10, color='white', weight='bold'))
    fig.update_layout(
        xaxis_title='% of Job Achieved',
        yaxis_title='',
        showlegend=False,
        margin=dict(l=10, r=10, t=10, b=25),
        height=500,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(gridcolor='lightgray', title_font=dict(size=10), range=[0, 100]),
        yaxis=dict(tickfont=dict(size=10)),
        coloraxis_showscale=False
    )
    
    return fig


# Callback for salary metrics
@app.callback(
    [Output('median-salary', 'children'),
     Output('mean-salary', 'children')],
    [Input('location-filter', 'value'),
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_salary(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
                  study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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


# Callback for employment rate - Navy blue color scheme
@app.callback(
    Output('employment-rate', 'figure'),
    [Input('location-filter', 'value'),
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_employment_rate(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
                           study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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
        emp_rate = 79
    
    donut_data = pd.DataFrame({
        'Category': ['Employed', 'Unemployed'],
        'Value': [emp_rate, 100 - emp_rate]
    })
    
    fig = px.pie(donut_data, 
                 values='Value', 
                 names='Category',
                 hole=0.7,
                 color='Category',
                 color_discrete_map={'Employed': '#1e3a5f', 'Unemployed': '#e0e0e0'})
    
    fig.update_traces(textinfo='none', showlegend=False)
    
    fig.add_annotation(
        text=f'{emp_rate:.0f}%',
        x=0.5, y=0.5,
        font=dict(size=32, color='#1e3a5f', weight='bold'),
        showarrow=False,
        xref='paper',
        yref='paper'
    )
    
    fig.update_layout(
        margin=dict(l=10, r=10, t=5, b=5),
        height=160
    )
    
    return fig


# Callback for gender ratio - Navy blue shades for high contrast
@app.callback(
    Output('gender-ratio', 'figure'),
    [Input('location-filter', 'value'),
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_gender_ratio(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
                        study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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
            'Count': [62.5, 25, 12.5]
        })
    
    fig = px.pie(gender_data, 
                 values='Count', 
                 names='Gender',
                 color='Gender',
                 color_discrete_map={'Male': '#1e3a5f', 'Female': '#5a9bd5', 'Others': '#b8d4f1'})
    
    fig.update_traces(textposition='inside', textinfo='label+percent', textfont=dict(size=10, color='white', weight='bold'))
    fig.update_layout(
        margin=dict(l=10, r=10, t=5, b=5),
        showlegend=False,
        height=160
    )
    
    return fig


# Callback for migration reasons - Shows percentages and navy blue colors
@app.callback(
    Output('migration-reasons', 'figure'),
    [Input('location-filter', 'value'),
     Input('location-states', 'value'),
     Input('location-states2', 'value'),
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
def update_migration_reasons(loc_all, loc_states, loc_states2, ind_all, ind1, ind2, ind3, ind4, 
                             study1, study2, study3, emp1, emp2, years_filter):
    
    locations = combine_filters([loc_all, loc_states, loc_states2])
    if not locations or 'ALL' in loc_all:
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
    
    # Calculate totals for percentage calculation
    migration_pivot['Total'] = migration_pivot.sum(axis=1)
    total_students = migration_pivot['Total'].sum()
    
    reasons = migration_pivot.index.tolist()
    male_data = migration_pivot['Male'].values if 'Male' in migration_pivot.columns else [35, 30, 25, 20, 15]
    female_data = migration_pivot['Female'].values if 'Female' in migration_pivot.columns else [40, 35, 30, 25, 20]
    
    # Create figure using graph_objects for better control
    fig = go.Figure()
    
    # Add male data
    fig.add_trace(go.Bar(
        name='Male',
        y=reasons,
        x=male_data,
        orientation='h',
        marker=dict(color='#1e3a5f'),
        text=[f'{val/total_students*100:.1f}%' if total_students > 0 else '0%' for val in male_data],
        textposition='inside',
        textfont=dict(size=9, color='white'),
        hovertemplate='%{y}<br>Male: %{x}<br>%{text}<extra></extra>'
    ))
    
    # Add female data
    fig.add_trace(go.Bar(
        name='Female',
        y=reasons,
        x=female_data,
        orientation='h',
        marker=dict(color='#5a9bd5'),
        text=[f'{val/total_students*100:.1f}%' if total_students > 0 else '0%' for val in female_data],
        textposition='inside',
        textfont=dict(size=9, color='white'),
        hovertemplate='%{y}<br>Female: %{x}<br>%{text}<extra></extra>'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title='Number of Students',
        yaxis_title='',
        margin=dict(l=10, r=10, t=5, b=20),
        height=280,
        plot_bgcolor='white',
        legend=dict(
            orientation='h', 
            yanchor='bottom', 
            y=1.02, 
            xanchor='right', 
            x=1, 
            font=dict(size=10)
        ),
        yaxis=dict(autorange='reversed', tickfont=dict(size=9)),
        xaxis=dict(tickfont=dict(size=9), gridcolor='lightgray')
    )
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)
