import React, { useRef, useEffect, useState } from 'react';
import { GameStatus } from '../types';
// Note: We are using teeth_layout for RELATIVE POSITIONS.
// But we will use the CANVAS INTERNAL RESOLUTION (e.g. 4096) for best quality.
import { TEETH_LAYOUT } from '../services/teeth_layout';
import { Skull, Check, X } from 'lucide-react';

interface CrocodileProps {
  status: GameStatus;
  isShaking: boolean;
  clickedTeeth: number[];
  trapPositions: number[];
  onToothClick: (id: number) => void;
}

// Canvas Resolution - using a fixed high res to match assets
// TEETH_LAYOUT.base_width is 1024 or 4096 depending on generation.
// We will rely on image.naturalWidth to scale properly if needed.
// But for simplicity, let's fix the internal canvas size to the base image size (4096).
const CANVAS_SIZE = 4096;

const Crocodile: React.FC<CrocodileProps> = ({
  status,
  isShaking,
  clickedTeeth,
  trapPositions,
  onToothClick
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [imagesLoaded, setImagesLoaded] = useState(false);

  // Store loaded images
  const imagesRef = useRef<{ [key: string]: HTMLImageElement }>({});

  // 1. Load Images Once
  useEffect(() => {
    const loadImages = async () => {
      const paths = [
        { key: 'base', src: '/croc_no_tooth01.png' },
        ...TEETH_LAYOUT.teeth.map(t => ({ key: `tooth-${t.id}`, src: `/teeth_refined/${t.image}` }))
      ];

      let loadedCount = 0;
      const total = paths.length;

      paths.forEach(({ key, src }) => {
        const img = new Image();
        img.src = src;
        img.onload = () => {
          imagesRef.current[key] = img;
          loadedCount++;
          if (loadedCount === total) {
            setImagesLoaded(true);
          }
        };
        img.onerror = () => {
          console.error(`Failed to load ${src}`);
        }
      });
    };

    loadImages();
  }, []);

  // 2. Draw Canvas
  useEffect(() => {
    if (!imagesLoaded || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear
    ctx.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

    // A. Draw Base
    const baseImg = imagesRef.current['base'];
    if (baseImg) {
      // Draw base filling the canvas
      ctx.drawImage(baseImg, 0, 0, CANVAS_SIZE, CANVAS_SIZE);
    }

    // B. Draw Teeth
    TEETH_LAYOUT.teeth.forEach((tooth) => {
      const imgKey = `tooth-${tooth.id}`;
      const img = imagesRef.current[imgKey];

      const isClicked = clickedTeeth.includes(tooth.id);

      // If clicked, we might NOT draw it (or draw transparently/darker)
      // Mirroring previous logic: if clicked, we hide it or dim it?
      // Previous DOM: className={`${isClicked ? 'brightness-50' : ''}`}
      // Canvas: we can set globalAlpha or filter.

      if (img) {
        if (isClicked) {
          ctx.filter = 'brightness(50%)';
        } else if (status === 'PLAYING') {
          // Hover effect is hard on canvas without requestAnimationFrame loop for mouse pos.
          // keeping it simple for now. 
          ctx.filter = 'none';
        } else {
          ctx.filter = 'none';
        }

        // Calculate position
        // Layout uses percentages relative to `base_width` which was used during generation.
        // We Map percentages to CANVAS_SIZE (4096).

        const x = (tooth.left_pct / 100) * CANVAS_SIZE;
        const y = (tooth.top_pct / 100) * CANVAS_SIZE;
        const w = (tooth.width_pct / 100) * CANVAS_SIZE;

        // Maintain aspect ratio or use layout height?
        // Aspect ratio of image is safer.
        const aspect = img.naturalWidth > 0 ? img.naturalHeight / img.naturalWidth : 1;
        const h = w * aspect;

        ctx.drawImage(img, x, y, w, h);

        // Reset filter
        ctx.filter = 'none';
      }
    });

  }, [imagesLoaded, clickedTeeth, status]);

  // 3. Handle Clicks
  const handleCanvasClick = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (status !== 'PLAYING' && status !== 'BETTING') return; // Only clickable in active states? Or just PLAYING.

    // Check GAME logic in parent determines if click is valid. Parent checks `status === 'PLAYING'`.
    // We just forward the ID.

    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const scaleX = CANVAS_SIZE / rect.width;
    const scaleY = CANVAS_SIZE / rect.height;

    const clickX = (e.clientX - rect.left) * scaleX;
    const clickY = (e.clientY - rect.top) * scaleY;

    // Iterate teeth (reverse order to hit top-most first if overlap)
    // Actually our teeth shouldn't overlap much, but Z-order matters.
    // array is 0..19. 19 is usually bottom/top?
    // We iterate backwards to find the one drawn "on top" if any.
    // Layout order is drawing order. Last drawn is on top.

    for (let i = TEETH_LAYOUT.teeth.length - 1; i >= 0; i--) {
      const tooth = TEETH_LAYOUT.teeth[i];

      // Bounding Box Check
      // Note: Using Rect collision. For perfect mesh collision we need pixel check, 
      // but Rect is usually fine for these chunky teeth.
      const x = (tooth.left_pct / 100) * CANVAS_SIZE;
      const y = (tooth.top_pct / 100) * CANVAS_SIZE;
      const w = (tooth.width_pct / 100) * CANVAS_SIZE;

      // Approximate height from layout (width_pct usually matched with image aspect).
      // Let's use the image aspect if available.
      const imgKey = `tooth-${tooth.id}`;
      const img = imagesRef.current[imgKey];
      if (!img) continue;

      const h = w * (img.naturalHeight / img.naturalWidth);

      if (clickX >= x && clickX <= x + w && clickY >= y && clickY <= y + h) {
        // Hit!
        onToothClick(tooth.id);
        return; // Stop after first hit
      }
    }
  };

  const isBitten = status === 'BITTEN';
  const isCashedOut = status === 'CASHED_OUT';

  return (
    <div
      ref={containerRef}
      className={`relative w-full max-w-2xl mx-auto transition-all duration-300 ${isShaking ? 'animate-shake' : ''}`}
    >
      {/* 
         Canvas displaying the unified assembly.
         Style w-full h-auto makes it responsive.
      */}
      <canvas
        ref={canvasRef}
        width={CANVAS_SIZE}
        height={CANVAS_SIZE}
        className="w-full h-auto drop-shadow-2xl cursor-pointer"
        onClick={handleCanvasClick}
      />

      {/* 
         Overlays Layer (DOM) 
         We can keep overlays as DOM elements for easy animations (pop-in, ping)
         Coordinate mapping is same: % of container.
      */}
      <div className="absolute inset-0 pointer-events-none">
        {TEETH_LAYOUT.teeth.map((tooth) => {
          const isClicked = clickedTeeth.includes(tooth.id);
          const isTrap = trapPositions.includes(tooth.id);
          const showTrapReveal = (isBitten || isCashedOut) && isTrap;

          if (!isClicked && !showTrapReveal) return null;

          return (
            <div
              key={tooth.id}
              className="absolute flex items-center justify-center transform -translate-x-1/2 -translate-y-1/2" // Centers overlay on the point?
              // Wait, layout x/y is Top-Left of tooth image.
              // We want overlay center to be center of tooth image?
              // Left = left_pct + width_pct/2
              style={{
                left: `${tooth.left_pct + tooth.width_pct / 2}%`,
                top: `${tooth.top_pct + (tooth.width_pct * 1.5) / 2}%`, // Approx height aspect 1.5? Or just eyeball it
                // Better: Top-Left + Offset.
                // Actually, let's just place it at Top_Left and center it with flex.
                // left: tooth.left_pct%, top: tooth.top_pct%, width: tooth.width_pct%
              }}
            >
              {/* 
                    Actually, simpler: define a div covering the tooth rect, center content inside.
                 */}
            </div>
          )
        })}

        {/* Re-implementing simplified Overlays loop */}
        {TEETH_LAYOUT.teeth.map((tooth) => {
          const isClicked = clickedTeeth.includes(tooth.id);
          const isTrap = trapPositions.includes(tooth.id);
          const showTrapReveal = (isBitten || isCashedOut) && isTrap;

          // Only render if needed
          if (!isClicked && !showTrapReveal) return null;

          // Calculate Center of Tooth (Approximate, assuming aspect ratio ~1.5)
          const centerX = tooth.left_pct + (tooth.width_pct / 2);
          const centerY = tooth.top_pct + (tooth.width_pct * 0.75); // Half of 1.5 aspect

          return (
            <div
              key={tooth.id}
              className="absolute w-0 h-0 flex items-center justify-center"
              style={{ left: `${centerX}%`, top: `${centerY}%` }}
            >
              {isClicked && !isTrap && (
                <div className="w-8 h-8 bg-green-500/80 rounded-full flex items-center justify-center shadow-lg shadow-green-500/50 animate-pop-in">
                  <Check size={18} className="text-white" strokeWidth={4} />
                </div>
              )}

              {isClicked && isTrap && (
                <div className="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center shadow-lg shadow-red-600/50 animate-ping-once">
                  <div className="absolute inset-0 bg-red-600 rounded-full animate-ping opacity-75"></div>
                  <X size={24} className="text-white relative z-10" strokeWidth={4} />
                </div>
              )}

              {!isClicked && showTrapReveal && (
                <div className="w-6 h-6 bg-red-950/80 rounded-full flex items-center justify-center animate-fade-in border border-red-500/30">
                  <Skull size={14} className="text-red-500" />
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Result Overlays (Winner/Chomp) */}
      {status === 'CASHED_OUT' && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-20">
          <div className="bg-green-500/90 text-white px-8 py-4 rounded-xl font-bangers text-5xl rotate-[-5deg] shadow-2xl border-4 border-white animate-bounce">
            WINNER!
          </div>
        </div>
      )}
      {status === 'BITTEN' && (
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-20">
          <div className="bg-red-600/90 text-white px-8 py-4 rounded-xl font-bangers text-5xl rotate-[5deg] shadow-2xl border-4 border-white animate-shake">
            CHOMP!
          </div>
        </div>
      )}
    </div>
  );
};

export default Crocodile;
