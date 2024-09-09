import { FC } from "react";
import { IStepsBarProps } from "../@types/props";

import "../styles/StepsBar.css";

const steps = [
  "upload file",
  "SET PARAMETERS AND THRESHOLDS",
  "Adjust protein\\gene names based on STRING",
  "PROTEINS\\GENES FOR WHICH THE NAMES SHOULD BE SET MANUALLY",
  " results",
];

const StepsBar: FC<IStepsBarProps> = ({ step }) => {

  const currentClass = (index: number): string => {
    /*
    Change the className of the step label text based on the step number,
    for styling propose.
    */
    if (index + 1 <= step) return "active";
    return "not";
  };

  return (
    <div className="progressbar">
      <ul>
        {steps.map((title, index) => {
          return (
            <li key={title} className={currentClass(index)}>
              {title}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default StepsBar;
