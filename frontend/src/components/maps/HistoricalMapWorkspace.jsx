import React, { useEffect, useRef, useState, useCallback } from 'react';
import L from 'leaflet';
import { 
  Sliders, 
  RotateCcw, 
  Eye, 
  EyeOff, 
  Maximize2, 
  ExternalLink, 
  AlertCircle, 
  Info,
  MapPin,
  Sparkles,
  Layers,
  SplitSquareVertical,
  Compass
} from 'lucide-react';
import { useTranslation } from '../../services/LanguageContext';

// Standard OpenStreetMap tile URL and attribution
const OSM_TILE_URL = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const OSM_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> contributors';

// Helper to create custom Leaflet marker icons
const createCustomIcon = (color = '#C5A66A', iconLetter = '🏛️') => {
  return L.divIcon({
    className: 'custom-map-marker',
    html: `
      <div style="
        background: #172B40;
        border: 2px solid ${color};
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.35);
        cursor: pointer;
        transition: transform 0.2s;
      ">
        ${iconLetter}
      </div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -18],
  });
};

export const HistoricalMapWorkspace = ({
  mapData,
  observations = [],
  mode = 'side_by_side', // 'side_by_side' | 'swipe' | 'transparency' | 'inspection'
  focusedObservation = null,
  onObservationClick = null,
}) => {
  const { lang, t } = useTranslation();

  // Opacity state for Mode C (Transparency)
  const [opacity, setOpacity] = useState(0.75);
  const [isLayerVisible, setIsLayerVisible] = useState(true);

  // Swipe slider position (0 to 100 percentage)
  const [swipePosition, setSwipePosition] = useState(50);
  const [isDraggingSwipe, setIsDraggingSwipe] = useState(false);

  // Container DOM Refs
  const sideBySideLeftRef = useRef(null);
  const sideBySideRightRef = useRef(null);
  const swipeContainerRef = useRef(null);
  const swipeLeftRef = useRef(null);
  const swipeRightRef = useRef(null);
  const overlayRef = useRef(null);
  const inspectionRef = useRef(null);

  // Leaflet Map Instances Refs
  const mapsRef = useRef([]);
  const imageOverlaysRef = useRef([]);
  const markersRef = useRef([]);
  const isSyncingRef = useRef(false);

  // Parse bounds from mapData
  const getMapBounds = useCallback(() => {
    if (!mapData?.bounds_json) {
      // Default to roughly 0.08 deg around center
      const lat = mapData?.center_lat || 13.0827;
      const lng = mapData?.center_lng || 80.2707;
      return [
        [lat - 0.04, lng - 0.04],
        [lat + 0.04, lng + 0.04],
      ];
    }
    try {
      const parsed = typeof mapData.bounds_json === 'string' 
        ? JSON.parse(mapData.bounds_json) 
        : mapData.bounds_json;
      if (Array.isArray(parsed) && parsed.length === 2) {
        return parsed;
      }
    } catch (e) {
      console.error('Error parsing bounds_json', e);
    }
    return [
      [(mapData?.center_lat || 13.0827) - 0.04, (mapData?.center_lng || 80.2707) - 0.04],
      [(mapData?.center_lat || 13.0827) + 0.04, (mapData?.center_lng || 80.2707) + 0.04],
    ];
  }, [mapData]);

  // Clean up existing maps
  const cleanupMaps = () => {
    mapsRef.current.forEach((m) => {
      try {
        m.off();
        m.remove();
      } catch (err) {
        // ignore already removed
      }
    });
    mapsRef.current = [];
    imageOverlaysRef.current = [];
    markersRef.current = [];
  };

  // Synchronize two maps on move and zoom
  const syncDualMaps = (mapA, mapB) => {
    const handleMoveA = () => {
      if (isSyncingRef.current) return;
      isSyncingRef.current = true;
      mapB.setView(mapA.getCenter(), mapA.getZoom(), { animate: false });
      isSyncingRef.current = false;
    };

    const handleMoveB = () => {
      if (isSyncingRef.current) return;
      isSyncingRef.current = true;
      mapA.setView(mapB.getCenter(), mapB.getZoom(), { animate: false });
      isSyncingRef.current = false;
    };

    mapA.on('move', handleMoveA);
    mapB.on('move', handleMoveB);
  };

  // Add observation markers to a map instance
  const addObservationMarkers = (leafletMap) => {
    if (!observations || observations.length === 0) return;

    observations.forEach((obs) => {
      if (!obs.coordinates_json) return;
      try {
        const coords = typeof obs.coordinates_json === 'string'
          ? JSON.parse(obs.coordinates_json)
          : obs.coordinates_json;
        if (Array.isArray(coords) && coords.length === 2) {
          const categoryIcon = obs.category === 'waterbodies' ? '🌊' 
            : obs.category === 'road_network' ? '🛣️'
            : obs.category === 'settlement_expansion' ? '🏘️'
            : obs.category === 'historical_landmarks' ? '🏛️'
            : obs.category === 'administrative_boundaries' ? '🏛️'
            : '📍';

          const marker = L.marker([coords[0], coords[1]], {
            icon: createCustomIcon('#C5A66A', categoryIcon),
            title: lang === 'ta' ? (obs.title_tamil || obs.title) : obs.title,
          }).addTo(leafletMap);

          const popupContent = document.createElement('div');
          popupContent.className = 'p-1 font-sans text-[#172B40] max-w-xs';
          popupContent.innerHTML = `
            <div style="font-weight: 700; font-size: 13px; margin-bottom: 4px; color: #172B40;">
              ${lang === 'ta' ? (obs.title_tamil || obs.title) : obs.title}
            </div>
            <div style="font-size: 11px; color: #64748B; margin-bottom: 6px;">
              ${obs.historical_year_ref || ''} • <span style="color: #065F46; font-weight: 600;">${lang === 'ta' ? 'சரிபார்க்கப்பட்டது' : 'Verified Finding'}</span>
            </div>
            <div style="font-size: 12px; line-height: 1.4; color: #334155;">
              ${lang === 'ta' ? (obs.observation_text_tamil || obs.observation_text) : obs.observation_text}
            </div>
          `;

          marker.bindPopup(popupContent);
          markersRef.current.push({ id: obs.id, marker, coords });
        }
      } catch (err) {
        console.error('Failed to parse marker coordinates', err);
      }
    });
  };

  // Initialize Maps based on mode
  useEffect(() => {
    if (!mapData) return;
    cleanupMaps();

    const centerLat = mapData.center_lat || 13.0827;
    const centerLng = mapData.center_lng || 80.2707;
    const defaultZoom = mapData.default_zoom || 13;
    const bounds = getMapBounds();
    const isUnreferenced = mapData.georeferencing_status === 'unreferenced';

    if (mode === 'side_by_side' && sideBySideLeftRef.current && sideBySideRightRef.current) {
      // MODE A: Side by Side
      // Left: Historical Map
      const mapLeft = L.map(sideBySideLeftRef.current, {
        center: [centerLat, centerLng],
        zoom: defaultZoom,
        zoomControl: true,
      });

      // Muted background layer for historical view
      L.tileLayer(OSM_TILE_URL, {
        attribution: OSM_ATTRIBUTION,
        maxZoom: 19,
        className: 'opacity-40 grayscale',
      }).addTo(mapLeft);

      if (!isUnreferenced && mapData.image_url) {
        const overlay = L.imageOverlay(mapData.image_url, bounds, {
          opacity: 0.95,
          interactive: true,
        }).addTo(mapLeft);
        imageOverlaysRef.current.push(overlay);
      }

      // Right: Modern Map
      const mapRight = L.map(sideBySideRightRef.current, {
        center: [centerLat, centerLng],
        zoom: defaultZoom,
        zoomControl: true,
      });

      L.tileLayer(OSM_TILE_URL, {
        attribution: OSM_ATTRIBUTION,
        maxZoom: 19,
      }).addTo(mapRight);

      // Add observation markers to both maps
      addObservationMarkers(mapLeft);
      addObservationMarkers(mapRight);

      // Synchronize both maps
      syncDualMaps(mapLeft, mapRight);

      mapsRef.current = [mapLeft, mapRight];
      setTimeout(() => {
        mapLeft.invalidateSize();
        mapRight.invalidateSize();
      }, 200);

    } else if (mode === 'swipe' && swipeLeftRef.current && swipeRightRef.current) {
      // MODE B: Swipe Comparison
      // Dual synchronized map panes inside one viewport container
      const mapLeft = L.map(swipeLeftRef.current, {
        center: [centerLat, centerLng],
        zoom: defaultZoom,
        zoomControl: true,
      });

      L.tileLayer(OSM_TILE_URL, {
        attribution: OSM_ATTRIBUTION,
        maxZoom: 19,
        className: 'opacity-40 grayscale',
      }).addTo(mapLeft);

      if (!isUnreferenced && mapData.image_url) {
        const overlay = L.imageOverlay(mapData.image_url, bounds, {
          opacity: 1.0,
          interactive: true,
        }).addTo(mapLeft);
        imageOverlaysRef.current.push(overlay);
      }

      const mapRight = L.map(swipeRightRef.current, {
        center: [centerLat, centerLng],
        zoom: defaultZoom,
        zoomControl: false,
      });

      L.tileLayer(OSM_TILE_URL, {
        attribution: OSM_ATTRIBUTION,
        maxZoom: 19,
      }).addTo(mapRight);

      addObservationMarkers(mapLeft);
      addObservationMarkers(mapRight);

      syncDualMaps(mapLeft, mapRight);

      mapsRef.current = [mapLeft, mapRight];
      setTimeout(() => {
        mapLeft.invalidateSize();
        mapRight.invalidateSize();
      }, 200);

    } else if (mode === 'transparency' && overlayRef.current) {
      // MODE C: Transparency Overlay
      const map = L.map(overlayRef.current, {
        center: [centerLat, centerLng],
        zoom: defaultZoom,
        zoomControl: true,
      });

      L.tileLayer(OSM_TILE_URL, {
        attribution: OSM_ATTRIBUTION,
        maxZoom: 19,
      }).addTo(map);

      if (!isUnreferenced && mapData.image_url) {
        const overlay = L.imageOverlay(mapData.image_url, bounds, {
          opacity: opacity,
          interactive: true,
        }).addTo(map);
        imageOverlaysRef.current.push(overlay);
      }

      addObservationMarkers(map);

      mapsRef.current = [map];
      setTimeout(() => {
        map.invalidateSize();
      }, 200);

    } else if (mode === 'inspection' && inspectionRef.current) {
      // MODE D: Archival Inspection
      const map = L.map(inspectionRef.current, {
        crs: L.CRS.Simple,
        minZoom: -2,
        maxZoom: 3,
        zoomControl: true,
      });

      const w = 2400;
      const h = 1800;
      const southWest = map.unproject([0, h], map.getMaxZoom() - 1);
      const northEast = map.unproject([w, 0], map.getMaxZoom() - 1);
      const imageBounds = new L.LatLngBounds(southWest, northEast);

      if (mapData.image_url) {
        L.imageOverlay(mapData.image_url, imageBounds).addTo(map);
        map.fitBounds(imageBounds);
      }

      mapsRef.current = [map];
      setTimeout(() => {
        map.invalidateSize();
      }, 200);
    }

    return () => {
      cleanupMaps();
    };
  }, [mapData, mode, getMapBounds]);

  // Update Opacity in Mode C
  useEffect(() => {
    if (mode === 'transparency') {
      imageOverlaysRef.current.forEach((overlay) => {
        if (overlay && overlay.setOpacity) {
          overlay.setOpacity(isLayerVisible ? opacity : 0);
        }
      });
    }
  }, [opacity, isLayerVisible, mode]);

  // Focus on observation if selected
  useEffect(() => {
    if (!focusedObservation || !focusedObservation.coordinates_json) return;
    try {
      const coords = typeof focusedObservation.coordinates_json === 'string'
        ? JSON.parse(focusedObservation.coordinates_json)
        : focusedObservation.coordinates_json;
      if (Array.isArray(coords) && coords.length === 2) {
        mapsRef.current.forEach((m) => {
          m.flyTo([coords[0], coords[1]], 15, { duration: 1.2 });
        });

        // Trigger popup
        const matched = markersRef.current.find((item) => item.id === focusedObservation.id);
        if (matched && matched.marker) {
          matched.marker.openPopup();
        }
      }
    } catch (e) {
      console.error('Failed to focus on observation', e);
    }
  }, [focusedObservation]);

  // Reset View handler
  const handleResetView = () => {
    if (!mapData) return;
    const centerLat = mapData.center_lat || 13.0827;
    const centerLng = mapData.center_lng || 80.2707;
    const defaultZoom = mapData.default_zoom || 13;

    mapsRef.current.forEach((m) => {
      if (mode === 'inspection') {
        const bounds = getMapBounds();
        m.fitBounds(bounds);
      } else {
        m.setView([centerLat, centerLng], defaultZoom, { animate: true });
      }
    });
  };

  // Draggable Swipe Handler
  const handleSwipeMove = (e) => {
    if (!isDraggingSwipe || !swipeContainerRef.current) return;
    const rect = swipeContainerRef.current.getBoundingClientRect();
    const clientX = e.clientX || (e.touches && e.touches[0]?.clientX);
    if (!clientX) return;

    const offset = clientX - rect.left;
    const percentage = Math.max(5, Math.min(95, (offset / rect.width) * 100));
    setSwipePosition(percentage);
  };

  const handleSwipeStart = () => setIsDraggingSwipe(true);
  const handleSwipeEnd = () => setIsDraggingSwipe(false);

  const isUnreferenced = mapData?.georeferencing_status === 'unreferenced';

  return (
    <div className="w-full bg-[#172B40] rounded-2xl shadow-xl border border-[#2C3F55] overflow-hidden flex flex-col">
      {/* Top Workspace Bar */}
      <div className="bg-[#122334] px-4 py-3 border-b border-[#2C3F55] flex flex-wrap items-center justify-between gap-3 text-white">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-[#C5A66A]/20 text-[#C5A66A] rounded-lg border border-[#C5A66A]/40">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm sm:text-base text-white">
                {lang === 'ta' ? (mapData.title_tamil || mapData.title) : mapData.title}
              </span>
              <span className="text-[11px] font-bold px-2 py-0.5 rounded-full bg-[#C5A66A]/20 text-[#C5A66A] border border-[#C5A66A]/40">
                {mapData.year_start ? `${mapData.year_start}–${mapData.year_end || ''}` : mapData.historical_period}
              </span>
            </div>
            <p className="text-xs text-gray-400">
              {lang === 'ta' ? (mapData.place_name_tamil || mapData.place_name) : mapData.place_name} • {mapData.district}
              {mapData.scale && ` • ${t('maps.scale', 'Scale')}: ${mapData.scale}`}
            </p>
          </div>
        </div>

        {/* Mode Specific Controls */}
        <div className="flex items-center gap-2 ml-auto">
          {mode === 'transparency' && (
            <div className="flex items-center gap-3 bg-[#1A3149] px-3 py-1.5 rounded-xl border border-[#2C3F55]">
              <span className="text-xs text-gray-300 font-medium hidden sm:inline">
                {t('maps.opacity', 'Opacity')}: <b className="text-[#C5A66A]">{Math.round(opacity * 100)}%</b>
              </span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={opacity}
                onChange={(e) => setOpacity(parseFloat(e.target.value))}
                className="w-24 sm:w-32 accent-[#C5A66A] cursor-pointer"
                title={t('maps.opacity', 'Opacity')}
              />
              <button
                onClick={() => setIsLayerVisible(!isLayerVisible)}
                className={`p-1.5 rounded-lg border text-xs transition-colors ${
                  isLayerVisible 
                    ? 'bg-[#C5A66A] text-[#172B40] border-[#C5A66A]' 
                    : 'bg-[#122334] text-gray-400 border-[#2C3F55] hover:text-white'
                }`}
                title={isLayerVisible ? t('maps.hideLayer', 'Hide Layer') : t('maps.showLayer', 'Show Layer')}
              >
                {isLayerVisible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
              </button>
            </div>
          )}

          {mode === 'swipe' && (
            <div className="hidden sm:flex items-center gap-2 bg-[#1A3149] px-3 py-1.5 rounded-xl border border-[#2C3F55] text-xs text-gray-300">
              <span>{t('maps.splitPosition', 'Split Position')}:</span>
              <span className="font-bold text-[#C5A66A]">{Math.round(swipePosition)}%</span>
            </div>
          )}

          <button
            onClick={handleResetView}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium bg-[#1A3149] text-gray-200 hover:text-white hover:bg-[#203D5B] border border-[#2C3F55] transition-colors"
            title={t('maps.resetView', 'Reset View')}
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">{t('maps.resetView', 'Reset View')}</span>
          </button>
        </div>
      </div>

      {/* Unreferenced Archival Warning Banner if applicable */}
      {isUnreferenced && mode !== 'inspection' && (
        <div className="bg-[#B45309]/20 border-b border-[#B45309]/40 px-4 py-2.5 flex items-center justify-between text-amber-200 text-xs">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0" />
            <span>{t('maps.unreferencedNotice', 'This historical map is preserved for archival visual inspection and is not georeferenced to avoid inaccurate geographical distortion.')}</span>
          </div>
        </div>
      )}

      {/* Map Comparison Workspace Viewport */}
      <div className="relative w-full h-[520px] sm:h-[600px] lg:h-[650px] bg-[#0F1C2A] overflow-hidden select-none">
        
        {/* MODE A: Side-by-Side Comparison */}
        {mode === 'side_by_side' && (
          <div className="grid grid-cols-1 md:grid-cols-2 w-full h-full divide-y md:divide-y-0 md:divide-x divide-[#C5A66A]/40">
            {/* Left Column: Historical Map */}
            <div className="relative w-full h-full overflow-hidden">
              <div className="absolute top-3 left-3 z-[1000] bg-[#172B40]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-[#C5A66A]/50 text-white shadow-lg flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-[#C5A66A] animate-pulse"></span>
                <span className="text-xs font-bold text-[#E8D8B0]">
                  {t('maps.historicalMap', 'Historical Cartography')} ({mapData.year_start || mapData.historical_period})
                </span>
              </div>
              <div ref={sideBySideLeftRef} className="w-full h-full" />
            </div>

            {/* Right Column: Modern Map */}
            <div className="relative w-full h-full overflow-hidden">
              <div className="absolute top-3 left-3 z-[1000] bg-[#172B40]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-emerald-500/50 text-white shadow-lg flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                <span className="text-xs font-bold text-emerald-200">
                  {t('maps.modernMap', 'Modern OpenStreetMap')} ({new Date().getFullYear()})
                </span>
              </div>
              <div ref={sideBySideRightRef} className="w-full h-full" />
            </div>
          </div>
        )}

        {/* MODE B: Swipe Comparison */}
        {mode === 'swipe' && (
          <div 
            ref={swipeContainerRef}
            className="relative w-full h-full overflow-hidden cursor-ew-resize"
            onMouseMove={handleSwipeMove}
            onTouchMove={handleSwipeMove}
            onMouseUp={handleSwipeEnd}
            onTouchEnd={handleSwipeEnd}
          >
            {/* Base Layer: Modern Map (Right Side) */}
            <div className="absolute inset-0 w-full h-full">
              <div ref={swipeRightRef} className="w-full h-full" />
              <div className="absolute top-3 right-3 z-[990] bg-[#172B40]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-emerald-500/50 text-white shadow-lg pointer-events-none text-xs font-bold text-emerald-200">
                {t('maps.modernMap', 'Modern Map')}
              </div>
            </div>

            {/* Overlaid Clipped Layer: Historical Map (Left Side) */}
            <div 
              className="absolute inset-0 w-full h-full pointer-events-auto"
              style={{
                clipPath: `inset(0 ${100 - swipePosition}% 0 0)`,
              }}
            >
              <div ref={swipeLeftRef} className="w-full h-full" />
              <div className="absolute top-3 left-3 z-[990] bg-[#172B40]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-[#C5A66A]/50 text-white shadow-lg pointer-events-none text-xs font-bold text-[#E8D8B0]">
                {t('maps.historicalMap', 'Historical')} ({mapData.year_start})
              </div>
            </div>

            {/* Interactive Vertical Divider Slider Handle */}
            <div 
              className="absolute top-0 bottom-0 z-[1000] w-1 bg-[#C5A66A] shadow-[0_0_12px_rgba(197,166,106,0.8)] pointer-events-auto cursor-ew-resize"
              style={{ left: `${swipePosition}%` }}
              onMouseDown={handleSwipeStart}
              onTouchStart={handleSwipeStart}
            >
              <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-[#172B40] border-2 border-[#C5A66A] shadow-xl flex items-center justify-center text-[#C5A66A] text-xs font-bold">
                ⮜⮞
              </div>
            </div>
          </div>
        )}

        {/* MODE C: Transparency Overlay */}
        {mode === 'transparency' && (
          <div className="relative w-full h-full">
            <div className="absolute top-3 left-3 z-[1000] bg-[#172B40]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-[#C5A66A]/50 text-white shadow-lg flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#C5A66A]" />
              <span className="text-xs font-bold text-[#E8D8B0]">
                {t('maps.transparency', 'Transparency Overlay')} • {Math.round(opacity * 100)}%
              </span>
            </div>
            <div ref={overlayRef} className="w-full h-full" />
          </div>
        )}

        {/* MODE D: Archival Visual Inspection */}
        {mode === 'inspection' && (
          <div className="relative w-full h-full">
            <div className="absolute top-3 left-3 z-[1000] bg-[#172B40]/90 backdrop-blur-md px-3 py-1.5 rounded-xl border border-amber-500/50 text-white shadow-lg flex items-center gap-2">
              <Info className="w-4 h-4 text-amber-400" />
              <span className="text-xs font-bold text-amber-200">
                {t('maps.inspection', 'High-Resolution Archival Inspection')}
              </span>
            </div>
            <div ref={inspectionRef} className="w-full h-full bg-[#1E293B]" />
          </div>
        )}
      </div>

      {/* Map Workspace Footer Legend */}
      <div className="bg-[#122334] px-4 py-2 border-t border-[#2C3F55] flex flex-wrap items-center justify-between text-[11px] text-gray-400 gap-2">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-[#C5A66A]"></span>
            {t('maps.historicalRef', 'Historical Cartography')}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
            {t('maps.modernRef', 'Modern Geography')}
          </span>
          <span className="flex items-center gap-1.5">
            <span className="text-base">🏛️</span>
            {t('maps.verifiedFinding', 'Verified Archival Findings')}
          </span>
        </div>
        <div className="text-gray-400">
          {mapData.georeferencing_status === 'georeferenced' 
            ? `✓ ${t('maps.georeferencedNotice', 'Georeferenced with precision coordinates and calibrated bounding boxes.')}`
            : `ℹ️ ${t('maps.unreferencedNotice', 'Archival visual inspection mode.')}`
          }
        </div>
      </div>
    </div>
  );
};

export default HistoricalMapWorkspace;
