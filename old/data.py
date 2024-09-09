from cmath import nan
import pandas as pd
import os
import string_api as api
          
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
        string_suggestions = string_suggestions.replace(c, "")
  
    if len(string_suggestions) == 0:
        return None
   
    string_suggestions = string_suggestions.split(",")   
    return string_suggestions[0]
    

#----------Data class definition----------#


class Data:
     
    def __init__(self, original_path, data_tab, index_header, id_header, vectors_headers_prefix):
        # data path
        self.original_path = original_path
        self.tab =  data_tab
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
                # drop all irrelevant columns
                vectors_cols = [col for col in self.df.columns if col.startswith(self.vectors_headers_prefix)]
                id_cols = [self.index_header, self.id_header]
                self.df =  self.df[id_cols + vectors_cols] 
            
            print(self)
            
            
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
        new_sug_col = self.df.apply(lambda row: api.map_uid(row[self.id_header], row[self.clean_header]), axis=1)
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
        scores = api.network_interactions(genes, score_threshold)
        
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