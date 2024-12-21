import { useEffect, useRef, useState } from 'react';
import { Galaxy } from '../types/galaxy';
import SystemDetailView from './SystemDetailView';
import { COLORS } from '../config/colors';
import { StarryBackground } from './StarryBackground';

interface Props {
  galaxy: Galaxy;
  width: number;
  height: number;
}

interface Node {
  pos: [number, number];
  vel: [number, number];
}

export const GalaxyVisualizer = ({ galaxy, width, height }: Props) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [nodes, setNodes] = useState<Record<number, Node>>({});
  const [selectedSystem, setSelectedSystem] = useState<number | null>(null);
  const headerHeight = 60;

  const calculateLayout = () => {
    const centerX = width / 2;
    const centerY = (height - headerHeight) / 2 + headerHeight;
    const numSystems = Object.keys(galaxy.systems).length;
    const radius = Math.min(width, height - headerHeight) * 0.4;
    const goldenAngle = Math.PI * (3 - Math.sqrt(5));

    const newNodes: Record<number, Node> = {};
    Object.keys(galaxy.systems).forEach((sysId, index) => {
      const id = parseInt(sysId);
      const distance = Math.sqrt(index / numSystems) * radius;
      const theta = index * goldenAngle;

      // Add random variation
      const distanceVar = distance + (Math.random() * 40 - 20);
      const thetaVar = theta + (Math.random() * 0.2 - 0.1);

      newNodes[id] = {
        pos: [
          centerX + distanceVar * Math.cos(thetaVar),
          centerY + distanceVar * Math.sin(thetaVar)
        ],
        vel: [0, 0]
      };
    });

    setNodes(newNodes);
  };

  const drawSystem = (ctx: CanvasRenderingContext2D, systemId: number) => {
    const system = galaxy.systems[systemId];
    const node = nodes[systemId];
    if (!node) return;

    const size = Math.min(8, 3 + (system.total_ep / 40));
    const [x, y] = node.pos;

    // Draw glow
    const gradient = ctx.createRadialGradient(x, y, size, x, y, size * 2);
    gradient.addColorStop(0, 'rgba(255, 255, 255, 0.3)');
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');
    
    ctx.beginPath();
    ctx.arc(x, y, size * 2, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();

    // Draw system
    ctx.beginPath();
    ctx.arc(x, y, size, 0, Math.PI * 2);
    ctx.fillStyle = COLORS[system.stars[0]?.type || 'Starless'];
    ctx.fill();
  };

  const drawConnections = (ctx: CanvasRenderingContext2D) => {
    const connections = new Set<string>();

    Object.entries(galaxy.systems).forEach(([sysId, system]) => {
      const connectedSystems = system.warp_points?.connections || [];
      connectedSystems.forEach((connectedId: number) => {
        const key = [Math.min(parseInt(sysId), connectedId), 
                    Math.max(parseInt(sysId), connectedId)].join('-');
        if (!connections.has(key)) {
          connections.add(key);
          const start = nodes[parseInt(sysId)]?.pos;
          const end = nodes[connectedId]?.pos;
          
          if (start && end) {
            ctx.beginPath();
            ctx.moveTo(start[0], start[1]);
            ctx.lineTo(end[0], end[1]);
            ctx.strokeStyle = '#282832';
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      });
    });
  };

  const handleClick = (event: React.MouseEvent<HTMLCanvasElement>) => {
    const rect = canvasRef.current?.getBoundingClientRect();
    if (!rect) return;

    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // Check if click is on a system
    Object.entries(nodes).forEach(([sysId, node]) => {
      const dx = x - node.pos[0];
      const dy = y - node.pos[1];
      if (Math.sqrt(dx * dx + dy * dy) < 15) {
        setSelectedSystem(parseInt(sysId));
      }
    });
  };

  useEffect(() => {
    calculateLayout();
  }, [galaxy, width, height]);
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
  
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
  
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
  
    // Draw title
    ctx.font = '32px Arial';
    ctx.fillStyle = '#ffffff';
    ctx.fillText('Space Farce Galaxy Map', 20, 40);
  
    // Draw connections and systems
    drawConnections(ctx);
    Object.keys(galaxy.systems).forEach(sysId => {
      drawSystem(ctx, parseInt(sysId));
    });
  }, [galaxy, width, height, nodes, selectedSystem]); // Add selectedSystem to dependencies
  
  // Add escape key handler
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && selectedSystem !== null) {
        setSelectedSystem(null);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedSystem]);

  return (
    <div style={{ 
      width: width, 
      height: height, 
      position: 'relative',
      backgroundColor: '#000'
    }}>
      <StarryBackground width={width} height={height} />
      {selectedSystem !== null ? (
        <SystemDetailView
          key={`system-${selectedSystem}`}
          system={galaxy.systems[selectedSystem]}
          systemId={selectedSystem}
          width={width}
          height={height}
          onClose={() => setSelectedSystem(null)}
        />
      ) : (
        <canvas
          key="galaxy-view"
          ref={canvasRef}
          width={width}
          height={height}
          style={{ 
            position: 'absolute',
            top: 0,
            left: 0,
            border: '1px solid #333' 
          }}
          onClick={handleClick}
        />
      )}
    </div>
  );
}; 