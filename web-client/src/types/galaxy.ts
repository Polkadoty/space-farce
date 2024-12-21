export interface Star {
  type: 'Red' | 'Orange' | 'Yellow' | 'White' | 'Blue' | 'Starless';
}

export interface Planet {
  economic_points: number;
  position: number;
  type: 'H' | 'R' | 'G' | 'I' | 'A';
  moons?: number;
}

export interface System {
  id: number;
  system_type: string;
  stars: Star[];
  planets: Planet[];
  total_ep: number;
  warp_points: {
    count: number;
    connections: number[];
  };
}

export interface Galaxy {
  seed: number;
  systems: Record<number, System>;
} 