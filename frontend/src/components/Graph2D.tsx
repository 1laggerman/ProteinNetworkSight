import { FC, MutableRefObject, useCallback, useEffect, useRef, useState } from "react";
import { ForceGraph2D } from "react-force-graph";
import useResizeObserver from "use-resize-observer";
import { ICustomNode, ICustomLink } from "../@types/graphs";
import { IGraphProps } from "../@types/props";
import Panel from "./Panel";
import "../styles/Graph.css";
import "../styles/Button.css";
import { ForceGraphMethods } from "react-force-graph-2d";
import ContextMenu from "./ContextMenu";
import jsPDF from "jspdf";


const Graph2DComponent: FC<IGraphProps> = ({ graphData, clickedVector }) => {
  const { ref, width = 1, height = 1 } = useResizeObserver();
  const [openPanel, setOpenPanel] = useState<boolean>(false);
  const [panelData, setPanelData] = useState<ICustomNode>();
  const [highlightNodes, setHighlightNodes] = useState(new Set());
  const [highlightLinks, setHighlightLinks] = useState(new Set());
  const [hoverNode, setHoverNode] = useState<ICustomNode>({});
  const [openContextMenu, setOpenContextMenu] = useState(false);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [canvas, setCanvas] = useState<HTMLCanvasElement>();
  const fgRef = useRef<ForceGraphMethods>();
  const fileName = clickedVector + "_2Dgraph";

  useEffect(() => {
    // Spread nodes a little wider
    // fgRef.current?.d3Force("charge")?.strength(-120);
  }, [fgRef.current]);

  const updateHighlight = () => {
    setHighlightNodes(highlightNodes);
    setHighlightLinks(highlightLinks);
  };

  const handleNodeHover = (node: ICustomNode) => {
    highlightNodes.clear();
    highlightLinks.clear();
    if (node) {
      highlightNodes.add(node);
      node.links &&
        node.links.forEach((link: string) => highlightNodes.add(link));

      node.links &&
        graphData.links.forEach((link: ICustomLink) => {
          if (link.source?.id === node.id) {
            highlightLinks.add(link);
            highlightNodes.add(link.target);
          }
          if (link.target?.id === node.id) {
            highlightLinks.add(link);
            highlightNodes.add(link.source);
          }
        });
    }

    setHoverNode(node);
    updateHighlight();
  };

  const handleLinkHover = (link: ICustomLink) => {
    highlightNodes.clear();
    highlightLinks.clear();

    if (link) {
      highlightLinks.add(link);
      highlightNodes.add(link.source);
      highlightNodes.add(link.target);
    }

    updateHighlight();
  };

  const handleOnClickNode = useCallback((node: ICustomNode) => {
    setOpenPanel(true);
    setPanelData({ ...node });
  }, []);

  const handleOnclickClosePanel = useCallback(() => {
    setOpenPanel(false);
  }, []);

  const getNodeColor = (node: ICustomNode): string => {
    return node.color ? node.color : "white";
  };

  const getNodeLabel = (node: ICustomNode): string => {
    return `<span style="color: #2f2f2f">${node.string_name}</span>`;
  };

  const getNodeSize = (node: ICustomNode): number => {
    return node.size ? node.size / 2 : 0;
  };

  const updateNodePosition = (node: ICustomNode) => {
    node.fx = node.x;
    node.fy = node.y;
    node.fz = node.z;
  };

  const getLinkWidth = (link: ICustomLink): number => {
    if (highlightLinks.has(link)) {
      return link.score ? link.score : 0;
    } else return link.score ? link.score / 5 : 0;
  };

  const customeNodeCanvasRender = (
    node: ICustomNode,
    ctx: CanvasRenderingContext2D,
    globalScale: number
  ) => {
    const label = node.id ? (node.id as string) : "";
    const fontSize = 12 / globalScale;
    ctx.font = `${fontSize}px Sans-Serif`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillStyle = "black"; //node.color;
    if (node.x && node.y && node.size) {
      ctx.fillText(label, node.x, node.y + node.size / 2 + 8);
    }

    // add ring just for highlighted nodes
    if (highlightNodes.has(node)) {
      ctx.beginPath();
      node.x &&
        node.y &&
        node.size &&
        ctx.arc(node.x, node.y, node.size / 2 + 3, 0, 2 * Math.PI, false);
      ctx.fillStyle = node === hoverNode ? "yellow" : "orange";
      ctx.fill();
    }
  };

  const showContextMenu = (event: MouseEvent) => {
    // Disable the default context menu
    event.preventDefault();
    setOpenContextMenu(false);
    const newPosition = {
      x: event.pageX,
      y: event.pageY,
    };
    setPosition(newPosition);
    setOpenContextMenu(true);
  };
  const onRenderFramePost = (canvasContext: CanvasRenderingContext2D) => {
    setCanvas(canvasContext.canvas);
  };

  const hideContextMenu = () => {
    setOpenContextMenu(false);
  };

  // const btnPDFExportClick = () => {
  //   if (!canvas) return;
  //   let width = canvas.width;
  //   let height = canvas.height;
  //   let pdf;
  //   if (width > height) {
  //     pdf = new jsPDF("l", "px", [width, height]);
  //   } else {
  //     pdf = new jsPDF("p", "px", [height, width]);
  //   }
  //   width = pdf.internal.pageSize.getWidth();
  //   height = pdf.internal.pageSize.getHeight();
  //   pdf.addImage(canvas, "PNG", 0, 0, width, height);
  //   pdf.save( fileName + ".pdf");
  // };

  const btnPNGExportClick = () => {
    let downloadLink = document.createElement("a");
    downloadLink.setAttribute("download", fileName + ".png");
    if (!canvas) return;
    let dataURL = canvas.toDataURL("image/png");
    let url = dataURL.replace(
      /^data:image\/png/,
      "data:application/octet-stream"
    );
    downloadLink.setAttribute("href", url);
    downloadLink.click();
  };

  return (
    <div ref={ref} className="graph-container">
      {openPanel && (
        <Panel node={panelData} onClickClose={handleOnclickClosePanel} />
      )}
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        height={height}
        width={width}
        backgroundColor={"white"}
        nodeVal={getNodeSize}
        nodeColor={getNodeColor}
        onNodeClick={handleOnClickNode}
        nodeLabel={getNodeLabel}
        onNodeDragEnd={updateNodePosition}
        linkWidth={getLinkWidth}
        cooldownTicks={40}
        onEngineStop={() => fgRef.current?.zoomToFit(800)}
        nodeCanvasObjectMode={() => "after"}
        nodeCanvasObject={customeNodeCanvasRender}
        //@ts-ignore
        onNodeHover={handleNodeHover}
        //@ts-ignore
        onLinkHover={handleLinkHover}
        onBackgroundRightClick={showContextMenu}
        onBackgroundClick={hideContextMenu}
        onRenderFramePost={onRenderFramePost}
      />
    </div>
  );
};

export default Graph2DComponent;
