from cmath import nan
import pandas as pd
import os
import requests 
from time import sleep
from pyvis.network import Network
import pandas as pd
import os
import shutil
import tempfile
import os
import webbrowser

string_api_url = "https://string-db.org/api"
medmolnet_api = ""
output_format = "tsv-no-header"
app_name = "personal_cancer_med_project"     # our app name
human = 9606    

#----------API Connection----------#

def api_request(method, params, wait_time = 1):
    """[summary]
    Args:
        method ([type]): [description]
        params ([type]): [description]
    Returns:
        [type]: [description]
    """
    # Construct URL
    request_url = "/".join([string_api_url, output_format, method])
    # call STRING
    response =  requests.post(request_url, data=params)
    # wait a sec between calls 
    sleep(wait_time)
    
    return response


def map_uid(org_id, clean_id):
    """[summary]
    Args:
        org_id ([type]): [description]
        clean_id ([type]): [description]
        print_result ([type]): [description]
    Returns:
        [type]: [description]
    """    
    clean_id = clean_id.upper()   
    
    # request string
    method = "get_string_ids"
    params = {
        "identifiers" : clean_id, # protein list
        "species" : human, 
        # "limit" : 5, # five (best) identifier per input protein
        "caller_identity" : app_name
    } 
    response = api_request(method, params)
    
    # parse the result
    str_suggestions = [] 
    for line in response.text.strip().split("\n"):
        l = line.split("\t")
        if(len(l) > 4):
            str_suggestions.append(l[4])
    
    if len(str_suggestions)  == 0:
        print("Attention: didn't find string id for:", org_id, ", after cleaning:", clean_id)
    else:
        print("Found: string id for:", org_id, ", after cleaning:", clean_id, "string suggestions:", str_suggestions)
   
    return str_suggestions  


def network_interactions(genes, score_threshold):
    """
    """
    # set parameters
    method = "network"        
    params = {
        "identifiers" : "%0d".join(genes), 
        "species" : human, 
        "caller_identity" : app_name
    }
    response = api_request(method, params)
    
    scores = []
    for line in response.text.strip().split("\n"):
        # takes the proteins names
        l = line.strip().split("\t")
        p1, p2 = l[2], l[3]

        # filter the interaction according to experimental score, prevent doubles
        experimental_score = float(l[10])
        if experimental_score > score_threshold:
            score = (p1, p2, experimental_score)
            if score not in scores:
                scores.append(score)

    return scores



          
#----------Global Functions----------#
def remove_duplicates(from_list):
    """
    """
    return list(dict.fromkeys(from_list))


def remove_None(from_list):
    """
    """
    return [i for i in from_list if (not pd.isna(i))]


def count_None(from_list):
    """
    """
    return sum(x is None for x in from_list)

#----------Specific Functions----------#
delete_after =['-P', '_P', '_CLEAVED','-CLEAVED', '_CLONE','-CLONE', '_ACTIVE', '-ACTIVE'] 
remove = ['_','-', ']', '[', '\'']

def clean_id(id, delete_after = delete_after, remove = remove, complex_sub = "COMPLEX" , delim = "_"):
    """Parse single id to make it readable for automation.
    Args:
        id (string): [description].
        delete_after ([string], optional): [description].
        remove ([string], optional): [description]. 
    Returns:
        new id string.
    """
    # move to uppercases letters
    id = str(id).upper()
    if not id:
        return ""
    
    # special case = complex protein
    if str(complex_sub) in id:
        return complex_rom_num(id, complex_sub, delim)
    
    # delete all chars that appear after the chars in the to_delete array (included)
    new_id = id
    for d in delete_after:
        new_id = new_id.partition(d)[0]

    # remove the chars that in the remove array
    for c in remove:
        new_id = new_id.replace(c, " ")

        
    return new_id


def complex_rom_num(comp, complex_sub, delim):
    """Finds the roman numeral of a complex protein.
    Args:
        comp ([type]): [description]
    Returns:
        [type]: [description]
    """    
    rom_start_idx = comp.find(complex_sub) + len(complex_sub) + len(delim)
    
    rom_end_idx = comp.find(delim, rom_start_idx)

    return complex_sub + " " + comp[rom_start_idx : rom_end_idx]

    
def first_string_suggestion(string_suggestions):
    """[summary]

    Args:
        string_suggestions ([type]): [description]
    """
    for c in ["[", "]", "\'", " "]:
        string_suggestions = str(string_suggestions).replace(c, "")
  
    if len(string_suggestions) == 0:
        return None
   
    string_suggestions = string_suggestions.split(",")   
    return string_suggestions[0]
    

#----------Data class definition----------#


class Data:
     
    def __init__(self, original_path, data_tab, index_header, id_header, vectors_headers_prefix):
        # data path
        self.original_path = original_path
        self.tab = data_tab
        self.dir = os.path.dirname(original_path)
        # for the new path - take the given path until the last '/' and add the new file name
        self.new_path = os.path.join(self.dir, 'prepared_data_table.xlsx') 
        self.scores_path = os.path.join(self.dir, 'network_scores.xlsx') 
        # original headers
        self.index_header = index_header
        self.id_header = id_header
        self.vectors_headers_prefix = vectors_headers_prefix
        # new headers
        self.clean_header =  'Clean ID'
        self.string_name_header =  'String Name'
        self.string_suggestions_header = 'String Suggestions'
        # reads the xlsx file into pandas object
        self.df = None
        self.open_tab()
        
      
    def __str__(self):    
        to_print = 5    
        s = "Data Object:\nNew path: " + str(self.new_path) +".\n"
        s += "Original headers: " + str(self.index_header) +", "+ str(self.id_header) +", "+ str(self.vectors_headers_prefix) +".\n"
        s += "New headers: " + str(self.clean_header) +", "+ str(self.string_name_header)  +", "+ str(self.string_suggestions_header)+".\n"
        s += "Starting content: \n" + self.df.iloc[:to_print, :to_print].to_markdown()
        return s
    
        
    def open_tab(self):
        """Reads the xlsx data table to a pandas data frame.
        Returns:
            [type]: [description]
        """
        if self.df is None: 
            # if new path exist - open the new path
            if os.path.isfile(self.new_path):
                self.df = pd.read_excel(self.new_path, self.tab, header=0)
            else:
                self.df = pd.read_excel(self.original_path, self.tab, header=0)
                for col in self.df.columns:
                    print(str(col), str(col).startswith(self.vectors_headers_prefix), self.vectors_headers_prefix)
                # drop all irrelevant columns

                vectors_cols = [col for col in self.df.columns if str(col).startswith(self.vectors_headers_prefix)]
                id_cols = [self.index_header, self.id_header]

                self.df =  self.df[id_cols + vectors_cols] 
            
            print(self.df)

            # print(self)
            
            
    def replace_tab_content(self):
        """
        Write a pandas dataframe into the new xlsx data table - replacing the previous content.
        """     
        # if the file don't exist - creates a new one.
        writer = pd.ExcelWriter(self.new_path, engine='xlsxwriter')
       
        self.df.to_excel(writer, sheet_name=self.tab, index=False, encoding='utf8')
        
        writer.save()
        print(self)
        
        
    def add_column(self, column, index, header):
        """[summary]
        Args:
            column_data ([type]): [description]
            column_index ([type]): [description]
            column_header ([type]): [description]
        """   
        # checks if needs to replace an existing column or create a new one
        if header in self.df.columns:
            self.df[header] = column
        else:
            self.df.insert(index, header, column)
        
        # writes the changes into the excel file
        self.replace_tab_content()
    
       
    def has_clean_id_col(self):
        """[summary]
        Returns:
            [type]: [description]
        """        
        if self.clean_header not in self.df.columns:
            return False
        return True
    
     
    def add_clean_id_col(self, at_index = 2):
        """Creating the new uid column applying clean_uid on each uid.
        Args:
            data ([type]): [description]
            org_id_header ([type]): [description]
            new_id_header ([type]): [description]
            new_id_index ([type]): [description]
        Returns:
            [type]: [description]
        """
        if self.has_clean_id_col():
            answer = input("Clean ID column already exist. Do you want to create it again? (Y/N)")
            if answer != 'Y':
                return
        
        # create a new column of the clean uid
        new_col = self.df.apply(lambda row: clean_id(row[self.id_header]), axis=1)
        # adds the new column to the data
        self.add_column(new_col, at_index, self.clean_header)
    
    
    
    def has_string_suggestions_col(self):
        """[summary]
        Returns:
            [type]: [description]
        """        
        if self.string_suggestions_header not in self.df.columns:
            return False
        return True
    
    
    def add_string_suggestions_col(self):
        """
        """
        if not self.has_clean_id_col():
            print("Please run add_clean_id_col func first.")   
            return
        
        if self.has_string_suggestions_col():
            answer = input("String suggestions column already exist. Do you want to create it again? (Y/N)")
            if answer != 'Y':
                return
        # create a new column of string suggestions using the string api
        new_sug_col = self.df.apply(lambda row: map_uid(row[self.id_header], row[self.clean_header]), axis=1)
        # adds the new column to the data
        self.add_column(new_sug_col, 3, self.string_suggestions_header)
        
        
    def has_string_name_col(self):
        """[summary]
        Returns:
            [type]: [description]
        """        
        if self.string_name_header not in self.df.columns:
            return False
        return True    
    
    
    def add_string_name_col(self):
        """[summary]

        Args:
            option ([type]): [description]
            print_result ([type]): [description]
            at_index (int, optional): [description]. Defaults to 3.
            at_header (str, optional): [description]. Defaults to 'StringName'.
        """
        if not self.has_string_suggestions_col():
            print("Please run add_string_suggestions_col func first.")   
            return
        
        if self.has_string_name_col():
            answer = input("String suggestions column already exist. Do you want to create it again? (Y/N)")
            if answer != 'Y':
                return
        
        # create a new column of the first string suggestion as string name
        new_name_col = self.df.apply(lambda row: first_string_suggestion(row[self.string_suggestions_header]), axis=1)
        # adds the new column to the data
        self.add_column(new_name_col, 4, self.string_name_header)
        
        # print results
        not_found = count_None(new_name_col)
        print("number of uid that were not found in the string data base:", not_found, "from total:", len(new_name_col))
 
  
    def unique_genes_names(self):
        """[summary]
        Returns:
            [type]: [description]
        """
        return remove_None(remove_duplicates(self.df[self.string_name_header]))
    
    
    def protein_mutations_id(self, string_name):
        """
        """    
        string_names =  self.df[self.string_name_header]
        original_names =  self.df[self.id_header]
    
        mutations = []
        for idx, name in enumerate(string_names):
            if name == string_name:
                mutations.append(original_names[idx])
        print("mutation for: ", str(string_name), "are: ", mutations )
        return mutations
    
    
    def get_network_interactions(self, score_threshold = 0.7):
        """[summary]
        Args:
            proteins_vectors ([type]): [description]
            option ([type]): [description]
            print_result (bool, optional): [description]. Defaults to False.
        Returns:
            [type]: [description]
        """ 
        if not self.has_string_name_col():
            print("Please run add_string_name_col func first.")   
            return
        
        if os.path.isfile(self.scores_path):
            answer = input("network scores file exist. Do you want to rewrite it? (Y/N)")
            if answer != 'Y':
                return  
    
        #create list of the proteins names
        genes = self.unique_genes_names()
        
        # get all pairs interactions scores
        scores = network_interactions(genes, score_threshold)
        
        # convert back to the original id
        original_scores = []
        for s in scores:
            first_mutation = self.protein_mutations_id(s[0])
            secont_mutations = self.protein_mutations_id(s[1])
            for mut1 in first_mutation:
                for mut2 in secont_mutations:
                    original_scores.append((mut1, mut2, s[2]))
                    
                    
        # convert the given scores into a pandas dataframe 
        scores_df = pd.DataFrame(original_scores, columns =['first protein', 'second protein', 'score'])
       
        # if the file don't exist - creates a new one.
        writer = pd.ExcelWriter(self.scores_path, engine='xlsxwriter')
       
        scores_df.to_excel(writer, sheet_name=self.tab, index=False, encoding='utf8')
        
        writer.save()
        print(scores_df)


#----------Main Functions----------#

def prepare_data(original_path, data_tab, index_header, id_header, vectors_headers_prefix,
                 score_threshold):
    """[summary]
    Args:
        data_path ([type], optional): [description]. Defaults to data_table_path.
        data_tab (str, optional): [description]. Defaults to "G".
        index_header (str, optional): [description]. Defaults to "index".
        id_header (str, optional): [description]. Defaults to "UID".
    """    
    resarch_data = Data(original_path, data_tab, index_header, id_header, vectors_headers_prefix)
    
    resarch_data.add_clean_id_col()
    
    resarch_data.add_string_suggestions_col()

    resarch_data.add_string_name_col()
    resarch_data.get_network_interactions(score_threshold)



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

    webbrowser.open(path)
    
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

#----------Main Functions----------#
data_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
data_table_path = os.path.join(data_dir, 'prepared_data_table.xlsx')

def prepare_interactice_network(original_path, data_tab, index_header, id_header, vectors_headers_prefix,
                 G_pos_threshold, G_neg_threshold):
    """
    """    
    resarch_data = Data(original_path, data_tab, index_header, id_header, vectors_headers_prefix)

    html_dir = os.path.join( resarch_data.dir , 'html')

    id, title, size, color, edges = create_attributes(resarch_data, vectors_headers_prefix, G_pos_threshold, G_neg_threshold)
        
    create_network(id, title, size, color, edges, html_dir)
    
    print(f"Created network for id:{id}\n"
          f"Titles: {title}\n"
          f"Sizes: {size}\n"
          f"Colors: {color}\n")
    
    top = create_table(id, size, edges, html_dir)
    print(top)
    
    # final_path = 'file://' +  merge_files(html_dir)
    
    # chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    # webbrowser.get(chrome_path).open(final_path)
    
# if __name__ == "__main__":
#     prepare_data("tests\‏‏‏‏data table.xlsx", "G", "index", "UID", "G", 0.4)
