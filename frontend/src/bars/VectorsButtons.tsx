import { FC } from "react";
import { IVectorsButtonsProp } from "../@types/props";
import "../styles/Button.css";
import "../styles/VectorsButtons.css";


const VectorsButtons: FC<IVectorsButtonsProp> = ({
  vectorsValues,
  setClickedVector,
  clickedVector,
}) => {
  const getClassName = (value:string) => {
    let className = "btn btn--gray btn--small";
    if(clickedVector === value)
      className += " active-btn";
    return className;
  }
  return (
    <div className="scroll-row-buttons">
      {vectorsValues.map((value: string, index: number) => {
        return (
          <button
            key={index}
            className={getClassName(value)}
            type="button"
            onClick={() => {
              setClickedVector(value);
            }}
          >
            {value}
          </button>
        );
      })}
    </div>
  );
};

export default VectorsButtons;
