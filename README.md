# Croc-O-Bet 🐊

A high-stakes "Crocodile Dentist" style betting game inspired by Minesweeper. Test your luck and nerve by pressing the crocodile's teeth — but beware of the sore ones!

## 🎮 Game Overview

Croc-O-Bet combines the tension of Mines with the classic Crocodile Dentist toy. 
- **The Goal**: Press as many healthy teeth as possible to increase your winning multiplier.
- **The Risk**: If you press a "sore tooth" (trap), the crocodile bites, and you lose your bet.
- **Cash Out**: You can cash out at any time to secure your winnings.

## ✨ Features

- **4K High-Resolution Assets**: All crocodile and teeth images are rendered at a crisp 4096x4096px resolution.
- **Canvas-Based Assembly**: A high-performance canvas rendering system ensures pixel-perfect alignment and smooth scaling across all devices.
- **Dynamic Multipliers**: The more teeth you successfully press, the higher your payout multiplier.
- **Adjustable Risk**: Choose your difficulty by setting the number of "sore teeth" (traps) from 1 to 19.
- **Visual Feedback**: Sleek dark-mode UI with smooth animations and sound effects.
- **Improved Aliasing**: Uses high-resolution, anti-aliased tooth assets for a premium look.
- **Developer Tools**: Includes a custom **Visual Assembler** for real-time teeth layout refinement.

## 🛠️ Tech Stack

- **Framework**: [React](https://react.dev/)
- **Build Tool**: [Vite](https://vitejs.dev/)
- **Rendering**: HTML5 Canvas (for 4K asset assembly)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Language**: TypeScript

## 🚀 Getting Started

### Prerequisites
- Node.js installed on your machine.

### Installation

1. Clone the repository (if applicable) or navigate to the project directory.
2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Game

Start the development server:
```bash
npm run dev
```

Open your browser and navigate to the URL shown in the terminal (usually `http://localhost:5173`).

## 🎲 How to Play

1. **Set Your Bet**: Enter your wager amount in the "Bet Amount" field.
2. **Choose Difficulty**: Use the slider to set the number of "Sore Teeth" (Traps). More traps mean higher multipliers but higher risk!
3. **Start Game**: Click **BET NOW**.
4. **Play**: Click on the crocodile's teeth.
   - **Safe Tooth**: Your multiplier increases. You can click another tooth or Cash Out.
   - **Sore Tooth**: The crocodile bites! You lose the current bet.
5. **Cash Out**: Click **CASH OUT** at any time to take your winnings.

## 📁 Project Structure

- `App.tsx`: Main game logic, state management, and assembler toggle.
- `components/`: 
  - `Crocodile.tsx`: High-resolution Canvas assembly and hit-testing.
  - `CrocodileAssembler.tsx`: Visual tool for tuning teeth layout.
  - `HistorySidebar.tsx`: Game session log.
- `services/`: 
  - `teeth_layout.ts`: Finalized 4K coordinate data.
  - `math.ts`: Multiplier and trap generation logic.
- `scripts/`: 
  - `refine_teeth.py`: Script for anti-aliasing tooth assets.
  - Collection of Python utilities for asset processing and layout verification.

## 📜 Version History

### [v1.1.1] - 2025-12-23
- **Anti-Aliasing**: Implemented a soft-alpha mask refinement for all tooth assets.
- **Refined Assets**: Generated a new set of smoother tooth images in `public/teeth_refined`.

### [v1.1.0] - 2025-12-22
- **Unified 4K Assets**: Upgraded all game assets to 4096x4096px.
- **Canvas Engine**: Implemented a new rendering engine using `<canvas>` for superior scaling and alignment.
- **Assembler Tool**: Added a developer-facing tool to visually adjust teeth positions, sizes, and opacity.
- **Layout Refinement**: Fully calibrated all 20 teeth coordinates based on high-resolution reference templates.

### [v1.0.0] - Initial Release
- Core gameplay loop with adjustable traps.
- Multiplier logic and betting controls.
- Basic SVG/DOM-based crocodile representation.

---
*Enjoy the thrill of the snap!* 🦷
