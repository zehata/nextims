# redirects the user to a login page
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


@router.get("/login")
async def get_login(
    request: Request,
    response: Response,
    scope: str,
    client_id: str,
    redirect_uri: str | None,
    state: str | None,
    response_type: str = "code",
):
    if response_type != "code":
        response.status_code = 400
        return response
    access_token: str | None = request.session.get("access_token")
    if access_token is None:
        # Browser is not logged in
        return RedirectResponse(url=login_url)
    token_data = TokenData.model_validate(jwt.decode(access_token, SECRET_KEY, algorithm=ALGORITHM))
    username = token_data.sub

    redis_client: Redis = request.state["redis_client"]

    user = read_user(
        redis_client=redis_client,
        username=username,
    )
    authorization_code = create_authorization(
        redis_client=redis_client,
        user_id=user.user_id,
        client_id=client_id,
    )
    return RedirectResponse(url=f"{redirect_uri}?code={authorization_code}&state={state}")
