import { useEffect, useRef } from 'react';
import { Galaxy } from '../types/galaxy';

interface GameWebSocketProps {
  gameId: string;
  token: string;
  onGalaxyUpdate: (galaxy: Galaxy) => void;
  onError: (error: string) => void;
}

export const useGameWebSocket = ({ gameId, token, onGalaxyUpdate, onError }: GameWebSocketProps) => {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${protocol}//${window.location.host}/api/v1/games/${gameId}/ws`);
    
    ws.onopen = () => {
      ws.send(JSON.stringify({ type: 'auth', token }));
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'galaxy_update') {
          onGalaxyUpdate(data.galaxy);
        }
      } catch (error) {
        onError('Failed to parse server message');
      }
    };

    ws.onerror = () => {
      onError('WebSocket connection error');
    };

    wsRef.current = ws;

    return () => {
      ws.close();
    };
  }, [gameId, token]);

  return wsRef.current;
}; 