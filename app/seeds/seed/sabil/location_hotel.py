from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.location import Location
from app.seeds.factories import LocationFactory


async def create_location(
    session: AsyncSession,
    lat: str,
    lng: str,
) -> Location:
    """Create a location with the given coordinates."""
    
    location = LocationFactory.build()
    location.lat = lat
    location.lng = lng
    
    session.add(location)
    await session.commit()
    await session.refresh(location)
    return location


async def create_location_optional(
    session: AsyncSession,
    lat: Optional[str] = None,
    lng: Optional[str] = None,
) -> Optional[Location]:
    """Create a location if coordinates are provided."""
    
    if lat and lng:
        return await create_location(session, lat, lng)
    return None
