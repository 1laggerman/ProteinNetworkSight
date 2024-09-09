import { FC } from "react";
import { IPanelProps } from "../@types/props";
import "../styles/Panel.css";

const Panel: FC<IPanelProps> = ({ node, onClickClose }) => {
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
