import { useState, useCallback, useMemo } from 'react';
import { GameStatus, HistoryItem } from '../../types';
import { TOTAL_TEETH, INITIAL_BALANCE } from '../../constants';
import { calculateMultiplier, generateTraps } from '../../services/math';
import { audioService } from '../../services/audio';

export const useCrocGame = () => {
    const [balance, setBalance] = useState(INITIAL_BALANCE);
    const [betAmount, setBetAmount] = useState(10.00);
    const [trapCount, setTrapCount] = useState(3);
    const [status, setStatus] = useState<GameStatus>('BETTING');
    const [clickedTeeth, setClickedTeeth] = useState<number[]>([]);
    const [trapPositions, setTrapPositions] = useState<number[]>([]);
    const [history, setHistory] = useState<HistoryItem[]>([]);

    const currentMultiplier = useMemo(() => {
        return calculateMultiplier(trapCount, clickedTeeth.length);
    }, [trapCount, clickedTeeth.length]);

    const nextMultiplier = useMemo(() => {
        return calculateMultiplier(trapCount, clickedTeeth.length + 1);
    }, [trapCount, clickedTeeth.length]);

    const isShaking = clickedTeeth.length > 5 || (clickedTeeth.length / (TOTAL_TEETH - trapCount)) > 0.5;

    const handleStartGame = useCallback(() => {
        if (balance < betAmount) return;
        setBalance(prev => prev - betAmount);
        setClickedTeeth([]);
        setTrapPositions(generateTraps(trapCount));
        setStatus('PLAYING');
        audioService.playClick();
    }, [balance, betAmount, trapCount]);

    const handleToothClick = useCallback((id: number) => {
        if (status !== 'PLAYING' || clickedTeeth.includes(id)) return;

        if (trapPositions.includes(id)) {
            setClickedTeeth(prev => [...prev, id]);
            setStatus('BITTEN');
            audioService.playBite();

            const newHistory: HistoryItem = {
                id: Math.random().toString(36).substr(2, 9),
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                bet: betAmount,
                multiplier: 0,
                win: 0,
                status: 'LOSS'
            };
            setHistory(prev => [newHistory, ...prev].slice(0, 20));
        } else {
            const nextCount = clickedTeeth.length + 1;
            setClickedTeeth(prev => [...prev, id]);
            audioService.playSuccess(nextCount);
        }
    }, [status, clickedTeeth, trapPositions, betAmount]);

    const handleCashOut = useCallback(() => {
        if (status !== 'PLAYING' || clickedTeeth.length === 0) return;

        const winAmount = betAmount * currentMultiplier;
        setBalance(prev => prev + winAmount);
        setStatus('CASHED_OUT');
        audioService.playSuccess(10); // Celebration sound

        const newHistory: HistoryItem = {
            id: Math.random().toString(36).substr(2, 9),
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
            bet: betAmount,
            multiplier: currentMultiplier,
            win: winAmount,
            status: 'WIN'
        };
        setHistory(prev => [newHistory, ...prev].slice(0, 20));
    }, [status, clickedTeeth, betAmount, currentMultiplier]);

    const handleReset = useCallback(() => {
        setStatus('BETTING');
        setClickedTeeth([]);
        setTrapPositions([]);
    }, []);

    return {
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
        handleReset,
    };
};
