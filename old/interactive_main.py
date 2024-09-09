from interactive import *
from data import *
import os
import webbrowser

#----------Main Functions----------#
data_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
data_table_path = os.path.join(data_dir, 'prepared_data_table.xlsx')

def prepare_interactice_network(original_path, data_tab, index_header, id_header, vectors_headers_prefix,
                 G_pos_threshold, G_neg_threshold):
    """
    """    
    resarch_data = Data(original_path, data_tab, index_header, id_header, vectors_headers_prefix)

    html_dir = os.path.join( resarch_data.dir , 'html')

    id, title, size, color, edges = create_attributes(resarch_data, 'Gi1', G_pos_threshold, G_neg_threshold)
        
    create_network(id, title, size, color, edges, html_dir)
    
    print(f"Created network for id:{id}\n"
          f"Titles: {title}\n"
          f"Sizes: {size}\n"
          f"Colors: {color}\n")
    
    top = create_table(id, size, edges, html_dir)
    print(top)
    
    return 'file://' +  merge_files(html_dir)
    

if __name__ == "__main__":
    final_path = prepare_interactice_network(
        data_table_path, "G", "index", "UID", "Gi", 0.04, -0.04)
    
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(final_path)
