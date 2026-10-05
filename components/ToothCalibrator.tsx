
import React, { useState, useRef } from 'react';
import { TOTAL_TEETH } from '../constants';
import crocodileImg from '../assets/crocodile.png';

interface Point {
  x: number;
  y: number;
  id: number;
}

const ToothCalibrator: React.FC<{ onSave: (points: Point[]) => void, onCancel: () => void }> = ({ onSave, onCancel }) => {
  const [points, setPoints] = useState<Point[]>([]);
  const imgRef = useRef<HTMLImageElement>(null);

  const handleImageClick = (e: React.MouseEvent<HTMLImageElement>) => {
    if (!imgRef.current) return;
    if (points.length >= TOTAL_TEETH) return;

    const rect = imgRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;

    setPoints([...points, { x, y, id: points.length }]);
  };

  const handleUndo = () => {
    setPoints(points.slice(0, -1));
  };

  const copyToClipboard = () => {
    const data = JSON.stringify(points, null, 2);
    navigator.clipboard.writeText(data);
    alert('Coordinates copied to clipboard!');
  };

  return (
    <div className="fixed inset-0 bg-slate-950 z-50 overflow-auto p-4 flex flex-col items-center">
      <div className="flex gap-4 mb-4 items-center">
        <h2 className="text-xl font-bold text-white">Tooth Calibrator ({points.length}/{TOTAL_TEETH})</h2>
        <button onClick={handleUndo} className="bg-slate-700 px-4 py-2 rounded text-white">Undo</button>
        <button onClick={() => setPoints([])} className="bg-red-700 px-4 py-2 rounded text-white">Clear</button>
        <button onClick={copyToClipboard} className="bg-blue-600 px-4 py-2 rounded text-white">Copy JSON</button>
        <button onClick={onCancel} className="bg-slate-600 px-4 py-2 rounded text-white">Close</button>
      </div>

      <div className="relative inline-block border-2 border-green-500 rounded-lg overflow-hidden">
        <img 
          ref={imgRef}
          src={crocodileImg} 
          alt="Calibration Reference" 
          className="max-w-[800px] w-full cursor-crosshair"
          onClick={handleImageClick}
        />
        {points.map((p, i) => (
          <div 
            key={i}
            className="absolute w-4 h-4 bg-red-500/50 border border-white rounded-full flex items-center justify-center text-[10px] font-bold text-white pointer-events-none transform -translate-x-1/2 -translate-y-1/2"
            style={{ left: `${p.x}%`, top: `${p.y}%` }}
          >
            {i}
          </div>
        ))}
      </div>

      <div className="mt-4 p-4 bg-slate-900 w-full max-w-[800px] text-xs font-mono text-green-400 rounded overflow-auto h-32">
        {JSON.stringify(points, null, 2)}
      </div>
    </div>
  );
};

export default ToothCalibrator;
