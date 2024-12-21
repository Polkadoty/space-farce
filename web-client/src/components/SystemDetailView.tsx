import { useEffect, useRef, useMemo } from 'react';
import { System } from '../types/galaxy';
import { COLORS, PLANET_COLORS } from '../config/colors';

interface Props {
  system: System;
  systemId: number;
  width: number;
  height: number;
  onClose: () => void;
}

const generateNoiseTexture = (ctx: CanvasRenderingContext2D, width: number, height: number) => {
  const imageData = ctx.createImageData(width, height);
  for (let i = 0; i < imageData.data.length; i += 4) {
    const value = Math.random() * 255;
    imageData.data[i] = value;
    imageData.data[i + 1] = value;
    imageData.data[i + 2] = value;
    imageData.data[i + 3] = 255;
  }
  return imageData;
};

export const SystemDetailView = ({ system, systemId, width, height, onClose }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const headerHeight = 60;
  const planetSize = 30; // Smaller planets

  const noiseTextures = useMemo(() => {
    const tempCanvas = document.createElement('canvas');
    const ctx = tempCanvas.getContext('2d');
    if (!ctx) return [];
    
    return [
      generateNoiseTexture(ctx, 128, 128),
      generateNoiseTexture(ctx, 128, 128),
      generateNoiseTexture(ctx, 128, 128)
    ];
  }, []);

  const drawStarGlow = (ctx: CanvasRenderingContext2D, x: number, y: number, size: number, color: string) => {
    // Inner glow
    const innerGlow = ctx.createRadialGradient(x, y, size * 0.5, x, y, size);
    innerGlow.addColorStop(0, color);
    innerGlow.addColorStop(1, 'rgba(255, 255, 255, 0)');
    
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fillStyle = innerGlow;
    ctx.fill();

    // Outer glow
    const outerGlow = ctx.createRadialGradient(x, y, size, x, y, size * 2);
    outerGlow.addColorStop(0, 'rgba(255, 255, 255, 0.2)');
    outerGlow.addColorStop(1, 'rgba(255, 255, 255, 0)');
    
    ctx.beginPath();
    ctx.arc(x, y, size * 2, 0, Math.PI * 2);
    ctx.fillStyle = outerGlow;
    ctx.fill();
  };

  const drawPlanet = (ctx: CanvasRenderingContext2D, x: number, y: number, type: string) => {
    // Base planet
    ctx.beginPath();
    ctx.arc(x, y, planetSize, 0, Math.PI * 2);
    ctx.fillStyle = PLANET_COLORS[type as keyof typeof PLANET_COLORS];
    ctx.fill();
  
    // Apply noise textures
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = planetSize * 2;
    tempCanvas.height = planetSize * 2;
    const tempCtx = tempCanvas.getContext('2d');
    if (!tempCtx || noiseTextures.length === 0) return;
  
    noiseTextures.forEach((noise, i) => {
      tempCtx.globalAlpha = 0.1 + (i * 0.05);
      tempCtx.putImageData(noise, 0, 0);
    });
  
    ctx.globalCompositeOperation = 'overlay';
    ctx.drawImage(tempCanvas, x - planetSize, y - planetSize, planetSize * 2, planetSize * 2);
    ctx.globalCompositeOperation = 'source-over';
  };

  useEffect(() => {
    console.log('System:', system);
    const canvas = canvasRef.current;
    if (!canvas) {
      console.error('No canvas ref');
      return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
      console.error('No canvas context');
      return;
    }

    // Clear canvas
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, width, height);

    // Draw header
    ctx.fillStyle = '#14141e';
    ctx.fillRect(0, 0, width, headerHeight);
    ctx.strokeStyle = '#282832';
    ctx.beginPath();
    ctx.moveTo(0, headerHeight);
    ctx.lineTo(width, headerHeight);
    ctx.stroke();

    // Draw title and controls
    ctx.font = '32px Arial';
    ctx.fillStyle = '#ffffff';
    ctx.fillText(`System ${String(systemId).padStart(3, '0')} - ${system.system_type}`, 20, 40);
    ctx.font = '16px Arial';
    ctx.fillText('Click anywhere or press ESC to return to galaxy view', 20, headerHeight - 10);

    // Draw star(s)
    const starX = width * 0.2;
    const centerY = (height - headerHeight) / 2 + headerHeight;
    const starSize = 80;

    if (system.system_type === "Starless Nexus") {
      drawStarGlow(ctx, starX, centerY, starSize, COLORS.Starless);
    } else {
      // Draw star(s)
      system.stars.forEach((star, index) => {
        const yOffset = system.stars.length > 1 ? (index === 0 ? -50 : 50) : 0;
        drawStarGlow(ctx, starX, centerY + yOffset, starSize, COLORS[star.type]);
      });
    }

    // Draw planets
    if (system.system_type !== 'Starless Nexus') {
      const planetStartX = width * 0.35;
      const planetSpacing = (width * 0.6) / Math.max(system.planets.length, 1);

      system.planets.forEach((planet, i) => {
        const xPos = planetStartX + (i * planetSpacing);
        
        // Draw orbit lines
        ctx.beginPath();
        ctx.strokeStyle = '#282832';
        ctx.lineWidth = 2;
        ctx.moveTo(starX + starSize, centerY);
        ctx.lineTo(xPos - planetSize, centerY);
        ctx.stroke();
        
        // Draw connecting lines between planets
        if (i < system.planets.length - 1) {
          ctx.beginPath();
          ctx.moveTo(xPos + planetSize, centerY);
          ctx.lineTo(xPos + planetSpacing - planetSize, centerY);
          ctx.stroke();
        }

        // Draw planet
        drawPlanet(ctx, xPos, centerY, planet.type);

        // Draw EP
        ctx.font = '24px Arial';
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'center';
        ctx.fillText(planet.economic_points.toString(), xPos, centerY + 8);

        // Draw moons if any
        if (planet.moons && planet.moons > 0) {
          ctx.font = '16px Arial';
          ctx.fillText(`Moons: ${planet.moons}`, xPos, centerY + 50);
        }
      });
    }
  }, [system, systemId, width, height]);

  return (
    <canvas
      ref={canvasRef}
      width={width}
      height={height}
      style={{ border: '1px solid #333', cursor: 'pointer' }}
      onClick={onClose}
    />
  );
};

export default SystemDetailView;