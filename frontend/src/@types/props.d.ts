import { Font } from "three/examples/jsm/loaders/FontLoader";
import { IOthers } from "./forms";
import { threshMap } from "./global";
/*
  This file define all the props interface - the argument for components.
*/

export interface IErrorInputTextProps {
  orgName: string;
}

export interface IStepProps {
  step: number;
  goNextStep: () => void;
}

export interface IPanelProps {
  node: true | ICustomNode;
  onClickClose: () => void;
}

export interface IGraphProps {
  graphData: ICustomGraphData;
  clickedVector: string;
  thresholds: threshMap;
  // font: Font;
}

export interface IStepsBarProps {
  step: number;
}

export interface IButtonsProps extends IStepProps {
  formId: string;
  goBackStep: () => void;
}

export interface IVectorsButtonsProp {
  vectorsValues: string[];
  setClickedVector: React.Dispatch<React.SetStateAction<string>>;
  clickedVector: string;
}

export interface IGraphBarProps {
  openTable: boolean;
  setOpenTable: React.Dispatch<React.SetStateAction<boolean>>;
  nodesNum: number;
  linksNum: number;
  clickedVector: string;
  thresholds: threshMap;
  setThresholds: React.Dispatch<React.SetStateAction<threshMap>>;
}

export interface ISwitchableProps {
  setNamesStringMap: React.Dispatch<
    React.SetStateAction<INamesStringMap | undefined>
  >;
  orgName: string;
  suggestions: { [key: string]: string };
}

interface MenuItem {
  label: string;
  icon: IconProp;
  onClick?: () => void;
  submenu?: MenuItem[];
}

interface ContextMenuProps {
  position: { x: number; y: number };
  items: MenuItem[];
}