from pyvis.network import Network
from data import Data
import pandas as pd
import os
import shutil
import tempfile

paths = []

def bigger_size(size):
    """
    """
    return (size * 100) + 5


def smaller_size(size):
    """
    """
    return (size - 5) / 100


def create_network(id, title, size, color, edges, html_dir):
    """
    """ 
    # init   
    net = Network()
    
    # creating the nodes
    net.add_nodes(id, label=id, title = title, size = size, color = color)
    
    # creating the edges
    for e in edges:
        net.add_edge(e[0], e[1], weight=e[2])
    
    # creating the path
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    path = os.path.join(html_dir, 'net.html') 
    paths.append(path)
    
    # writing the final network into path
    net.show_buttons(filter_=['physics'])
    net.show(path)


def create_attributes(data, vector, G_pos_threshold , G_neg_threshold):
    """
    """    
    # taking the relevent columns
    rows = len(data.df.index)
    G_values = data.df[vector]
    string_names =  data.df[data.string_name_header]
    original_names =  data.df[data.id_header]
    
    # create nodes attributes
    id = []
    title = []
    color = []
    size = []
    red = "#ff0000"
    blue = "#0047AB"
    for i in range(rows):
        G_value = G_values[i]
        string_name = string_names[i] 
        
        # check if protein has string name
        if pd.isna(string_name):
            continue

        # color: negative = blue, positive = red
        if G_value < 0 and G_value < G_neg_threshold:
            color.append(str(red))
            
        elif G_value > 0 and G_value > G_pos_threshold:
            color.append(str(blue))
        
        else:
            continue
        
        # id = original name
        id.append(original_names[i])
        # title = string name
        title.append(string_name)
        # size = G_Value
        size.append(bigger_size(abs(G_value)))
    
    # reads scores file
    df = pd.read_excel(data.scores_path, data.tab, header=0)
    
    # create edges attributes 
    edges = []
    for __, row in df.iterrows():
        first = row['first protein']
        second = row['second protein']
        score = row['score']
       
        # if both in nodes id - add the edge
        if (first in id) and (second in id):
            edges.append((first, second, score))
        
    return id, title, size, color , edges


def add_table_script(path):
    """
    """
    table_first_line = "<table id = \"table\" border=\"1\" class=\"dataframe\">"

    table_scripts = "<html lang= \"en\" dir=\"ltr\"><head>"
    table_scripts += "<link rel=\"stylesheet\" type=\"text/css\" href=\"https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css\">"
    table_scripts += "<script src=\"https://code.jquery.com/jquery-3.6.0.min.js\"integrity=\"sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=\"crossorigin=\"anonymous\"></script> "
    table_scripts += "<script type=\"text/javascript\" charset=\"utf8\" src=\"https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js\"></script>"
    table_scripts += "<script type=\"text/javascript\">"
    table_scripts += "  $(document).ready( function () {"
    table_scripts += "    $('#table').DataTable();"
    table_scripts += "} );"
    table_scripts += "</script></head><body>"

    table_last_line = "</body></html>"
    
    # writing
    with open(path) as src, tempfile.NamedTemporaryFile(
                                    'w', dir=os.path.dirname(path), delete=False) as dst:

        # Discard first line
        src.readline()

        # Save the new first lines
        dst.write(table_scripts + '\n')
        dst.write(table_first_line + '\n')

        # Copy the rest of the file
        shutil.copyfileobj(src, dst)
        
        # Save the new last lines
        dst.write(table_last_line + '\n')


    # remove old version
    os.unlink(path)

    # rename new version
    os.rename(dst.name, path)

    return()
  
    
def create_table(ids, sizes, edges, html_dir):
    """
    """
    # size back to original
    sizes = [smaller_size(s) for s in sizes]
    
    # calculating different scores for each node
    degrees = []
    weights = []
    scores = []
    for id, size in zip(ids, sizes):
        #  node degree = number of neighbors
        node_degree = sum(1 for e in edges if (e[0] == id or e[1] == id))
        
        # node weight = average edges weights
        if node_degree != 0:
            node_weight = sum(e[2] for e in edges if (e[0] == id or e[1] == id))
        else:
            node_weight = 0
        
        # final node score 
        
        total_score = node_weight * 0.5 + size * 0.5
        
        degrees.append(node_degree)
        weights.append(node_weight)
        scores.append(total_score)  
         
    # creating the table   
    df = pd.DataFrame(list(zip(ids, sizes, degrees, weights, scores)),
               columns =['ID', 'Size', 'Node degree', 'weighted Node degree', 'Final score' ])
    
    # top 3 proteins
    top = df.nlargest(3, 'Final score')
    
    # creating the path
    path = os.path.join(html_dir, 'table.html') 
    paths.append(path)
    
    # creating the html file
    df.to_html(path)
    add_table_script(path)
    
    return top


def merge_files(html_dir):
    # Python program to
    # demonstrate merging of
    # two files
    final_path = os.path.join(html_dir, 'result.html') 

    # Open file3 in write mode
    with open(final_path, 'w') as outfile:
    
        # Iterate through list
        for names in paths:
    
            # Open each file in read mode
            with open(names) as infile:
    
                # read the data from file1 and
                # file2 and write it in file3
                outfile.write(infile.read())
    
            # Add '\n' to enter data of file2
            # from next line
            outfile.write("\n")
    
    return final_path