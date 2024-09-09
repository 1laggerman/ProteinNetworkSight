// import { FC, useCallback, useRef, useState } from "react";
// import { ForceGraph3D } from "react-force-graph";
// import useResizeObserver from "use-resize-observer";
// import { ICustomLink, ICustomNode } from "../@types/graphs";
// import { IGraphProps } from "../@types/props";
// import { ForceGraphMethods } from "react-force-graph-3d";
// import Panel from "./Panel";
// import "../styles/Graph.css";
// import "../styles/Button.css";
// import { SVGRenderer } from "three/examples/jsm/renderers/SVGRenderer.js";
// import * as THREE from "three";
// import ContextMenu from "./ContextMenu";
// import { TextGeometry } from "three/examples/jsm/geometries/TextGeometry";
// import { CSG } from "three-csg-ts";



// const Graph3DComponent: FC<IGraphProps> = ({
//   graphData,
//   clickedVector,
//   font,
// }) => {
//   const { ref, width = 1, height = 1 } = useResizeObserver();
//   const [openPanel, setOpenPanel] = useState(false);
//   const [panelData, setPanelData] = useState<ICustomNode>();
//   const [openContextMenu, setOpenContextMenu] = useState(false);
//   const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
//   const svgRef = useRef<ForceGraphMethods>();
//   const fileName = clickedVector + "_3Dgraph";


//   const handleOnClickNode = useCallback((node: ICustomNode) => {
//     setOpenPanel(true);
//     setPanelData({ ...node });
//   }, []);

//   const handleOnclickClosePanel = useCallback(() => {
//     setOpenPanel(false);
//   }, []);


//   const getTextMargin = (node: ICustomNode): number => {
//     if (!node.size) return 0;
//     if (getNodeSize(node) >= 20) return getNodeSize(node) + 10;
//     return 20;
//   };

//   // const getNodeLabel = (node: ICustomNode): string => {
//   //   return `<span style="color: #2f2f2f"> 
//   //                       ID: ${node.id} </br> 
//   //                       Value: ${node.size} </br> 
//   //                       size: ${getNodeSize(node)} </br> 
//   //                       STRING name: ${node.string_name} </span>`;
//   // };

//   const getLinkWidth = (link: ICustomLink) => { 
//     if (!link.score) return 0;
//     return link.score * 2 ;
//   };

//   const getLinkColor = (link: ICustomLink) => {
//       if (!link.score)  return "white"
//       if (link.score >= 0.95) return "black";
//       if (link.score >= 0.90) return "#101010";
//       if (link.score >= 0.8) return "#282828";
//       if (link.score >= 0.7) return "#383838";
//       if (link.score >= 0.6) return "#484848";
//       if (link.score >= 0.5) return "#585858";
//       if (link.score >= 0.4) return "#696969";
//       if (link.score >= 0.3) return "#888888";
//       return "white";
//   } ;

//   const getNodeSize = (node: ICustomNode): number => {
//     if (!node.size) return 0;
//     return Math.abs(node.size) * 100;
//   };

//   const updateNodePosition = (node: ICustomNode) => {
//     node.fx = node.x;
//     node.fy = node.y;
//     node.fz = node.z;
//   };


//   const showContextMenu = (event: MouseEvent) => {
//     // Disable the default context menu
//     event.preventDefault();

//     setOpenContextMenu(false);
//     const newPosition = {
//       x: event.pageX,
//       y: event.pageY,
//     };
//     setMenuPosition(newPosition);
//     setOpenContextMenu(true);
//   };

//   const hideContextMenu = () => {
//     setOpenContextMenu(false);
//   };

//   const btnSVGExportClick = () => {
//     //convert to svg
//     var rendererSVG = new SVGRenderer();
//     if (!svgRef.current) return;
//     var scene = svgRef.current.scene();
//     var camera = svgRef.current.camera();
//     var tempCamera = new THREE.PerspectiveCamera();
//     tempCamera.copy(camera as THREE.PerspectiveCamera, true);
//     tempCamera.aspect = width / height; // set the aspect ratio
//     tempCamera.updateProjectionMatrix();

//     rendererSVG.setSize(width, height);
//     rendererSVG.render(scene, tempCamera);

//     // create the file
//     var XMLS = new XMLSerializer();
//     var svgfile = XMLS.serializeToString(rendererSVG.domElement);
//     var svgData = svgfile;

//     var preface = '<?xml version="1.0" standalone="no"?>\r\n';
//     var svgBlob = new Blob([preface, svgData], {
//       type: "image/svg+xml;charset=utf-8",
//     });

//     // create download link and activate the downloading
//     var svgUrl = URL.createObjectURL(svgBlob);
//     var downloadLink = document.createElement("a");
    
//     downloadLink.href = svgUrl;
//     downloadLink.download = fileName + ".svg";

//     document.body.appendChild(downloadLink);
//     downloadLink.click();
//     document.body.removeChild(downloadLink);
//   };

// //   const btnPDFExportClick = async () => {
    
// // };

//   const getNodeThreeObject = (node: ICustomNode) => {
//     // create the circle
//     const circleGeo = new THREE.CircleGeometry(getNodeSize(node), 32);
//     const circleMat = new THREE.MeshBasicMaterial({
//       color: node.color,
//     });
//     const circleMesh = new THREE.Mesh(circleGeo, circleMat);
//     if (!font) return circleMesh;

//     // create the text
//     const textGeo = new TextGeometry(node.id as string, {
//       font: font,
//       size: 8,
//       height: 0.2,
//     });
//     textGeo.center();
//     const textMat = new THREE.MeshBasicMaterial({ color: 0x00000 });
//     const textMesh = new THREE.Mesh(textGeo, textMat);
//     textMesh.position.y = -getTextMargin(node);

//     // Merge meshes
//     circleMesh.updateMatrix();
//     textMesh.updateMatrix();
//     const uniRes = CSG.union(circleMesh, textMesh);

//     return uniRes;
//   };
//   return (
//     <div ref={ref} className="graph-container">
//       {openPanel && (
//         <Panel node={panelData} onClickClose={handleOnclickClosePanel} />
//       )}
//       {openContextMenu && (
//         <ContextMenu
//           position={menuPosition}
//           onSvgClick={btnSVGExportClick}
//           // onPdfClick={btnPDFExportClick}
//         />
//       )}
//       <ForceGraph3D
//         numDimensions={2}
//         showNavInfo={false}
//         ref={svgRef}
//         graphData={graphData}
//         height={height}
//         width={width}
//         backgroundColor={"white"}
//         onNodeClick={handleOnClickNode}
//         linkColor={getLinkColor}
//         linkWidth={getLinkWidth}
//         // nodeLabel={getNodeLabel}
//         onNodeDragEnd={updateNodePosition}
//         linkOpacity={0.5}
//         cooldownTicks={80}
//         // onEngineStop={() => svgRef.current?.zoomToFit(800)}
//         onEngineStop={() => svgRef.current?.d3Force("charge")?.strength(-100)}
//         nodeThreeObject={getNodeThreeObject}
//         onBackgroundRightClick={showContextMenu}
//         onBackgroundClick={hideContextMenu}
        
//       />
//     </div>
//   );
// };

// export default Graph3DComponent;
export{}
