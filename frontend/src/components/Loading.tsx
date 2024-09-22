import { FC } from "react";
import ClipLoader from "react-spinners/ClipLoader";
import "../styles/Loading.css";

const LoadingComponent: FC = () => {
  return (
    <div className="loading-wrapper">
      <p>Preparing the results.</p>
      <p>
        Please be patient, this may take a few minutes (depending on the data
        size).
      </p>
      <ClipLoader size={80} color="#217BF4" />
    </div>
  );
};

export default LoadingComponent;
