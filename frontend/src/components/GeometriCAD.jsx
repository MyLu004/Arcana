import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Stage, Layer, Rect, Circle, Line, Text, Group } from "react-konva";

/**
 * GeometricCADCanvas.jsx
 *
 * A whiteboard/CAD-like sketch surface for interior layouts with:
 * - Pan & zoom, snapping grid, rulers
 * - Shapes: rectangle, circle, line/arrow, freehand, text labels
 * - Dimensions overlay (W×H on selected rects)
 * - Tool palette & layers list
 * - Export to PNG -> uploads to backend /upload-image
 * - "Generate Design" calls /agent/design/multi with the uploaded control image URL
 *
 * Tailwind classes used for styling. Ensure you have Tailwind set up.
 * Dependencies: react-konva, konva
 *   npm i react-konva konva
 */

const TOOLS = {
  SELECT: "select",
  RECT: "rect",
  CIRCLE: "circle",
  LINE: "line",
  PENCIL: "pencil",
  TEXT: "text",
};

const ROOM_TYPES = [
  { label: "Living Room", value: "living_room" },
  { label: "Bedroom", value: "bedroom" },
  { label: "Kitchen", value: "kitchen" },
  { label: "Office", value: "office" },
];

const ROOM_SIZES = [
  { label: "Small", value: "small" },
  { label: "Medium", value: "medium" },
  { label: "Large", value: "large" },
];

const GRID_SIZE = 20; // px
const SNAP = 5; // px

export default function GeometricCADCanvas({
  apiBase = "http://localhost:8000",
  onDesignReady, // callback(designResult)
  className = "",
}) {
  const stageRef = useRef(null);
  const layerRef = useRef(null);

  const [tool, setTool] = useState(TOOLS.SELECT);
  const [shapes, setShapes] = useState([]); // {id,type,props}
  const [lines, setLines] = useState([]); // for pencil/line
  const [isDrawing, setIsDrawing] = useState(false);
  const [selectedId, setSelectedId] = useState(null);

  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const [prompt, setPrompt] = useState("Cozy modern with warm neutrals and natural wood accents");
  const [roomType, setRoomType] = useState("living_room");
  const [roomSize, setRoomSize] = useState("medium");
  const [styles, setStyles] = useState("modern, scandinavian");
  const [budget, setBudget] = useState(3500);

  const [busy, setBusy] = useState(false);
  const [uploadUrl, setUploadUrl] = useState(null);
  const [error, setError] = useState(null);

  // Grid lines memo
  const gridLines = useMemo(() => {
    if (!stageRef.current) return { v: [], h: [] };
    const stage = stageRef.current.getStage();
    const width = stage.width() / scale;
    const height = stage.height() / scale;
    const v = [];
    const h = [];
    for (let i = -100; i < width + 100; i += GRID_SIZE) v.push(i);
    for (let j = -100; j < height + 100; j += GRID_SIZE) h.push(j);
    return { v, h };
  }, [scale]);

  const snapToGrid = (val) => Math.round(val / SNAP) * SNAP;

  const deselectAll = () => setSelectedId(null);

  // Zoom
  const handleWheel = (e) => {
    e.evt.preventDefault();
    const stage = stageRef.current.getStage();
    const oldScale = stage.scaleX();
    const pointer = stage.getPointerPosition();
    const mousePointTo = {
      x: (pointer.x - stage.x()) / oldScale,
      y: (pointer.y - stage.y()) / oldScale,
    };
    const direction = e.evt.deltaY > 0 ? -1 : 1;
    const scaleBy = 1.06;
    const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy;

    setScale(newScale);
    setPosition({
      x: pointer.x - mousePointTo.x * newScale,
      y: pointer.y - mousePointTo.y * newScale,
    });
  };

  // Panning
  const [panning, setPanning] = useState(false);
  const [lastPos, setLastPos] = useState(null);

  const onMouseDown = (e) => {
    const stage = stageRef.current.getStage();
    const pos = stage.getPointerPosition();
    const { x, y } = screenToWorld(pos.x, pos.y);

    if (tool === TOOLS.SELECT) {
      // start panning with middle/right button or spacebar? For simplicity: hold space to pan
      if (e.evt.button === 1) {
        setPanning(true);
        setLastPos({ x: pos.x, y: pos.y });
        return;
      }
      // selection logic
      const clickedOnEmpty = e.target === stage;
      if (clickedOnEmpty) deselectAll();
      return;
    }

    setIsDrawing(true);

    if (tool === TOOLS.RECT) {
      const id = `rect-${Date.now()}`;
      const rect = {
        id,
        type: TOOLS.RECT,
        props: { x: snapToGrid(x), y: snapToGrid(y), width: 0, height: 0, fill: "rgba(99,102,241,0.1)", stroke: "#6366f1", strokeWidth: 2, name: "Rect" },
      };
      setShapes((prev) => [...prev, rect]);
      setSelectedId(id);
    } else if (tool === TOOLS.CIRCLE) {
      const id = `circle-${Date.now()}`;
      const c = { id, type: TOOLS.CIRCLE, props: { x: snapToGrid(x), y: snapToGrid(y), radius: 1, fill: "rgba(16,185,129,0.1)", stroke: "#10b981", strokeWidth: 2, name: "Circle" } };
      setShapes((prev) => [...prev, c]);
      setSelectedId(id);
    } else if (tool === TOOLS.LINE) {
      const id = `line-${Date.now()}`;
      const l = { id, points: [snapToGrid(x), snapToGrid(y), snapToGrid(x), snapToGrid(y)], stroke: "#f59e0b", strokeWidth: 3 };
      setLines((p) => [...p, l]);
      setSelectedId(id);
    } else if (tool === TOOLS.PENCIL) {
      const id = `pencil-${Date.now()}`;
      const l = { id, points: [snapToGrid(x), snapToGrid(y)], stroke: "#fff", strokeWidth: 2, tension: 0.5 }; // freehand line
      setLines((p) => [...p, l]);
      setSelectedId(id);
    } else if (tool === TOOLS.TEXT) {
      const id = `text-${Date.now()}`;
      const t = { id, type: TOOLS.TEXT, props: { x: x, y: y, text: "Label", fontSize: 16, fill: "#111827" } };
      setShapes((prev) => [...prev, t]);
      setSelectedId(id);
    }
  };

  const onMouseMove = (e) => {
    const stage = stageRef.current.getStage();
    const pos = stage.getPointerPosition();

    if (panning && lastPos) {
      const dx = pos.x - lastPos.x;
      const dy = pos.y - lastPos.y;
      setPosition((p) => ({ x: p.x + dx, y: p.y + dy }));
      setLastPos({ x: pos.x, y: pos.y });
      return;
    }

    if (!isDrawing) return;

    const { x, y } = screenToWorld(pos.x, pos.y);

    if (tool === TOOLS.RECT) {
      setShapes((prev) =>
        prev.map((s) => {
          if (s.id !== selectedId) return s;
          const w = snapToGrid(x - s.props.x);
          const h = snapToGrid(y - s.props.y);
          return { ...s, props: { ...s.props, width: w, height: h } };
        })
      );
    } else if (tool === TOOLS.CIRCLE) {
      setShapes((prev) =>
        prev.map((s) => {
          if (s.id !== selectedId) return s;
          const dx = x - s.props.x;
          const dy = y - s.props.y;
          const r = Math.max(1, Math.sqrt(dx * dx + dy * dy));
          return { ...s, props: { ...s.props, radius: r } };
        })
      );
    } else if (tool === TOOLS.LINE) {
      setLines((prev) =>
        prev.map((l) => (l.id === selectedId ? { ...l, points: [l.points[0], l.points[1], snapToGrid(x), snapToGrid(y)] } : l))
      );
    } else if (tool === TOOLS.PENCIL) {
      setLines((prev) =>
        prev.map((l) => (l.id === selectedId ? { ...l, points: [...l.points, snapToGrid(x), snapToGrid(y)] } : l))
      );
    }
  };

  const onMouseUp = () => {
    setIsDrawing(false);
    setPanning(false);
    setLastPos(null);
  };

  const screenToWorld = (sx, sy) => {
    const stage = stageRef.current.getStage();
    const wx = (sx - position.x) / scale;
    const wy = (sy - position.y) / scale;
    return { x: wx, y: wy };
  };

  const worldToScreen = (wx, wy) => ({ x: wx * scale + position.x, y: wy * scale + position.y });

  // Export current canvas to image & upload
  const exportAndUpload = async () => {
    setBusy(true);
    setError(null);
    try {
      const stage = stageRef.current.getStage();
      // High-res export
      const dataURL = stage.toDataURL({ pixelRatio: 2, mimeType: "image/png" });

      const blob = await (await fetch(dataURL)).blob();
      const file = new File([blob], `sketch-${Date.now()}.png`, { type: "image/png" });

      const form = new FormData();
      form.append("file", file);

      const res = await fetch(`${apiBase}/upload-image`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
      const json = await res.json();
      setUploadUrl(json.url);
      return json.url;
    } catch (e) {
      console.error(e);
      setError(e.message || "Upload failed");
    } finally {
      setBusy(false);
    }
  };

  const handleGenerate = async () => {
    const url = await exportAndUpload();
    if (!url) return;

    setBusy(true);
    setError(null);
    try {
      // Build request matching backend DesignRequest
      const payload = {
        prompt,
        room_type: roomType,
        room_size: roomSize,
        style_preferences: styles
          .split(",")
          .map((s) => s.trim())
          .filter(Boolean),
        budget_max: Number(budget) || null,
      };

      // Kick multi-agent pipeline
      // NOTE: main.py currently uses a placeholder control_image_url internally.
      // If you want to force using this sketch, you can update main.py to accept control_image_url from client
      // and pass it into orchestrator.orchestrate_design. For now we still upload (so you have a URL),
      // and you can wire it in backend.

      const res = await fetch(`${apiBase}/agent/design/multi`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error(`Design failed: ${res.status}`);
      const design = await res.json();

      // surface to parent (chat) if provided
      onDesignReady && onDesignReady(design);
    } catch (e) {
      console.error(e);
      setError(e.message || "Design generation failed");
    } finally {
      setBusy(false);
    }
  };

  // Toolbar button
  const ToolButton = ({ name, active, onClick, children }) => (
    <button
      onClick={onClick}
      className={`px-2 py-1 rounded-md text-sm border ${
        active ? "bg-[var(--color-secondary)] text-white" : "bg-white text-gray-800 border-gray-300"
      } hover:shadow transition`}
      title={name}
    >
      {children}
    </button>
  );

  // Rulers
 const Rulers = () => {
   // how many grid steps are visible on each axis (+padding)
   const stepPx = GRID_SIZE * scale;
   const padSteps = 2;
   const startCol = Math.floor((-position.x) / stepPx) - padSteps;
   const endCol   = Math.ceil((stageSize.width - position.x) / stepPx) + padSteps;
   const startRow = Math.floor((-position.y) / stepPx) - padSteps;
   const endRow   = Math.ceil((stageSize.height - position.y) / stepPx) + padSteps;

   const cols = [];
   for (let i = startCol; i <= endCol; i++) cols.push(i);
   const rows = [];
   for (let j = startRow; j <= endRow; j++) rows.push(j);

   return (
     <>
       {/* top ruler */}
      <div className="absolute left-0 right-0 top-0 h-6 bg-white border-b border-gray-200 flex items-end text-[10px] text-gray-600 select-none pointer-events-none">
        <div className="relative w-full h-full">
          {cols.map((i) => {
            const left = i * stepPx + position.x;
            if (left < -20 || left > stageSize.width + 20) return null;
            return (
              <div key={i} className="absolute" style={{ left }}>
                <div className="h-3 w-px bg-gray-300" />
                <div className="translate-x-[-50%]">{i * GRID_SIZE}</div>
              </div>
            );
          })}
         </div>
       </div>
       {/* left ruler */}
       <div className="absolute left-2 top-0 bottom-0 w-5 bg-gray-100 border-r border-gray-200 text-[10px] text-gray-600 select-none pointer-events-none">
         <div className="relative w-full h-full">
           {rows.map((j) => {
             const top = j * stepPx + position.y;
             if (top < -20 || top > stageSize.height + 20) return null;
             return (
               <div key={j} className="absolute" style={{ top }}>
                 <div className="w-3 h-px bg-gray-300" />
                 <div className="-rotate-90 origin-left">{j * GRID_SIZE}</div>
               </div>
             );
           })}
         </div>
       </div>
     </>
   );
 };
  // Dimensions overlay for selected rects
  const Dimensions = ({ shape }) => {
    if (!shape || shape.type !== TOOLS.RECT) return null;
    const { x, y, width, height } = shape.props;
    const { x: sx, y: sy } = worldToScreen(x, y);
    const { x: ex, y: ey } = worldToScreen(x + width, y + height);
    const w = Math.abs(ex - sx);
    const h = Math.abs(ey - sy);
    return (
      <div
        className="pointer-events-none absolute text-[10px] bg-black/70 text-white px-1 py-0.5 rounded"
        style={{ left: Math.min(sx, ex) + w / 2 - 20, top: Math.min(sy, ey) - 16 }}
      >
        {Math.abs(width)}×{Math.abs(height)} px
      </div>
    );
  };

    const wrapRef = useRef(null);
    const [stageSize, setStageSize] = useState({ width: 1200, height: 700 });

    useEffect(() => {
    if (!wrapRef.current) return;
    const ro = new ResizeObserver(([entry]) => {
        const { width, height } = entry.contentRect;
        setStageSize({ width, height });
    });
    ro.observe(wrapRef.current);
    return () => ro.disconnect();
    }, []);

  return (
    <div className={`flex flex-col h-[calc(100dvh-4rem)] ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between p-3 bg-white border-b">
        <div className="flex items-center gap-2">
          <span className="font-semibold">Geometric CAD</span>
          <span className="text-xs text-gray-500">whiteboard & layout sketch</span>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={roomType}
            onChange={(e) => setRoomType(e.target.value)}
            className="border rounded px-2 py-1 text-sm"
          >
            {ROOM_TYPES.map((r) => (
              <option key={r.value} value={r.value}>{r.label}</option>
            ))}
          </select>
          <select
            value={roomSize}
            onChange={(e) => setRoomSize(e.target.value)}
            className="border rounded px-2 py-1 text-sm"
          >
            {ROOM_SIZES.map((r) => (
              <option key={r.value} value={r.value}>{r.label}</option>
            ))}
          </select>
          <input
            className="border rounded px-2 py-1 text-sm w-72"
            placeholder="Style preferences (comma separated)"
            value={styles}
            onChange={(e) => setStyles(e.target.value)}
          />
          <input
            type="number"
            className="border rounded px-2 py-1 text-sm w-28"
            placeholder="Budget"
            value={budget}
            onChange={(e) => setBudget(e.target.value)}
          />
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex items-center gap-2 p-2 bg-gray-50 border-b">

        <div className="flex flex-col gap-5">
            <div className="flex gap-3">
                <ToolButton name="Select" active={tool === TOOLS.SELECT} onClick={() => setTool(TOOLS.SELECT)}>↖︎ Select</ToolButton>
                <ToolButton name="Rect" active={tool === TOOLS.RECT} onClick={() => setTool(TOOLS.RECT)}>▭ Rect</ToolButton>
                <ToolButton name="Circle" active={tool === TOOLS.CIRCLE} onClick={() => setTool(TOOLS.CIRCLE)}>◯ Circle</ToolButton>
                <ToolButton name="Line" active={tool === TOOLS.LINE} onClick={() => setTool(TOOLS.LINE)}>／ Line</ToolButton>
                <ToolButton name="Pencil" active={tool === TOOLS.PENCIL} onClick={() => setTool(TOOLS.PENCIL)}>✎ Pencil</ToolButton>
                <ToolButton name="Text" active={tool === TOOLS.TEXT} onClick={() => setTool(TOOLS.TEXT)}>T Text</ToolButton>
            </div>

            {/* <div className="mx-3 h-6 w-px bg-gray-300" /> */}

            <div className="flex gap-3">
                <button
                    onClick={() => {
                        setScale(1);
                        setPosition({ x: 0, y: 0 });
                    }}
                    className="px-2 py-1 text-sm rounded border bg-white hover:shadow"
                >
                Reset View
                </button>
                <button
                onClick={() => {
                    setShapes([]);
                    setLines([]);
                    deselectAll();
                }}
                className="px-2 py-1 text-sm rounded border bg-white hover:shadow"
                >
                Clear
                </button>
                <div className="ml-auto flex items-center gap-2">
                    <input
                        className="border rounded px-2 py-1 text-sm w-96"
                        placeholder="Describe the vibe… (prompt used by AI)"
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                    />
                    <button
                        onClick={handleGenerate}
                        disabled={busy}
                        className={`px-3 py-2 rounded-lg text-white text-sm font-semibold ${
                        busy ? "bg-blue-300" : "bg-blue-600 hover:bg-blue-700"
                        }`}
                    >
                    {busy ? "Generating…" : "Generate Design"}
                    </button>
                </div>

            </div>
        
        </div>
      </div>

      {/* Canvas wrapper with rulers */}
      <div ref={wrapRef} className="relative flex-1 bg-[#121212] overflow-hidden">
        <Rulers />
        {/* Stage */}
        <Stage
          ref={stageRef}
          width={stageSize.width}
          height={stageSize.height}
          scaleX={scale}
          scaleY={scale}
          x={position.x}
          y={position.y}
          onWheel={handleWheel}
          onMouseDown={onMouseDown}
          onMousemove={onMouseMove}
          onMouseup={onMouseUp}
          className="cursor-crosshair"
        >
          {/* Grid */}
          <Layer listening={false}>
            {gridLines.v.map((x, i) => (
              <Line key={`v-${i}`} points={[x, -2000, x, 2000]} stroke="#222" strokeWidth={1} />
            ))}
            {gridLines.h.map((y, i) => (
              <Line key={`h-${i}`} points={[-2000, y, 2000, y]} stroke="#222" strokeWidth={1} />
            ))}
          </Layer>

          {/* Shapes & lines */}
          <Layer ref={layerRef}>
            {shapes.map((s) => {
              if (s.type === TOOLS.RECT) {
                return (
                  <Group key={s.id} onClick={() => setSelectedId(s.id)}>
                    <Rect {...s.props} />
                  </Group>
                );
              }
              if (s.type === TOOLS.CIRCLE) {
                return (
                  <Group key={s.id} onClick={() => setSelectedId(s.id)}>
                    <Circle {...s.props} />
                  </Group>
                );
              }
              if (s.type === TOOLS.TEXT) {
                return <Text key={s.id} {...s.props} onClick={() => setSelectedId(s.id)} draggable />;
              }
              return null;
            })}

            {lines.map((l) => (
              <Line key={l.id} points={l.points} stroke={l.stroke} strokeWidth={l.strokeWidth} lineCap="round" lineJoin="round" />
            ))}
          </Layer>
        </Stage>

        {/* Dimension tag */}
        <Dimensions shape={shapes.find((s) => s.id === selectedId)} />
      </div>

      {/* Footer status */}
      <div className="flex items-center justify-between p-2 text-xs bg-white border-t">
        <div className="flex gap-3 text-gray-600">
          <span>Tool: <b>{tool}</b></span>
          <span>Scale: {(scale * 100).toFixed(0)}%</span>
          <span>Shapes: {shapes.length} | Lines: {lines.length}</span>
          {uploadUrl && <span className="text-green-600">Uploaded: {uploadUrl}</span>}
        </div>
        {error && <div className="text-red-600">{error}</div>}
      </div>
    </div>
  );
}
