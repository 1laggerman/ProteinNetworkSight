from data import *

#----------Main Functions----------#
data_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'data')
data_table_path = os.path.join(data_dir, 'data_table.xlsx')

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


if __name__ == "__main__":
    prepare_data(data_table_path, "G", "index", "UID", "Gi", 0.4)