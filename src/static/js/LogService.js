const LogService = {

    test() {
        console.log('TEST LOGS');
    },

    saveLog() {

        // let currentDateTime = new Date().toUTCString();
        let currentDate = new Date().toISOString().slice(0, 10); // 2022-08-01
        let count = 1;
        let url = "/save_log?current_date=" + currentDate + "&count=" + count;
        let fetchPromise = fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function(response) {
            return response.json();
        }).then(function(data) {
            console.log(data);
        }).catch(function(err) {
            console.log('Error', err);
        });
        return fetchPromise;
    }

};

export { LogService };

