import os
import webbrowser
import networkx as nx


def configuration_to_nx(config):
    G = nx.MultiDiGraph()
    for relation in config:
        for i, node in enumerate(relation):
            G.add_node(node)
            if (i+1) < len(relation):
                from_node = node
                to_node = relation[i + 1]
                G.add_edge(from_node, to_node)
    return G


def show_network(G, name="out.html", is_notebook=False):
    html = get_html(G)
    o = open(name, "w")  # TODO write tempfile if no name is provided?
    o.write(html)
    o.close()
    if not is_notebook:
        webbrowser.open('file://' + os.path.realpath(name))
    # TODO if we are in a notebook, then there are some extra steps to render the html


def get_html(G):

    nodes = "[" + ",".join(["{id: " + str(n) + ", label: " + str(n) + ", shape: \"dot\", size: 10}" for n in G.nodes]) + "]"

    edges = []
    self_references = {}
    for e in G.edges:
        self_reference = ""
        if e[0] == e[1]:
            if (e[0], e[1]) not in self_references:
                self_references[(e[0], e[1])] = 0
            self_references[(e[0], e[1])] += 1
            self_reference = ", selfReferenceSize: %s" % (15 + self_references[(e[0], e[1])]*5)
        edges.append("{from: %s, to: %s, arrows: \"to\", weight: 1%s}" % (str(e[0]), str(e[1]), self_reference))
    edges = "[" + ",".join(edges) + "]"

    ret = """<html><head>
      <title>Netomaton</title>
      <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.19.1/vis.js"></script>
      <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.19.1/vis.css" rel="stylesheet" type="text/css">
      <style type="text/css">
          #mynetwork {
            width: 100%;
            height: 100%;
            border: 1px solid lightgray;
          }
          #loadingBar {
            position: absolute;
            top: 50%;
            left: 50%;
            -moz-transform: translateX(-50%) translateY(-50%);
            -webkit-transform: translateX(-50%) translateY(-50%);
            transform: translateX(-50%) translateY(-50%);
            -webkit-transition: all 0.5s ease;
            -moz-transition: all 0.5s ease;
            -ms-transition: all 0.5s ease;
            -o-transition: all 0.5s ease;
            transition: all 0.5s ease;
            opacity: 1;
          }
          #wrapper {
            position: relative;
            width: 100%;
            height: 100%;
          }
    
          #text {
            position: absolute;
            top: 8px;
            left: 330px;
            width: 30px;
            height: 50px;
            margin: auto auto auto auto;
            font-size: 16px;
            font-family: sans-serif;
            color: #000000;
          }
    
          div.outerBorder {
            position: relative;
            top: 0px;
            width: 400px;
            height: 44px;
            margin: auto auto auto auto;
          }
    
          #border {
            position: absolute;
            top: 10px;
            left: 10px;
            width: 300px;
            height: 13px;
            margin: auto auto auto auto;
            box-shadow: 0px 0px 4px rgba(0, 0, 0, 0.2);
          }
    
          #bar {
            position: absolute;
            top: 0px;
            left: 0px;
            width: 10px;
            height: 10px;
            margin: auto auto auto auto;
            border: 2px solid rgba(30, 30, 30, 0.05);
            background: rgb(0, 173, 246); /* Old browsers */
            box-shadow: 2px 0px 4px rgba(0, 0, 0, 0.4);
          }
      </style>
    <script type="text/javascript">
    function draw() {
      var nodes = new vis.DataSet(""" + nodes + """);
      var edges = new vis.DataSet(""" + edges + """);
      var container = document.getElementById('mynetwork');
      var data = {
        nodes: nodes,
        edges: edges
      };
      var options = {
          "physics": {
            "forceAtlas2Based": {
              "gravitationalConstant": -50,
              "centralGravity": 0.01,
              "springLength": 100,
              "springConstant": 0.53,
              "avoidOverlap": 0
            },
            "minVelocity": 0.75,
            "solver": "forceAtlas2Based",
            "timestep": 0.22
          }
      };
      var network = new vis.Network(container, data, options);
      
      network.on("stabilizationProgress", function (params) {
        var maxWidth = 296;
        var minWidth = 12;
        var widthFactor = params.iterations / params.total;
        var width = Math.max(minWidth, maxWidth * widthFactor);
    
        document.getElementById("bar").style.width = width + "px";
        document.getElementById("text").innerText =
          Math.round(widthFactor * 100) + "%";
      });
      network.once("stabilizationIterationsDone", function () {
        document.getElementById("text").innerText = "100%";
        document.getElementById("bar").style.width = "296px";
        document.getElementById("loadingBar").style.opacity = 0;
        // really clean the dom element
        setTimeout(function () {
          document.getElementById("loadingBar").style.display = "none";
        }, 500);
      });
    }
    </script>
    </head>
    <body onload="draw()">
    <div id="wrapper">
      <div id="mynetwork"></div>
      <div id="loadingBar">
        <div class="outerBorder">
          <div id="text">0%</div>
          <div id="border">
            <div id="bar"></div>
          </div>
        </div>
      </div>
    </div>
    </body></html>"""
    return ret