import React from 'react';
import { useSceneStore } from '../smart2dcanvas/Smart2Dcanvas_SceneStore';
import { Pro2D_getLeftRailTools, Pro2D_getBlockedToolMessage } from './Pro2D_ToolRegistry.mjs';

const TOOLS = Pro2D_getLeftRailTools();

type Pro2DLeftRailProps = {
  onBlockedTool?: (tool: any) => void;
};

const Pro2D_LeftRail: React.FC<Pro2DLeftRailProps> = ({ onBlockedTool }) => {
  const activeTool = useSceneStore((state) => state.activeTool);
  const setActiveTool = useSceneStore((state) => state.setActiveTool);

  return (
    <div className="w-24 border-r border-slate-800 bg-slate-950/80 p-2 flex flex-col gap-2 overflow-auto">
      {TOOLS.map((tool: any) => {
        const blocked = tool.implemented === false;
        const message = blocked ? Pro2D_getBlockedToolMessage(tool) : tool.label;
        return (
          <button
            key={tool.id}
            type="button"
            aria-disabled={blocked}
            className={`rounded-lg border px-2 py-2 text-xs text-center ${blocked ? 'border-rose-950 bg-slate-950 text-slate-500 opacity-80' : activeTool === tool.id ? 'border-amber-500 bg-amber-500/10 text-amber-200' : 'border-slate-700 bg-slate-900 text-slate-300 hover:border-slate-500'}`}
            onClick={() => {
              if (blocked) {
                onBlockedTool?.(tool);
                return;
              }
              setActiveTool(tool.id as any);
            }}
            title={message}
          >
            <div className="text-base">{tool.icon}</div>
            <div className="mt-1 leading-tight">{tool.label}</div>
            {blocked ? <div className="mt-1 text-[10px] uppercase tracking-wide text-rose-300/80">Planned</div> : null}
          </button>
        );
      })}
    </div>
  );
};

export default Pro2D_LeftRail;
