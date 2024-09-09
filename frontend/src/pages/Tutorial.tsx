import { FC } from "react";
import "../styles/Tutorial.css";
import example_rows from "../assets/tutorial images/example_rows.png";
import set_params from "../assets/tutorial images/set_params.png";
import browser from "../assets/tutorial images/browser.png";
import graph from "../assets/tutorial images/graph.png";
import others from "../assets/tutorial images/others.png";
import protein_names from "../assets/tutorial images/protein_names.png";
import table from "../assets/tutorial images/table.png";
import manual_thresholds from "../assets/tutorial images/manual_thresholds.png";
import graph_layout from "../assets/tutorial images/graph_layout.png";
import right_click_menu from "../assets/tutorial images/right_click_menu.png";
import { openLink } from "../common/GeneralCommon";
import { downloadExampleFile } from "../common/ExampleFileAction";

const Tutorial: FC = () => {
  const stringdbLink = "https://string-db.org/";
  const drugsDatabaseLink = "https://www.anticancerfund.org/en/cancerdrugs-db";
  return (
    <div className="page-container">
      <div className="tutorial-container">
        <h1 className="t-h1">ProteinNetworkSight Tutorial</h1>
        <p className="t-p note">
          Note: In addition to the documentation a video tutorial will be
          uploaded soon.
        </p>
        {/* Summary DIV */}
        <div>
          <h2 className="t-h2">Summary</h2>
          <p className="t-p">Our tool works with two existing databases:</p>
          <ol type="a">
            <li className="t-li">
              <button
                className="btn--here"
                onClick={() => {
                  openLink(stringdbLink);
                }}
              >
                String-db
              </button>
              , an online tool and a database of known and predicted
              protein-protein interactions
            </li>
            <li className="t-li">
              <button
                className="btn--here"
                onClick={() => {
                  openLink(drugsDatabaseLink);
                }}
              >
                Cancer Drugs Database
              </button>
              , a database that provides a listing of licensed cancer drugs
            </li>
          </ol>
          <p className="t-p">
            ProteinNetworkSight is an open source tool for calculating patient-specific
            protein networks based on integrating the input from the user with
            the information retrieved from String-db.
          </p>
        </div>
        {/* Starting Point DIV */}
        <div>
          <h2 className="t-h2">Starting Point </h2>
          <p className="t-p">
            For the user to begin, they must upload an Excel / CSV / TSV file on a single sheet (or a TXT that represents an Excel file),
            where each row represents a protein or gene and each column represents a feature. 
            It is recommended that the file contains up to 2000 rows.
            such that each row represents a protein/gene and the columns
            are features to be analysed. The file should contain a column of
            protein/gene names as well as additional column(s) of numeric
            values. Numeric values can represent gene/protein scores (as
            obtained from for example principal component analysis (PCA) or
            information-theoretic) or simple fold changes. The first line is the
            header, specifying column names. Note that the names of the numeric
            columns should start with the same prefix.
          </p>
          <p className="t-p">
            <button className="btn--here" onClick={downloadExampleFile}>
              Here
            </button>
            &nbsp;you can find an example file (fetched from Vasudevan et al.,
            npj Precision Oncology, 2021, Supplementary Data 1). For example,
            here are 10 rows of the example file, where the gene column is named
            “UID” the header of the numerical columns start with “G”, followed
            by some index.
          </p>
          <img className="" src={example_rows} alt="example_rows" />
        </div>
        {/* Setting parameters and thresholds DIV */}
        <div>
          <h2 className="t-h2">Setting parameters and thresholds </h2>
          <p className="t-p">In this step the user should specify:</p>
          <ol type="a">
            <li className="t-li">
              The header name of the gene protein / gene column (in the example
              file it is “UID”)
            </li>
            <li className="t-li">
              The prefix shared by the names of the numerical columns (in the
              example file it is “G”, Gi - is a weight of each protein in a
              pattern (vector) G1, G2, G3 etc.)
            </li>
            <li className="t-li">
              Thresholds for defining the lower limit for String interaction
              score, representing a probability of interaction between each pair
              of examined proteins. The thresholds are defined according to
              STRING-db
            </li>
            <li className="t-li">
              Positive and negative thresholds for excluding values within this
              range of protein scores (for example what is the the minimum score
              to be included in the network analysis)
            </li>
            <li className="t-li">
              Organism of interest (in the example file, it is “Homo sapiens”)
            </li>
          </ol>
          <img className="t-img" src={set_params} alt="set_params" />
        </div>
        {/* Adjusting protein/gene names DIV */}
        <div>
          <h2 className="t-h2">Manual thresholds adjustments </h2>
          <p className="t-p">
          <li className="t-li">
              You can also choose to adjust the thresholds of every G column in the graph
              individually.
          </li>
          </p>
          <img className="t-img" src={manual_thresholds} alt="manual_thresholds"/>
        </div>
        <div>
          <h2 className="t-h2">Adjusting protein/gene names </h2>
          <p className="t-p">
            Our tool connects to&nbsp;
            <button
              className="btn--here"
              onClick={() => {
                openLink(stringdbLink);
              }}
            >
              String-db
            </button>
            &nbsp;in order to create and visualise protein networks. Thus,
            protein/gene names specified in the input file should match the
            names used by String-db. Genes often have multiple names, so it is
            possible that the user used a gene whose name was different in the
            input file and in String-db. The next two steps highlight such cases
            and allow the users to choose different names.
          </p>
          <img className="t-img" src={protein_names} alt="protein_names"/>
          <img className="t-img" src={others} alt="others"/>
        </div>
        {/* Results page DIV */}
        <div>
          <h2 className="t-h2">Results page</h2>
          <p className="t-p">
            The obtained network includes the input score values represented by
            nodes (node radius corresponds to the input protein score value).
            The edges are adapted from STRING-db. Edge width represents the
            probability of a protein-protein interaction. The information can be
            downloaded as either a table or a network. The network can be either
            visualized online or downloaded as a SVG file (editable). Online
            presentation is interactive: the networks can be changed, zoomed-in,
            zoomed-out or rotated.
          </p>
          <h3 className="t-h3">Graph representation</h3>
          <p className="t-p">
            The graph presents a network such that each node represents a
            protein. Node size is proportional to the input value and node color
            represents the sign of the value (red for positive values, blue for
            negative values). Edges between each pair of proteins present
            protein-protein interactions (width of each edge corresponds to a
            probability of a functional protein-protein connection).
          </p>
          <img className="t-img" src={graph} alt="graph"/>
          <p className="t-p">
            The Right click menu in the graph is used to change the layout of the graph.<br/>
            The user can also download the graph as a SVG/PNG/JSON file.<br/>
            You can download the json file for further analysis of this current graph in Cytoscape.<br/>
          </p>
          <img className="t-img" src={right_click_menu} alt="right_click_menu"/>
          <p className="t-p">
            In the right click menu you can order your graphs in the following orders.<br/>
            To save the current layout of the graph you can move any of the nodes and it will be saved until you move another node.<br/>
            if you want to change the layout back to the original layout you can click on the preset layout button.<br/>
          </p>
          <img className="t-img" src={graph_layout} alt="graph_layout"/>
          <p className="t-p">
            In this figure we see several interactions. For example, we can see
            that TIGAR has a positive (blue color) large value and it interacts
            with LKB1 (positive, smaller value) and with GAPDH which has a
            negative value (red color). Furthermore, we can deduce that ACC1
            interacts with both BCL2 and FASN, with BCL2 showing a higher
            probability of interaction (based on the thicker edge connecting the
            two proteins).
          </p>
          <h3 className="t-h3">Table representation</h3>
          <p className="t-p">
            The table representation contain the following columns:
          </p>
          <ul>
            <li className="t-li">
              Original name (the input name for each protein)
            </li>
            <li className="t-li">
              String name (the modified name according to String-db).
            </li>
            <li className="t-li">
              Node value - an input score (as was calculated by using, for
              example, PCA or surprisal analysis)
            </li>
            <li className="t-li">
              Node degree - a number of protein partners each examined protein
              has
            </li>
            <li className="t-li">
              Weighted node degree -Sum of weighted links as provided by STRING's DB and defined as the probability for functional connetion

            </li>
            <li className="t-li">
              Final score -  the average between the node's size (i.e., absolute value of protein’s score) and weighted node degree.

            </li>
            <li className="t-li">
              Drug - a known anticancer drug as obtained from the&nbsp;
              <button
                className="btn--here"
                onClick={() => {
                  openLink(drugsDatabaseLink);
                }}
              >
                Cancer Drugs Database
              </button>
            </li>
          </ul>
          <img className="t-img" src={table} alt="table"/>
        </div>
        {/* Browser compatibility DIV */}
        <div>
          <h2 className="t-h2">Browser compatibility</h2>
          <p className="t-p">
            A summary of the website's browser compatibility, specifying the
            checked version per OS and browser:
          </p>
          <img className="t-img" src={browser}  alt="browser"/>
        </div>
      </div>
    </div>
  );
};

export default Tutorial;
