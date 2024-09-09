import React from 'react';
import { useForm } from "react-hook-form";
// import {useState} from 'react'
import "../styles/FileDetails.css";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: (thresholds: Array<Array<number>>) => void;
  length: number;
  headers: Array<String>;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, onConfirm, length , headers}) => {
  const default_value = 0.1;
  const initialState = Array.from({ length: length }, () => [default_value, -default_value]);
  const [thresholds, setThresholds] = React.useState<Array<Array<number>>>(initialState);
    const modalStyle: React.CSSProperties = {
      display: isOpen ? 'block' : 'none',
      position: 'fixed',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      backgroundColor: '#fff', // Set a solid background color
      height: '80%',
      width: '40%',
      padding: '20px', // Increase padding for a larger modal
      borderRadius: '8px', // Add rounded corners if desired
      boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)', // Add a subtle shadow
      zIndex: 1000,
    };

    const formStyle: React.CSSProperties = {
        display: 'flex',
        flexWrap: 'nowrap',
        flexDirection: 'column',
        height: '90%',
        width: '100%',
        paddingLeft: '5px',
        paddingRight: '5px',
        overflowY: 'scroll',
    };

    const buttonStyle: React.CSSProperties = {
      paddingTop: '3%',
      paddingBottom: '3%',
      paddingRight: '7%',
      paddingLeft: '7%',
      marginRight: '7%',
      marginLeft: '3%',
      marginTop: '10px',
      fontSize: '20px',
    };

    const fieldStyle: React.CSSProperties = {
      width: '100%',
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      textAlign: 'left',
      padding: 'auto',
      marginRight: '5px',
    };
  
    const handleInputChange = (rowIndex: number, colIndex: number, value: String) => {
      thresholds[rowIndex][colIndex] = Number(value);
    };
  
    const renderInputFields = () => {

      return thresholds.map((row, rowIndex) => (
        <div key={rowIndex} style={{display: 'flex', flexDirection: 'column', minHeight: '120px', width: '100%', marginTop: '10px', textAlign: 'center', justifyContent: 'center'}}>

          <label style={{backgroundColor: 'lightblue', padding: '5px', marginTop: '5px', marginBottom: '5px'}}>Thresholds for {headers[rowIndex]}</label>

          <div style={{display: 'flex', flexDirection: 'row', width: '100%'}}>
            <div style={fieldStyle}>
            <label htmlFor={"positiveThreshold".concat(String(headers[rowIndex]))}>Positive Threshold:</label>
              <input
                id={"positiveThreshold".concat(String(headers[rowIndex]))}
                type="number"
                step="0.0001"
                className="text-input"
                min={0}
                max={1}
                defaultValue={default_value}
                onChange={(e) => handleInputChange(rowIndex, 0, e.target.value)}

              />
            </div>

            <div style={fieldStyle}>
              <label htmlFor={"negativeThreshold".concat(String(headers[rowIndex]))}>Negative Threshold:</label>
              <input
                id={"negativeThreshold".concat(String(headers[rowIndex]))}
                type="number"
                step="0.0001"
                className="text-input"
                min={-1}
                max={0}
                defaultValue={-default_value}
                key={0}
                onChange={(e) => handleInputChange(rowIndex, 1, e.target.value)}
              />
            </div>
          </div>
        </div>
      ));
    };
  
    return (
      <div style={modalStyle}>
        <div style={{height: '100%', width: '100%'}}>

            {/* x button on the edge of the modal on next comment */}
            {/* <span className="close" onClick={onClose}>&times;</span>  */}

            <div style={formStyle}>
              {renderInputFields()}
            </div>

          {/* Buttons at the bottom */}
            <div style={{ marginTop: '20px', display: 'flex', flexDirection: 'row', justifyContent: 'center', alignItems: 'center'}}>
                <button style={{...buttonStyle, backgroundColor: '#fff'}} onClick={onClose}>CANCEL</button>
                <button style={{...buttonStyle, backgroundColor: 'lightblue'}} onClick={() => onConfirm(thresholds)}>CONFIRM</button>
            </div>
        </div>
      </div>
    );
  };

export default Modal;