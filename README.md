# StrategiesAnalysis

StrategiesAnalysis contains two main programs for generating network graphs of work strategies - one in MATLAB and one in Python. The Python program is under ongoing development.

## Getting Started

All of the required Python packages are listed in `requirements.txt`.

To install the required packages:
```
pip install -r requirements.txt
```

Running the MATLAB program will require the Bioinformatics toolbox if it is not already intalled.

## Usage

### Running MATLAB program

The main script file for the MATLAB visualization is `main.m` located in the root folder. Running this script generates three network visualizations:
1. A directional graph of actions and information resources
2. A non-directional graph of actions and physical resources
3. A directional graph of actions under the contraints given by the physical and information resources

### Running Python Program

The Python visualization runs on a web application powered by Dash, and the script that runs this application is `app.py`. Running `app.py` runs `main.py` which builds the actual network visualization. Both files are located in `Python\GUITesting`.

To generate the network visualization, run `app.py`.  If there are any cycles detected in the network you will be asked to choose an edge to remove so the network can be generated without cycles. You will then receive the following output:
```
Dash is running on http://127.0.0.1:8050/
```
Follow this link to the server the application is running on. 

The visualization produced is a directed network of action nodes (equivalent to the 3rd MATLAB visualization). This application is interactive and has the following capabilities:
1. Toggle work allocation on/off
2. Move slider to see work strategies for different control modes
3. Toggle arrangement of nodes between topological sort and agent-clustered
4. View either the full network with action and resource nodes or the network with only action nodes

## Data Files
The MATLAB and Python programs use the same data files to generate the visualizations. The data files with the most up to date format are located in `DataFiles\KatieResearch\FinalReportFiles`.

Creating the network graphs requires data on physical resource constraints, information resource constraints, and a work allocation. This data provided in csv format. Listed below are examples of the contents and format of the 3 required data files.

Physical Resource Constraints:
```
Action_name,Resource_name,use,priority

Example:

MaintenanceWMPrepare_inspection_tools,MaintenanceWMInspection_tool,use,0
MaintenanceWMApply_inspection_tools,MaintenanceWMInspection_tool,use,0
```
Information Resource Constraints:
```
Action_name,Resource_name,get or set,priority

Example:

MaintenanceWMGive_inspection_update,MaintenanceWMInspection_outlook,set,1
MaintenanceWMStore_inspection_tools,MaintenanceWMInspection_result,get,0
```
Currently, the program accepts values of -1, 0, or 1 for priority with the following implications:
* -1: soft interdependency, scrambled control mode
* 0: hard interdependency
* 1: soft interdependency, strategic control mode

Work Allocation:
```
Action_name,Agent

Example:

MaintenanceWMTraverse,
MaintenanceWMPrepareInspectionTools,Astronaut
```

In the work allocation csv, an agent is not required for each action. Actions that do not have a corresponding agent will be unassigned in the visualization. **All other entries in each data file are required.**

In the examples above, `MaintenanceWM` is the work model prefix for each of the nodes listed in the data file. This is used to help distinguish the specific work model in the csv. `WMname` must be updated in `main.py` to match the prefix that will be used in the chosen data file - if no prefix is used, leave `WMname` as an empty string.
## Third Party Libraries
This section describes third party libraries used in the Python implementation of the program.
### Networkx
[Networkx](https://networkx.org/documentation/stable/index.html) is the package used to create and analyze networks from the given data. Here it is most heavily used for adding, removing, and searching for nodes or edges in a network. Among its other capabilities are searching for cycles in a network and generating positions of nodes based on a chosen layout.

### Plotly
The graphing library from [Plotly](https://plotly.com/python/) is used to create interactive visualizations of the networks. Currently only the `plotly.graph_objects` module is being used, where a "graph object" is a visualized network. This module allows for the creation and manipulation of our network visualizations. In the web application, the appearance and interaction with the graph and legend can be manipulated with this module. Other items on the page, including the slider bar and radio buttons, are components of the Dash web application discussed below.

### Dash
[Dash](https://dash.plotly.com/) is Plotly's framework for building data visualization applications and is written on top of Flask. Visualizing the networks in a web application allows for more flexibility and interaction with the user. Each interactive item on the page is a "dash core component" and from the `dash_core_components` module. There is also a `dash_html_components` module that allows you to control the arrangement of core components on the page.

**add more about callbacks

## Other Files/Modules
This section describes the files that make up the Python program.
### main
This is the core script of the program that generates the networks from the given data. Because `app.py` is what runs the server for the web application, `main.py` returns the Plotly graph objects that were generated for `app.py` to include on the page.

### app
This is the script that should be run in order to view the application. This will get the plotly graph objects from `main.py` and arrange the graph and various controls on the webpage.
### networkbuild
The networkbuild module contains functions corresponding to the creation of networks from the raw data, relying heavily on the Networkx package.

### networkvis
The networkvis module contains functions corresponding to the visualization of the network and creation of Plotly graph objects.

### sorting, trees, utility
These modules contain various functions that aid in sorting and grouping nodes during network creation and visualization.

## Future Work
Currently, the networks that these programs generate are manually inspected to identify key interdependencies between human and robotic teammates in the work environment. This is done by looking for certain patterns in the work environment that can indicate a specific opportunistic interdependency. For example, when two different agents are completing related work simultaneously, this presents an opportunity for one agent to update the other on their progress.

We believe that this inspection might be automated by modifying the program to search for these patterns in the network, generating suggestions for opportunistic interdependencies that might be present in the work environment.

## Authors

Dr. Martijn IJtsma  ijtsma.1@osu.edu

Katie Albert    albert.224@osu.edu

James Bartman   jbartman47@berkeley.edu