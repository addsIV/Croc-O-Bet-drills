
import React from 'react';
import { HistoryItem } from '../types';
import StatusBadge from './StatusBadge';

interface HistorySidebarProps {
  history: HistoryItem[];
}

const HistorySidebar: React.FC<HistorySidebarProps> = ({ history }) => {
  return (
    <div className="bg-slate-900/50 rounded-xl p-4 h-full flex flex-col border border-slate-800">
      <h3 className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-4">Recent Hunts</h3>
      <div className="flex-1 overflow-y-auto space-y-2 pr-1 custom-scrollbar">
        {history.length === 0 && (
          <div className="text-slate-600 text-center py-8 italic text-sm">
            No rounds played yet...
          </div>
        )}
        {history.map((item) => (
          <div key={item.id} className="bg-slate-800/80 rounded-lg p-3 flex justify-between items-center border border-slate-700">
            <div>
              <div className="text-[10px] text-slate-500">{item.time}</div>
              <StatusBadge
                icon={item.status === 'WIN' ? 'Trophy' : 'Skull'}
                label={item.status}
                tone={item.status === 'WIN' ? 'win' : 'loss'}
              />
              <div className="text-sm font-bold">${item.bet.toFixed(2)}</div>
            </div>
            <div className="text-right">
              <div className={`text-xs font-bold ${item.status === 'WIN' ? 'text-green-400' : 'text-red-400'}`}>
                {item.multiplier.toFixed(2)}x
              </div>
              <div className={`text-sm font-black ${item.status === 'WIN' ? 'text-green-500' : 'text-slate-400'}`}>
                {item.status === 'WIN' ? `+$${item.win.toFixed(2)}` : '-'}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistorySidebar;
