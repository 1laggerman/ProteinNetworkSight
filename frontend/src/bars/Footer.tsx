import { FC } from "react";
import "../styles/Footer.css";

const lastUpdate = "25 February, 2023"

const FooterComponent: FC = () => {
  return (
    <div className="footer-container">

    <div className="name">
      <p className="names">Tohar Tsivtman and Ayelet Gibli</p>
      <p className="names">Nitzan Migdal and Omri Nahor</p>

      <p className="names">Aviv Eldad</p>
      
      
    </div>
    <div className="update"><p className="update">Last database update: {lastUpdate}</p></div>
    <div className="years">
    <p className="year">2022</p>
    <p className="year">2023</p>
  </div>
  </div>
  );
};

export default FooterComponent;
