def render(is_user_logged='', user_role='', csrf_token=''):
    html = ''
    html += f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title> f1 </title>
        <link rel="stylesheet" href="./static/css/main.css">
        <link rel="stylesheet" href="./static/css/secret_page.css">
    </head>
    <body>
    <nav class="top-nav">
        <a href="/"> Home </a>
    """
    if is_user_logged != 1:
        html += '<a href="/login_form"> Login </a>'
    else:
        html += '<a href="./secret" > Secret Page </a>'
        html += '<a href="javascript:void(0)" id="ajax-logout"> Logout </a>'
    html += f"""
    </nav>
    <form id="stateForm">
        <input type="hidden" name="isUserLogged" value="{is_user_logged}" />
        <input type="hidden" name="userRole" value="{user_role}" />
        <input type="hidden" name="csrfToken" value="{csrf_token}" />
        <input type="hidden" name="pageNum" value="" />
        <input type="hidden" name="pages" value="" />
        <input type="hidden" name="itemsPerPage" value="" />
    </form>
    """
    return html

