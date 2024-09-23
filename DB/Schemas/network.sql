-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS network;

-- Table for storing node-to-node links (protein interactions) in the network schema
CREATE TABLE network.node_node_links (
    node_id_a INT,  -- Internal identifier (equivalent to protein_id)
    node_id_b INT,  -- Internal identifier (equivalent to protein_id)
    taxonomy_id INT,  -- Taxonomy identifier (equivalent to species_id)
    combined_score FLOAT,  -- The combined score of all the evidence scores
    evidence_score JSONB,  -- Evidence score as a JSON list of score types and their scores (e.g., {{4, 0.626}})
    PRIMARY KEY (node_id_a, node_id_b),  -- Composite primary key for unique links between two proteins
    FOREIGN KEY (node_id_a) REFERENCES items.proteins(protein_id),  -- Reference to node A (protein)
    FOREIGN KEY (node_id_b) REFERENCES items.proteins(protein_id),  -- Reference to node B (protein)
    FOREIGN KEY (taxonomy_id) REFERENCES items.species(species_id)  -- Reference to species (taxonomy)
);


-- Create an index for (node_id_a, node_id_b)
CREATE INDEX idx_node_node_links_a_b ON network.node_node_links(node_id_a, node_id_b);

-- Create an index for (node_id_b, node_id_a)
CREATE INDEX idx_node_node_links_b_a ON network.node_node_links(node_id_b, node_id_a);
