
import React, { useState, lazy, Suspense } from 'react';
import { Coins, Flame, Skull, TrendingUp, Info } from 'lucide-react';
import { TOTAL_TEETH } from './constants';
import Crocodile from './components/Crocodile';
const CrocodileAssembler = lazy(() => import('./components/CrocodileAssembler'));
import HistorySidebar from './components/HistorySidebar';
import { PenTool } from 'lucide-react';
import { useCrocGame } from './src/hooks/useCrocGame';

const App: React.FC = () => {
  const {
    balance,
    betAmount,
    setBetAmount,
    trapCount,
    setTrapCount,
    status,
    clickedTeeth,
    trapPositions,
    history,
    currentMultiplier,
    nextMultiplier,
    isShaking,
    handleStartGame,
    handleToothClick,
    handleCashOut,
    handleReset
  } = useCrocGame();

  const [showAssembler, setShowAssembler] = useState(false);

  if (showAssembler) {
    return (
      <Suspense fallback={<div className="p-8 text-slate-400">Loading assembler…</div>}>
        <CrocodileAssembler onBack={() => setShowAssembler(false)} />
      </Suspense>
    );
  }

  return (
    <div className="min-h-screen flex flex-col lg:flex-row bg-slate-950 text-slate-100 overflow-hidden relative">
      {/* Dev Tools Button */}
      <button
        onClick={() => setShowAssembler(true)}
        className="fixed bottom-4 left-4 z-50 bg-slate-800 p-2 rounded-full opacity-50 hover:opacity-100 transition-opacity"
        title="Open Assembler Tool"
      >
        <PenTool size={16} />
      </button>

      {/* Left Sidebar - Controls */}
      <div className="w-full lg:w-[350px] bg-slate-900 border-r border-slate-800 p-6 flex flex-col gap-6 z-10 shadow-2xl">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center shadow-lg shadow-green-500/20">
            <Flame className="text-white" size={24} />
          </div>
          <h1 className="text-2xl font-bangers tracking-wider text-green-500">CROC-O-BET</h1>
        </div>

        <div className="bg-slate-950/50 rounded-xl p-4 border border-slate-800 flex items-center justify-between">
          <div className="flex flex-col">
            <span className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Balance</span>
            <span className="text-xl font-bold flex items-center gap-2">
              <Coins className="text-yellow-500" size={18} />
              ${balance.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
            </span>
          </div>
        </div>

        {/* Bet Controls */}
        <div className="flex flex-col gap-4">
          <div className="flex flex-col gap-1.5">
            <label className="text-xs text-slate-400 font-bold uppercase ml-1">Bet Amount</label>
            <div className="flex gap-2">
              <div className="relative flex-1">
                <input
                  type="number"
                  value={betAmount}
                  onChange={(e) => setBetAmount(Math.max(0.1, parseFloat(e.target.value) || 0))}
                  disabled={status === 'PLAYING'}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg py-3 px-4 text-sm font-bold focus:outline-none focus:ring-2 focus:ring-green-500/50 disabled:opacity-50"
                />
              </div>
              <div className="flex gap-1">
                <button onClick={() => setBetAmount(prev => prev / 2)} className="bg-slate-800 hover:bg-slate-700 px-3 rounded-lg text-xs font-bold transition-colors">1/2</button>
                <button onClick={() => setBetAmount(prev => prev * 2)} className="bg-slate-800 hover:bg-slate-700 px-3 rounded-lg text-xs font-bold transition-colors">2x</button>
              </div>
            </div>
          </div>

          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between items-center ml-1">
              <label className="text-xs text-slate-400 font-bold uppercase">Sore Teeth</label>
              <span className="text-xs font-bold text-red-500 flex items-center gap-1">
                <Skull size={12} /> {trapCount} Traps
              </span>
            </div>
            <input
              type="range"
              min="1"
              max="19"
              value={trapCount}
              onChange={(e) => setTrapCount(parseInt(e.target.value))}
              disabled={status === 'PLAYING'}
              className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-red-500 disabled:opacity-30"
            />
            <div className="flex justify-between px-1 text-[10px] text-slate-600 font-bold">
              <span>EASY</span>
              <span>INSANE</span>
            </div>
          </div>

          <div className="pt-2">
            {status === 'BETTING' || status === 'BITTEN' || status === 'CASHED_OUT' ? (
              <button
                onClick={status === 'BETTING' ? handleStartGame : handleReset}
                className="w-full py-4 bg-green-500 hover:bg-green-400 text-slate-950 font-black text-xl rounded-xl transition-all active:scale-95 shadow-lg shadow-green-500/20 uppercase tracking-tighter"
              >
                {status === 'BETTING' ? 'BET NOW' : 'NEW GAME'}
              </button>
            ) : (
              <button
                onClick={handleCashOut}
                disabled={clickedTeeth.length === 0}
                className={`w-full py-4 text-slate-950 font-black text-xl rounded-xl transition-all active:scale-95 shadow-lg uppercase tracking-tighter
                  ${clickedTeeth.length > 0 ? 'bg-yellow-400 hover:bg-yellow-300 btn-glow' : 'bg-slate-700 cursor-not-allowed text-slate-400'}`}
              >
                CASH OUT (${(betAmount * currentMultiplier).toFixed(2)})
              </button>
            )}
          </div>
        </div>

        {/* Info Box */}
        <div className="mt-auto bg-slate-800/30 p-4 rounded-xl border border-slate-700/50">
          <div className="flex items-center gap-2 text-slate-400 mb-2">
            <Info size={16} />
            <span className="text-xs font-bold uppercase">Game Stats</span>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div className="bg-slate-950/40 p-2 rounded-lg">
              <div className="text-[10px] text-slate-500 uppercase">Current Multi</div>
              <div className="text-lg font-bold text-green-400">{currentMultiplier.toFixed(2)}x</div>
            </div>
            <div className="bg-slate-950/40 p-2 rounded-lg">
              <div className="text-[10px] text-slate-500 uppercase">Next Multi</div>
              <div className="text-lg font-bold text-yellow-500">{nextMultiplier.toFixed(2)}x</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 relative flex flex-col p-4 md:p-12 overflow-y-auto">
        <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col gap-8">

          {/* Top Multiplier Bar */}
          <div className="flex justify-center gap-4 py-4 px-8 bg-slate-900/40 backdrop-blur rounded-full border border-slate-800/50">
            <div className="flex flex-col items-center">
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Multiplier</span>
              <span className={`text-4xl font-black ${status === 'BITTEN' ? 'text-red-500 line-through' : 'text-green-500'} transition-all`}>
                {currentMultiplier.toFixed(2)}x
              </span>
            </div>
            <div className="w-[1px] bg-slate-800 self-stretch" />
            <div className="flex flex-col items-center">
              <span className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Potential Win</span>
              <span className={`text-4xl font-black ${status === 'BITTEN' ? 'text-slate-600' : 'text-yellow-500'} transition-all`}>
                ${(betAmount * currentMultiplier).toFixed(2)}
              </span>
            </div>
          </div>

          {/* Crocodile View */}
          <div className="flex-1 flex flex-col items-center justify-center min-h-[400px]">
            <Crocodile
              status={status}
              isShaking={isShaking && status === 'PLAYING'}
              clickedTeeth={clickedTeeth}
              trapPositions={trapPositions}
              onToothClick={handleToothClick}
            />
          </div>

          {/* Status Indicator Bar */}
          <div className="bg-slate-900/80 rounded-2xl p-6 border border-slate-800 shadow-2xl flex flex-wrap gap-6 justify-center items-center">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-red-500 shadow-lg shadow-red-500/50" />
              <span className="text-sm font-bold text-slate-300">Traps: <span className="text-red-500">{trapCount}</span></span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-slate-200" />
              <span className="text-sm font-bold text-slate-300">Total: <span className="text-white">20</span></span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="text-green-500" size={18} />
              <span className="text-sm font-bold text-slate-300">Prob. Next Success:
                <span className="text-green-400 ml-1">
                  {status === 'PLAYING'
                    ? `${(((TOTAL_TEETH - trapCount - clickedTeeth.length) / (TOTAL_TEETH - clickedTeeth.length)) * 100).toFixed(1)}%`
                    : '---'}
                </span>
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Sidebar - History */}
      <div className="w-full lg:w-[300px] bg-slate-900 border-l border-slate-800 p-4 z-10 hidden xl:block">
        <HistorySidebar history={history} />
      </div>
    </div>
  );
};

export default App;
