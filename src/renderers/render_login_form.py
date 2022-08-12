def render(csrf_token):
    html = ''
    html += f"""
    <div class="sep20"></div>
    <div class='login_form'>
        <form id="loginForm">
            <label> Username: </label>
            <h4> Login Form </h4>
            <input type="text" name="user" />
    
            <label> Password: </label>
            <input type="password" name="pass"/>
    
            <input type="hidden" name="csrfToken" value = "{csrf_token}" />
    
            <button id="loginSubmit"> Login </button>
            <button id="loginReset"> Reset </button>
    
        </form>
    </div>
    """
    return html


