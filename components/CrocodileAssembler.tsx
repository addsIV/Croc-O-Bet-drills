
import React, { useState, useEffect, useRef } from 'react';
import { TEETH_LAYOUT } from '../services/teeth_layout';
import { Eye, EyeOff, Save } from 'lucide-react';

// Use 4096 as internal reference size
const CANVAS_BASE = 4096;

interface Layer {
    id: string; // "ref", "base", "tooth-0", etc.
    name: string;
    image: string;
    x: number;
    y: number;
    width: number;
    height: number;
    opacity: number;
    visible: boolean;
    zIndex: number;
    isLocked?: boolean;
}

const CrocodileAssembler: React.FC<{ onBack: () => void }> = ({ onBack }) => {
    const [scale, setScale] = useState(0.2); // View scale (to fit 4096 on screen)
    const [selectedId, setSelectedId] = useState<string | null>(null);
    const [layers, setLayers] = useState<Layer[]>([]);

    // Initialize Layers
    useEffect(() => {
        const initLayers: Layer[] = [];

        // 1. Reference (Croc01) - Bottom
        initLayers.push({
            id: 'ref',
            name: 'Reference (Croc01)',
            image: '/croc01.png',
            x: 0,
            y: 0,
            width: 4096,
            height: 4096,
            opacity: 0.3,
            visible: true,
            zIndex: 0,
            isLocked: true
        });

        // 2. Base (No Tooth)
        initLayers.push({
            id: 'base',
            name: 'Base (No Tooth)',
            image: '/croc_no_tooth01.png',
            x: 0,
            y: 0,
            width: 4096,
            height: 4096,
            opacity: 1.0,
            visible: true,
            zIndex: 1,
            isLocked: true
        });

        // 3. Teeth
        TEETH_LAYOUT.teeth.forEach(t => {
            // Convert % to pixels relative to 4096
            const x = (t.left_pct / 100) * 4096;
            const y = (t.top_pct / 100) * 4096;
            const w = (t.width_pct / 100) * 4096;

            // Initial Height guess logic (based on w and aspect ratio? We don't know aspect ratio yet).
            // We'll let the image element determine height naturally, but store a value to track override.
            // If the user wants to resize, we need W and H.
            // Let's default H to 0 (auto) and handle logic to set it once loaded?
            // Actually, we can just use W and aspect for now.
            // In layout we usually only stored Width %. 

            initLayers.push({
                id: `tooth-${t.id}`,
                name: `Tooth ${t.id}`,
                image: `/teeth/${t.image}`,
                x,
                y,
                width: w,
                height: 0, // Auto
                opacity: 1.0,
                visible: true,
                zIndex: 10 + t.id
            });
        });

        setLayers(initLayers);
    }, []);

    const updateLayer = (id: string, updates: Partial<Layer>) => {
        setLayers(prev => prev.map(l => l.id === id ? { ...l, ...updates } : l));
    };

    const handleExport = () => {
        // Convert back to layout format
        // We only care about Teeth layers

        const newTeeth = layers.filter(l => l.id.startsWith('tooth-')).map(l => {
            const tid = parseInt(l.id.replace('tooth-', ''));

            return {
                id: tid,
                image: `tooth${tid < 10 ? '0' + tid : tid}.png`,
                left_pct: (l.x / 4096) * 100,
                top_pct: (l.y / 4096) * 100,
                width_pct: (l.width / 4096) * 100
            };
        });

        const output = {
            base_width: 4096,
            base_height: 4096,
            teeth: newTeeth
        };

        const jsonStr = JSON.stringify(output, null, 2);
        console.log(jsonStr);
        navigator.clipboard.writeText(jsonStr);
        alert("Layout JSON copied to clipboard! (Check Console too)");
    };

    const selectedLayer = layers.find(l => l.id === selectedId);

    return (
        <div className="flex h-screen w-full bg-gray-900 text-white overflow-hidden">
            {/* Sidebar */}
            <div className="w-80 flex flex-col border-r border-gray-700 bg-gray-800 p-4 overflow-y-auto">
                <h2 className="text-xl font-bold mb-4">Assembler Layers</h2>
                <div className="space-y-2 mb-4">
                    {layers.slice().reverse().map(layer => (
                        <div
                            key={layer.id}
                            className={`flex items-center p-2 rounded cursor-pointer ${selectedId === layer.id ? 'bg-blue-600' : 'hover:bg-gray-700'}`}
                            onClick={() => setSelectedId(layer.id)}
                        >
                            <button
                                onClick={(e) => { e.stopPropagation(); updateLayer(layer.id, { visible: !layer.visible }); }}
                                className="mr-2 text-gray-400 hover:text-white"
                            >
                                {layer.visible ? <Eye size={16} /> : <EyeOff size={16} />}
                            </button>
                            <span className="text-sm truncate flex-1">{layer.name}</span>
                        </div>
                    ))}
                </div>

                {selectedLayer && (
                    <div className="border-t border-gray-600 pt-4 mt-auto">
                        <h3 className="font-bold mb-2 text-blue-400">{selectedLayer.name}</h3>

                        <div className="grid grid-cols-2 gap-2 text-xs">
                            <label>Opacity</label>
                            <input
                                type="range" min="0" max="1" step="0.1"
                                value={selectedLayer.opacity}
                                onChange={(e) => updateLayer(selectedLayer.id, { opacity: parseFloat(e.target.value) })}
                            />

                            <label>X (px)</label>
                            <input
                                type="number"
                                value={Math.round(selectedLayer.x)}
                                onChange={(e) => updateLayer(selectedLayer.id, { x: parseInt(e.target.value) })}
                                className="bg-gray-700 p-1 rounded"
                            />

                            <label>Y (px)</label>
                            <input
                                type="number"
                                value={Math.round(selectedLayer.y)}
                                onChange={(e) => updateLayer(selectedLayer.id, { y: parseInt(e.target.value) })}
                                className="bg-gray-700 p-1 rounded"
                            />

                            <label>Width (px)</label>
                            <input
                                type="number"
                                value={Math.round(selectedLayer.width)}
                                onChange={(e) => updateLayer(selectedLayer.id, { width: parseInt(e.target.value) })}
                                className="bg-gray-700 p-1 rounded"
                            />

                            {/* Height is auto for now, usually */}
                        </div>
                    </div>
                )}

                <div className="mt-4 flex gap-2">
                    <button onClick={handleExport} className="flex-1 bg-green-600 p-2 rounded flex items-center justify-center gap-2 font-bold">
                        <Save size={16} /> Export JSON
                    </button>
                    <button onClick={onBack} className="bg-gray-600 p-2 rounded">
                        Exit
                    </button>
                </div>
            </div>

            {/* Viewport */}
            <div className="flex-1 overflow-auto bg-gray-950 relative flex items-center justify-center p-10">

                {/* Stage */}
                <div
                    className="relative bg-checkerboard shadow-2xl"
                    style={{
                        width: CANVAS_BASE * scale,
                        height: CANVAS_BASE * scale,
                        backgroundImage: 'radial-gradient(#333 1px, transparent 1px)',
                        backgroundSize: '20px 20px'
                    }}
                >
                    {/* Render Layers */}
                    {layers.map(layer => {
                        if (!layer.visible) return null;

                        return (
                            <img
                                key={layer.id}
                                src={layer.image}
                                alt={layer.name}
                                className="absolute select-none"
                                style={{
                                    left: layer.x * scale,
                                    top: layer.y * scale,
                                    width: layer.width * scale,
                                    // Height auto to preserve aspect
                                    height: layer.height ? layer.height * scale : 'auto',
                                    opacity: layer.opacity,
                                    zIndex: layer.zIndex,
                                    outline: selectedId === layer.id ? '2px solid #3b82f6' : 'none'
                                }}
                                draggable={false}
                                onClick={(e) => {
                                    e.stopPropagation(); // prevent stage click?
                                    setSelectedId(layer.id);
                                }}
                            />
                        );
                    })}

                </div>

                {/* View Controls */}
                <div className="absolute top-4 right-4 bg-gray-800 p-2 rounded flex gap-2">
                    <button onClick={() => setScale(s => Math.max(0.05, s - 0.05))} className="px-2 bg-gray-700 rounded">-</button>
                    <span className="text-xs flex items-center">{Math.round(scale * 100)}%</span>
                    <button onClick={() => setScale(s => Math.min(1.0, s + 0.05))} className="px-2 bg-gray-700 rounded">+</button>
                </div>
            </div>
        </div>
    );
};

export default CrocodileAssembler;
