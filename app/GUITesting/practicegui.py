import plotly.graph_objects as go

fig = go.Figure()

for step in [1,2,3]:
    fig.add_trace(
        go.Scatter(
            x=[1,2],
            y=[step, 2**step],
            mode="lines",
            line=go.scatter.Line(color="gray"),
            showlegend=False)
    )

#fig.data[0].visible=True

# Create and add slider
steps = []
ctrlmodes=["Scrambled","Tactical/Opportunisitc","Strategic"]
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": ctrlmodes[i] + " work strategy"}],  # layout attribute
        label=ctrlmodes[i]
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Control Mode: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.write_html('test.html', auto_open=True)