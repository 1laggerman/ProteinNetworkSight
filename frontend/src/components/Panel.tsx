import { FC } from "react";
import { IPanelProps } from "../@types/props";
import "../styles/Panel.css";

const Panel: FC<IPanelProps> = ({ node, onClickClose }) => {
  console.log(node);
  return (
    <div className="panel-container">
      <div>
        <button onClick={onClickClose} className = "close-button">X</button>
      </div>
      <div>
        <p className="paragraph-style">
          <span className="panel-container-span">ID:</span>
          {node.id}
        </p>
        <p className="paragraph-style">
          <span className="panel-container-span">Weighted Node Degree:</span>
          {node.linksWeights}
        </p>
        <p className="paragraph-style">
          <span className="panel-container-span">Node Value:</span>
          {node.size}
        </p>
        <p className="paragraph-style">
          <span className="panel-container-span">Final Score:</span>
          {node.size / 2 + node.linksWeights / 2}
        </p>
        <p className="paragraph-style">
          <span className="panel-container-span">Info:</span> {node.info}
        </p>
        <p className="paragraph-style">
          <span className="panel-container-span">Drug:</span>
          {node.drug}
        </p>
        <p className="paragraph-style">
          <span className="panel-container-span">Links:</span>
          {node.links.join(', ')}
        </p>
       
      </div>
    </div>
  );
};

export default Panel;
