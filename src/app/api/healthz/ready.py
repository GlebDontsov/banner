from fastapi import HTTPException, Request, status
from sqlalchemy import text


async def ready(request: Request) -> int:
    """Ready."""
    try:
        request.app.state.session.execute(text('SELECT 1'))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Failed to connect to the database',
        )
    return status.HTTP_200_OK
