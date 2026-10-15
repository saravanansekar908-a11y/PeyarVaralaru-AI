import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  ReactFlow, 
  Controls, 
  Background, 
  useNodesState, 
  useEdgesState,
  MarkerType 
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import { useTranslation } from '../services/LanguageContext';
import { getGraphData, getPlaces } from '../services/api';
import StatusBadge from '../components/StatusBadge';
import { 
  Network, 
  Info, 
  X, 
  ExternalLink, 
  Landmark, 
  Clock, 
  BookOpen, 
  Tag, 
  Layers 
} from 'lucide-react';

export const RelationshipGraph = () => {
  const { lang, t } = useTranslation();
  const [searchParams, setSearchParams] = useSearchParams();
  const placeIdParam = searchParams.get('place') || '1';

  const [selectedPlaceId, setSelectedPlaceId] = useState(placeIdParam);
  const [placesList, setPlacesList] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    const fetchPlaces = async () => {
      try {
        const list = await getPlaces();
        setPlacesList(list);
      } catch (err) {
        console.error('Failed to load places list:', err);
      }
    };
    fetchPlaces();
  }, []);

  const layoutGraph = (rawNodes, rawEdges) => {
    const placeNode = rawNodes.find((n) => n.type === 'place');
    const histNodes = rawNodes.filter((n) => n.type === 'historical_name');
    const eventNodes = rawNodes.filter((n) => n.type === 'event');
    const sourceNodes = rawNodes.filter((n) => n.type === 'source');

    const formattedNodes = [];

    // Place node at center
    if (placeNode) {
      formattedNodes.push({
        id: placeNode.id,
        type: 'default',
        position: { x: 380, y: 180 },
        data: {
          label: (
            <div className="p-2 text-center">
              <div className="font-bold text-sm text-[#172B40] flex items-center justify-center gap-1">
                <Landmark className="w-4 h-4 text-[#C5A66A]" />
                <span>{placeNode.label}</span>
              </div>
              {placeNode.data?.current_name_tamil && (
                <div className="text-xs text-gray-500 font-medium">
                  {placeNode.data.current_name_tamil}
                </div>
              )}
              <span className="text-[10px] uppercase font-bold text-[#C5A66A] tracking-wider block mt-0.5">
                {lang === 'ta' ? 'தற்போதைய இடம்' : 'Current Place'}
              </span>
            </div>
          ),
          raw: placeNode,
        },
        style: {
          background: '#FFFFFF',
          border: '2px solid #172B40',
          borderRadius: '12px',
          boxShadow: '0 4px 12px rgba(23,43,64,0.15)',
          width: 170,
        },
      });
    }

    // Historical names on the left arc
    histNodes.forEach((hn, index) => {
      const yOffset = 60 + index * 90;
      formattedNodes.push({
        id: hn.id,
        type: 'default',
        position: { x: 60, y: yOffset },
        data: {
          label: (
            <div className="p-1.5 text-center">
              <div className="font-bold text-xs text-[#92400E] flex items-center justify-center gap-1">
                <Tag className="w-3 h-3 text-[#C5A66A]" />
                <span>{hn.label}</span>
              </div>
              <span className="text-[10px] text-gray-500 block">
                {hn.data?.name_type || 'Variant'}
              </span>
            </div>
          ),
          raw: hn,
        },
        style: {
          background: '#FFFBEB',
          border: '1.5px solid #FDE68A',
          borderRadius: '8px',
          width: 140,
        },
      });
    });

    // Event nodes in the center-right
    eventNodes.forEach((evt, index) => {
      const yOffset = 80 + index * 120;
      formattedNodes.push({
        id: evt.id,
        type: 'default',
        position: { x: 650, y: yOffset },
        data: {
          label: (
            <div className="p-1.5 text-center">
              <div className="font-bold text-xs text-emerald-900 flex items-center justify-center gap-1">
                <Clock className="w-3 h-3 text-emerald-600" />
                <span>{evt.label}</span>
              </div>
              <span className="text-[10px] text-emerald-700 block mt-0.5 font-medium">
                {evt.data?.event_type || 'Event'}
              </span>
            </div>
          ),
          raw: evt,
        },
        style: {
          background: '#ECFDF5',
          border: '1.5px solid #A7F3D0',
          borderRadius: '8px',
          width: 150,
        },
      });
    });

    // Source nodes to the far right
    sourceNodes.forEach((src, index) => {
      const yOffset = 80 + index * 130;
      formattedNodes.push({
        id: src.id,
        type: 'default',
        position: { x: 920, y: yOffset },
        data: {
          label: (
            <div className="p-1.5 text-center">
              <div className="font-bold text-xs text-blue-900 flex items-center justify-center gap-1 line-clamp-1">
                <BookOpen className="w-3 h-3 text-blue-600 shrink-0" />
                <span>{src.label}</span>
              </div>
              {src.data?.document_identifier && (
                <span className="text-[9px] font-mono text-gray-500 block">
                  {src.data.document_identifier}
                </span>
              )}
            </div>
          ),
          raw: src,
        },
        style: {
          background: '#EFF6FF',
          border: '1.5px solid #BFDBFE',
          borderRadius: '8px',
          width: 160,
        },
      });
    });

    // Format edges with labels and smooth step markers
    const formattedEdges = rawEdges.map((e) => ({
      id: e.id,
      source: e.source,
      target: e.target,
      label: e.label,
      animated: e.label === 'CHANGED_ON',
      style: {
        stroke: e.label === 'CHANGED_ON' ? '#059669' : e.label === 'SUPPORTED_BY' ? '#2563EB' : '#C5A66A',
        strokeWidth: 2,
      },
      labelStyle: {
        fontSize: 10,
        fontWeight: 600,
        fill: '#172B40',
      },
      labelBgStyle: {
        fill: '#FFFFFF',
        fillOpacity: 0.9,
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: e.label === 'CHANGED_ON' ? '#059669' : e.label === 'SUPPORTED_BY' ? '#2563EB' : '#C5A66A',
      },
    }));

    return { nodes: formattedNodes, edges: formattedEdges };
  };

  useEffect(() => {
    const loadGraph = async () => {
      setLoading(true);
      try {
        const data = await getGraphData(selectedPlaceId);
        const { nodes: fn, edges: fe } = layoutGraph(data.nodes, data.edges);
        setNodes(fn);
        setEdges(fe);
      } catch (err) {
        console.error('Failed to load graph data:', err);
      } finally {
        setLoading(false);
      }
    };
    loadGraph();
  }, [selectedPlaceId]);

  const onNodeClick = useCallback((event, node) => {
    if (node.data?.raw) {
      setSelectedNode(node.data.raw);
    }
  }, []);

  const handlePlaceChange = (e) => {
    const val = e.target.value;
    setSelectedPlaceId(val);
    setSearchParams({ place: val });
    setSelectedNode(null);
  };

  return (
    <div className="space-y-4 max-w-6xl mx-auto py-2">
      {/* Top Header & Selector */}
      <div className="bg-white rounded-2xl p-5 border border-gray-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-[#C5A66A]/20 text-[#172B40] flex items-center justify-center shrink-0">
            <Network className="w-5 h-5 text-[#C5A66A]" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-[#172B40]">
              {t('graph.title', 'Historical Relationship Explorer')}
            </h2>
            <p className="text-xs text-gray-500">
              {lang === 'ta'
                ? 'ஊர்கள், வரலாற்றுப் பெயர்கள், மாற்ற நிகழ்வுகள் மற்றும் ஆவணங்களுக்கிடையேயான உறவுகள்'
                : 'Interactive relational network of places, historical names, events, and primary sources.'}
            </p>
          </div>
        </div>

        {/* Place Dropdown */}
        <div className="flex items-center gap-2">
          <label className="text-xs font-semibold text-gray-600 shrink-0">
            {lang === 'ta' ? 'இடத்தைத் தேர்ந்தெடுக்கவும்:' : 'Select place:'}
          </label>
          <select
            value={selectedPlaceId}
            onChange={handlePlaceChange}
            className="px-3 py-1.5 bg-[#F7F4ED] border border-gray-300 rounded-lg text-xs font-semibold text-[#172B40] focus:outline-none focus:border-[#C5A66A]"
          >
            {placesList.map((p) => (
              <option key={p.id} value={p.id}>
                {lang === 'ta' && p.current_name_tamil ? p.current_name_tamil : p.current_name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Interactive Canvas Container */}
      <div className="relative bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden h-[580px] flex">
        {loading ? (
          <div className="m-auto text-center text-gray-500 text-sm">
            <div className="inline-block animate-spin w-7 h-7 border-2 border-[#172B40] border-t-transparent rounded-full mb-3"></div>
            <p>{t('common.loading', 'Building relationship network...')}</p>
          </div>
        ) : (
          <div className="w-full h-full relative">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onNodeClick={onNodeClick}
              fitView
              minZoom={0.2}
              maxZoom={1.5}
            >
              <Background color="#E2E8F0" gap={16} />
              <Controls />
            </ReactFlow>

            {/* Legend on Bottom Left */}
            <div className="absolute bottom-4 left-4 bg-white/95 backdrop-blur p-3 rounded-xl border border-gray-200 shadow-md text-xs space-y-1.5 z-10 pointer-events-auto">
              <span className="font-bold text-gray-700 block text-[11px] uppercase tracking-wider mb-1">
                {t('graph.legend', 'Graph Legend')}
              </span>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-white border-2 border-[#172B40] inline-block"></span>
                <span className="text-gray-600">{t('graph.place', 'Current Place')}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded bg-[#FFFBEB] border border-[#FDE68A] inline-block"></span>
                <span className="text-gray-600">{t('graph.historicalName', 'Historical Name')}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded bg-[#ECFDF5] border border-[#A7F3D0] inline-block"></span>
                <span className="text-gray-600">{t('graph.eventNode', 'Event')}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded bg-[#EFF6FF] border border-[#BFDBFE] inline-block"></span>
                <span className="text-gray-600">{t('graph.sourceNode', 'Source Document')}</span>
              </div>
            </div>

            {/* Side Panel for Node Inspection */}
            {selectedNode && (
              <div className="absolute top-4 right-4 w-80 bg-white/98 backdrop-blur p-5 rounded-2xl border border-gray-200 shadow-xl z-20 space-y-3 max-h-[530px] overflow-y-auto animate-in fade-in duration-200">
                <div className="flex items-start justify-between gap-2 border-b border-gray-100 pb-2">
                  <div className="space-y-0.5">
                    <span className="text-[10px] uppercase font-bold text-[#C5A66A] tracking-wider">
                      {selectedNode.type}
                    </span>
                    <h4 className="font-bold text-base text-[#172B40]">
                      {selectedNode.label}
                    </h4>
                  </div>
                  <button
                    onClick={() => setSelectedNode(null)}
                    className="p-1 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="text-xs space-y-2 text-gray-600">
                  {selectedNode.type === 'place' && (
                    <>
                      {selectedNode.data?.current_name_tamil && (
                        <div>
                          <span className="font-semibold text-gray-800">
                            {lang === 'ta' ? 'தமிழ் பெயர்:' : 'Tamil Name:'}
                          </span>{' '}
                          {selectedNode.data.current_name_tamil}
                        </div>
                      )}
                      <div>
                        <span className="font-semibold text-gray-800">
                          {lang === 'ta' ? 'மாவட்டம்:' : 'District:'}
                        </span>{' '}
                        {selectedNode.data?.district || '-'}
                      </div>
                    </>
                  )}

                  {selectedNode.type === 'historical_name' && (
                    <>
                      <div>
                        <span className="font-semibold text-gray-800">
                          {lang === 'ta' ? 'வகை:' : 'Name Type:'}
                        </span>{' '}
                        {selectedNode.data?.name_type}
                      </div>
                      <div>
                        <span className="font-semibold text-gray-800">
                          {lang === 'ta' ? 'மொழி:' : 'Language:'}
                        </span>{' '}
                        {selectedNode.data?.language}
                      </div>
                      {(selectedNode.data?.valid_from || selectedNode.data?.valid_to) && (
                        <div>
                          <span className="font-semibold text-gray-800">
                            {lang === 'ta' ? 'காலம்:' : 'Documented Period:'}
                          </span>{' '}
                          {selectedNode.data.valid_from || '?'} - {selectedNode.data.valid_to || '?'}
                        </div>
                      )}
                    </>
                  )}

                  {selectedNode.type === 'event' && (
                    <>
                      <div>
                        <span className="font-semibold text-gray-800">
                          {lang === 'ta' ? 'நிகழ்வு வகை:' : 'Event Type:'}
                        </span>{' '}
                        {selectedNode.data?.event_type}
                      </div>
                      <div>
                        <span className="font-semibold text-gray-800">
                          {lang === 'ta' ? 'தேதி:' : 'Date:'}
                        </span>{' '}
                        {selectedNode.data?.event_date || 'Date unknown'}
                      </div>
                      <div className="pt-1">
                        <span className="font-semibold text-gray-800 block mb-0.5">
                          {lang === 'ta' ? 'விளக்கம்:' : 'Description:'}
                        </span>
                        <p className="text-gray-700 leading-relaxed bg-[#F7F4ED] p-2 rounded">
                          {selectedNode.data?.description}
                        </p>
                      </div>
                      <div className="pt-1">
                        <StatusBadge status={selectedNode.data?.evidence_status} />
                      </div>
                    </>
                  )}

                  {selectedNode.type === 'source' && (
                    <>
                      <div>
                        <span className="font-semibold text-gray-800">
                          {lang === 'ta' ? 'வெளியீடு:' : 'Publisher:'}
                        </span>{' '}
                        {selectedNode.data?.publisher}
                      </div>
                      {selectedNode.data?.document_identifier && (
                        <div>
                          <span className="font-semibold text-gray-800">
                            {lang === 'ta' ? 'ஆவண எண்:' : 'Document ID:'}
                          </span>{' '}
                          <span className="font-mono">{selectedNode.data.document_identifier}</span>
                        </div>
                      )}
                      {selectedNode.data?.source_url && (
                        <div className="pt-2">
                          <a
                            href={selectedNode.data.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800 font-semibold"
                          >
                            <span>{lang === 'ta' ? 'ஆவண இணைப்பைத் திற' : 'Open Source Document'}</span>
                            <ExternalLink className="w-3.5 h-3.5" />
                          </a>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RelationshipGraph;
