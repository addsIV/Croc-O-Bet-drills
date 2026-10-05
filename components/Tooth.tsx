
import React from 'react';

interface ToothProps {
  id: number;
  isClicked: boolean;
  isTrap: boolean;
  isRevealed: boolean;
  status: 'BETTING' | 'PLAYING' | 'BITTEN' | 'CASHED_OUT';
  onClick: (id: number) => void;
}

const Tooth: React.FC<ToothProps> = ({ id, isClicked, isTrap, isRevealed, status, onClick }) => {
  const isDisabled = status !== 'PLAYING' || isClicked;
  
  const getDisplayClass = () => {
    if (isClicked) {
      if (isTrap) return 'bg-red-500 border-red-700 transform translate-y-2 opacity-80';
      return 'bg-yellow-400 border-yellow-600 transform translate-y-2 shadow-inner';
    }
    if (isRevealed && isTrap) return 'bg-red-500/50 border-red-900 animate-pulse';
    return 'bg-slate-50 border-slate-300 hover:bg-slate-200 hover:-translate-y-1';
  };

  return (
    <button
      disabled={isDisabled}
      onClick={() => onClick(id)}
      className={`
        w-full h-12 rounded-b-xl border-b-4 transition-all duration-150 
        ${getDisplayClass()}
        ${isDisabled && !isClicked ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}
      `}
    />
  );
};

export default Tooth;
