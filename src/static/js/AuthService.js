let AuthService = {

    // TODO: Put this in a separate utill.js file to re-use this func
    redirect(url) {
      window.location.href = url
    },

    // TODO: Put this in a separate utill.js file to re-use this func
    escapeInput(input) {
        return input.toString()
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;")
             .replace(/^\s+|\s+$/g,''); // trim
     },

    // TODO: Put this in a separate utill.js file to re-use this func
    setCookie(cookieName, cookieVal, minutes) {
      const now = new Date();
      now.setTime(now.getTime() + (minutes * 60 * 1000));
      const expires = "expires="+ now.toUTCString();
      document.cookie = cookieName + "=" + cookieVal + ";" + expires + ";path=/";
    },

    // TODO: Put this in a separate utill.js file to re-use this func
    getCookie(cookieName) {
      let name = cookieName + "=";
      let decodedCookie = decodeURIComponent(document.cookie);
      let ca = decodedCookie.split(';');
      for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
          c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
          return c.substring(name.length, c.length);
        }
      }
      return "";
    },

    // TODO: Put this in a separate utill.js file to re-use this func
    deleteAllCookies() {
        let allCookies = document.cookie.split(';');
        for (let i = 0; i < allCookies.length; i++) {
            document.cookie = allCookies[i] + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
        }
    },

    ajaxLogout(input_uid_mask) {

        const input = {
            uid_mask: input_uid_mask
        };

        fetch("/logout", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(input),
        }).then(function(res){
            return res.json();
        }).then(function(data) {
           if (typeof data !== undefined && data !== null && data.redirect === 1) {
             let uid_mask = AuthService.getCookie('uid_mask');
             let role_mask = AuthService.getCookie('role_mask');
             let temp_token = AuthService.getCookie('temp_token');
             AuthService.deleteAllCookies();
             AuthService.redirect('http://localhost:8000/');
           }
        }).catch(function(err) {
            console.log('Error', err);
        });

    },

    isUserLoggedIn() {
        let temp_token = AuthService.getCookie('temp_token');
        if (temp_token !== undefined && temp_token !== null && temp_token !== '') {
            return true;
        }
        return false;
    },

    ajaxLogin(input) {

        fetch("/login_ajax", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(input),
        })
        .then(function(res){
            return res.json();
        }).then(function(data) {
            if (!data) {
                redirect('http://localhost:8000/');
            } else {
                AuthService.setCookie('uid_mask', data.uid_mask, 30);
                AuthService.setCookie('role_mask', data.role_mask, 30);
                AuthService.setCookie('temp_token', data.temp_token, 30);
                AuthService.redirect('http://localhost:8000/secret');
            }
        }).catch(function(err) {
            console.log('Error', err);
        });

    },

    timeTerminate(minutes) {
      let timeToReload = minutes * 60 * 1000;
      setInterval(function() {
        let temp_token = AuthService.getCookie('temp_token');
        if (temp_token !== undefined && temp_token !== null) {
          AuthService.deleteAllCookies();
          window.alert('Session expired!');
          window.location.href = 'http://localhost:8000/';
        }
      }, timeToReload);
    },

    init() {

        const ajaxLoginLink = document.querySelector('#loginSubmit');
        if (typeof ajaxLoginLink !== undefined && ajaxLoginLink !== null) {
            ajaxLoginLink.addEventListener('click', function(event) {

                event.preventDefault();
                const form = document.querySelector('#loginForm');

                let user = form['user'].value;
                let password = form['pass'].value;
                let csrfToken = form['csrfToken'].value;

                const input = {
                    user: AuthService.escapeInput(user),
                    password: AuthService.escapeInput(password),
                    csrfToken: AuthService.escapeInput(csrfToken)
                };
                AuthService.ajaxLogin(input);
            });
        }

        const ajaxLogoutLink = document.querySelector('#ajax-logout');
        if (typeof ajaxLogoutLink !== undefined && ajaxLogoutLink !== null) {
            ajaxLogoutLink.addEventListener('click', function(event){
                event.preventDefault();
                const uid_mask = AuthService.getCookie('uid_mask');
                if (uid_mask !== undefined && uid_mask !== '') {
                    AuthService.ajaxLogout(uid_mask);
                } else {
                    window.alert('You should be logged in first before to logout!');
                }

            });
        }

    }

}

// export { AuthService };

AuthService.init();
AuthService.timeTerminate(60);


