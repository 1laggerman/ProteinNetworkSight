import type { NodeObject, LinkObject, GraphData } from "react-force-graph-3d";

export interface ICustomNode extends NodeObject {
  originalName?: string;
  string_name?: string;
  info?: string;
  color?: string;
  size?: number;
  drug?: string;
  links?: string[];
  linksWeights?: number;
}

export interface ICustomLink extends LinkObject {
  index?: number;
  score?: number;
  source?: any;
  target?: any;
}

export interface ICustomGraphData extends GraphData {
  nodes: ICustomNode[];
  links: ICustomLink[];
}

export interface IObjectNode {
  nodeCanvasObjectMode:
    | string
    | ((obj: NodeObject) => CanvasCustomRenderMode)
    | undefined;
  nodeCanvasObject: CanvasCustomRenderFn<NodeObject> | undefined;
  nodeThreeObjectExtend: NodeAccessor$1<boolean> | undefined;
}
