import aiohttp
from aiohttp import web
import yarl


async def proxy_handler(request: web.Request) -> web.Response:
    """
    Check request contains http url in query args:
        /fetch?url=http%3A%2F%2Fexample.com%2F
    and trying to fetch it and return body with http status.
    If url passed without scheme or is invalid raise 400 Bad request.
    On failure raise 502 Bad gateway.
    :param request: aiohttp.web.Request to handle
    :return: aiohttp.web.Response
    """
    # print(request.query)
    session = request.app['session']
    if 'url' not in request.query:
        raise web.HTTPBadRequest(body=b'No url to fetch')
    url = request.query['url']
    url_new = yarl.URL(url)
    # print(url_new.scheme)
    if url_new.scheme == '':
        exp = web.HTTPBadRequest(body=b'Empty url scheme')
        raise exp
        # return web.Response(body=b'Empty url scheme', status=400)
    if url_new.scheme != 'http' and url_new.scheme != '':
        raise web.HTTPBadRequest(body=b'Bad url scheme: ftp')
        # return web.Response(body=b'Bad url scheme: ftp', status=400)
    # if url == '':
    #     raise web.HTTPBadRequest(body=b'No url to fetch')
    # try:
    async with session.get(url) as resp:
        if resp.status == 500:
            raise web.HTTPInternalServerError(body=b'Internal server error')
        if resp.status == 200:
            text = await resp.text()
            # print(text)
            # raise web.HTTPOk(body=text)
            if text != b'OK':
                # print('sdf')
                raise web.HTTPOk(text=text)
            else:
                raise web.HTTPOk(body=b'OK')
            # raise web.HTTPOk(body=b'OK', text=text)
        return resp
    # except Exception as exp:
    #     print("sdf")


async def setup_application(app: web.Application) -> None:
    """
    Setup application routes and aiohttp session for fetching
    :param app: app to apply settings with
    """
    # print(app.router, app.)
    app.router.add_get('/fetch', proxy_handler)
    app['session'] = aiohttp.ClientSession()


async def teardown_application(app: web.Application) -> None:
    """
    Application with aiohttp session for tearing down
    :param app: app for tearing down
    """
    # await app.shutdown()
