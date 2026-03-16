# redirects the user to a login page
from starlette.status import HTTP_400_BAD_REQUEST
from app.exceptions.users import UserNotFound
from app.db.users import read_user
from app.db.authorizations import create_authorization
from fastapi import APIRouter
from app.constants import ALGORITHM
from app.constants import SECRET_KEY
import jwt
from app.typing.token import TokenData
from fastapi.responses import RedirectResponse
from fastapi import Response
from fastapi import Request
from redis import Redis

router = APIRouter(prefix="/oauth")


@router.get("/authorize")
async def authorize(
    request: Request,
    response: Response,
    scope: str,
    client_id: str,
    redirect_uri: str | None,
    state: str | None,
    response_type: str = "code",
):
    if response_type != "code":
        response.status_code = HTTP_400_BAD_REQUEST
        return response

    access_token: str | None = request.session.get("access_token")
    if access_token is None:
        # Browser is not logged in
        return RedirectResponse(url=f"/login?scope={scope}")

    token_data = TokenData.model_validate(jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM))
    username = token_data.sub

    redis_client: Redis = request.state["redis_client"]

    user = read_user(
        redis_client=redis_client,
        username=username,
    )
    if user is None:
        raise UserNotFound
    authorization_code = create_authorization(
        redis_client=redis_client,
        user_id=user.user_id,
        client_id=client_id,
        scope=scope,
    )
    return RedirectResponse(url=f"{redirect_uri}?code={authorization_code}&state={state}")
