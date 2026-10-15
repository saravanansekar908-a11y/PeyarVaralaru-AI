"""
Graph API route — generates nodes and edges for React Flow visualization.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, Place
from app.schemas import GraphData, GraphNode, GraphEdge

router = APIRouter(prefix="/api", tags=["graph"])


@router.get("/graph/{place_id}", response_model=GraphData)
def get_place_graph(place_id: int, db: Session = Depends(get_db)):
    """Generate graph nodes and edges for a place and its relationships."""
    place = db.query(Place).filter(Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")

    nodes = []
    edges = []

    # Place node (center)
    place_node_id = f"place-{place.id}"
    nodes.append(GraphNode(
        id=place_node_id,
        label=place.current_name,
        type="place",
        data={
            "current_name_tamil": place.current_name_tamil or "",
            "district": place.district or "",
        }
    ))

    # Historical name nodes
    for hn in place.historical_names:
        hn_node_id = f"histname-{hn.id}"
        nodes.append(GraphNode(
            id=hn_node_id,
            label=hn.name,
            type="historical_name",
            data={
                "language": hn.language or "",
                "name_type": hn.name_type or "",
                "valid_from": hn.valid_from or "",
                "valid_to": hn.valid_to or "",
            }
        ))
        edges.append(GraphEdge(
            id=f"edge-place-hn-{hn.id}",
            source=place_node_id,
            target=hn_node_id,
            label="HAS_HISTORICAL_NAME",
        ))

    # Event nodes and source nodes
    seen_sources = set()
    for evt in place.events:
        evt_node_id = f"event-{evt.id}"
        nodes.append(GraphNode(
            id=evt_node_id,
            label=evt.event_date or evt.event_type,
            type="event",
            data={
                "event_type": evt.event_type,
                "event_date": evt.event_date or "",
                "description": evt.description or "",
                "evidence_status": evt.evidence_status,
            }
        ))
        edges.append(GraphEdge(
            id=f"edge-place-evt-{evt.id}",
            source=place_node_id,
            target=evt_node_id,
            label="CHANGED_ON",
        ))

        for src in evt.sources:
            src_node_id = f"source-{src.id}"
            if src.id not in seen_sources:
                nodes.append(GraphNode(
                    id=src_node_id,
                    label=src.title,
                    type="source",
                    data={
                        "publisher": src.publisher or "",
                        "source_url": src.source_url or "",
                        "document_identifier": src.document_identifier or "",
                    }
                ))
                seen_sources.add(src.id)

            edges.append(GraphEdge(
                id=f"edge-evt-src-{evt.id}-{src.id}",
                source=evt_node_id,
                target=src_node_id,
                label="SUPPORTED_BY",
            ))

    return GraphData(nodes=nodes, edges=edges)
