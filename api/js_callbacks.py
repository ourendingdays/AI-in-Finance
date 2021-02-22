BUTTON_PRED = """
    function sleep(milliseconds) {
        const date = Date.now();
        let currentDate = null;
        do {
            currentDate = Date.now();
        } while (currentDate - date < milliseconds);
        }

    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/predict";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"predict": "True"});
    xhr.send(data);
    console.log(data);
    sleep(3000);
    alert('Prediction is ready!');
"""

BUTTON_DATE = """
    plot.x_range.start = Date.parse(new Date(cb_obj.value));

    var st_date = cb_obj.value;
    console.log(st_date)
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/predict_date";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"start_date": st_date});
    xhr.send(data);
    console.log(data);
"""

BUTTON_DATE_END = """
    plot.x_range.end = Date.parse(new Date(cb_obj.value));

    var end_date = cb_obj.value;
    console.log(end_date);
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/predict_date_end";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"end_date": end_date});
    xhr.send(data);
    console.log(data);
"""

BUTTON_DATE_END = """
    plot.x_range.end = Date.parse(new Date(cb_obj.value));

    var end_date = cb_obj.value;
    console.log(end_date);
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/predict_date_end";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"end_date": end_date});
    xhr.send(data);
    console.log(data);
"""

BUTTON_TAB = """
    var model = cb_obj.active;
    console.log(model)
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/predict_model";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"model": model});
    xhr.send(data);
    console.log(data);
"""

BUTTON_RESET = """
    var x = source.data["ds"];
    var y = source.data["yhat"];

    var y_lower = source.data["yhat_lower"];
    var y_upper = source.data["yhat_upper"];
    var y_actual = source.data["y_actual"];


    var req = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/prophet";

    req.responseType = 'json';
    req.open('GET', url, true);
    req.onload = function() {
        var jsonResponse = req.response;
        console.log('res', jsonResponse);
        var data = jsonResponse;

        console.log('data: ', data.data["ds"]);

        x = data.data["ds"];
        y = data.data["yhat"];
        y_lower = data.data["yhat_lower"];
        y_upper = data.data["yhat_upper"];
        y_actual = data.data["y_actual"];

        x.forEach(function(part, index, theArray) {
            theArray[index] = Date.parse(new Date(theArray[index]));
        });

        source.data["x"] = x;
        source.data["y"] = y;
        source.data["yhat_lower"] = y_lower;
        source.data["yhat_upper"] = y_upper;
        source.data["y_actual"] = y_actual;

        console.log(y_actual);

        console.log(x, y);
        source.change.emit();
        console.log(source);

        var y_range_arr = y;
        var yrange_max = Math.max.apply(Math, y_range_arr) * 1.05;

        var x_min = Date.parse(new Date(x[0]));
        var x_max = Date.parse(new Date('2021-12-31'));

        console.log(0, yrange_max, x_min, x_max);

        plot.y_range.start = 0;
        plot.y_range.end = yrange_max;
        plot.x_range.start = x_min;
        plot.x_range.end = x_max;

    };
    req.send(null);
"""

BUTTON_RESET_ARIMA = """
    var x = source.data["ds"];
    var y = source.data["yhat"];
    var y_actual = source.data["y_actual"];
    var y_lower = source.data["yhat_lower"];
    var y_upper = source.data["yhat_upper"];


    var req = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/arima";

    req.responseType = 'json';
    req.open('GET', url, true);
    req.onload = function() {
        var jsonResponse = req.response;
        console.log('res', jsonResponse);
        var data = jsonResponse;

        console.log('data: ', data.data["ds"]);

        x = data.data["ds"];
        y = data.data["yhat"];
        y_actual = data.data["y_actual"];
        y_lower = data.data["yhat_lower"];
        y_upper = data.data["yhat_upper"];

        x.forEach(function(part, index, theArray) {
            theArray[index] = Date.parse(new Date(theArray[index]));
        });

        source.data["x"] = x;
        source.data["y"] = y;
        source.data["y_actual"] = y_actual;
        source.data["yhat_lower"] = y_lower;
        source.data["yhat_upper"] = y_upper;

        console.log(y_actual);

        console.log(x, y);
        source.change.emit();
        console.log(source);

        var y_range_arr = y;
        var yrange_max = Math.max.apply(Math, y_range_arr) * 1.05;

        var x_min = Date.parse(new Date(x[0]));
        var x_max = Date.parse(new Date('2021-12-31'));

        console.log(0, yrange_max, x_min, x_max);

        plot.y_range.start = 0;
        plot.y_range.end = yrange_max;
        plot.x_range.start = x_min;
        plot.x_range.end = x_max;

    };
    req.send(null);
"""

BUTTON_RESET_LSTM = """
    var x = source.data["ds"];
    var y = source.data["yhat"];
    var y_actual = source.data["y_actual"];
    var y_lower = source.data["yhat_lower"];
    var y_upper = source.data["yhat_upper"];

    var req = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/lstm";

    req.responseType = 'json';
    req.open('GET', url, true);
    req.onload = function() {
        var jsonResponse = req.response;
        console.log('res', jsonResponse);
        var data = jsonResponse;

        console.log('data: ', data.data["ds"]);

        x = data.data["ds"];
        y = data.data["yhat"];
        y_actual = data.data["y_actual"];
        y_lower = data.data["yhat_lower"];
        y_upper = data.data["yhat_upper"];

        x.forEach(function(part, index, theArray) {
            theArray[index] = Date.parse(new Date(theArray[index]));
        });

        source.data["x"] = x;
        source.data["y"] = y;
        source.data["y_actual"] = y_actual;
        source.data["yhat_lower"] = y_lower;
        source.data["yhat_upper"] = y_upper

        console.log(x, y);
        source.change.emit();
        console.log(source);

        var y_range_arr = y;
        var yrange_max = Math.max.apply(Math, y_range_arr) * 1.05;

        var x_min = Date.parse(new Date(x[0]));
        var x_max = Date.parse(new Date('2021-12-31'));

        console.log(0, yrange_max, x_min, x_max);

        plot.y_range.start = 0;
        plot.y_range.end = yrange_max;
        plot.x_range.start = x_min;
        plot.x_range.end = x_max;

    };
    req.send(null);
"""


CHECKBOX = """
    console.log('checkbox_group: active=' + this.active)

    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/combine";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"active": this.active});
    xhr.send(data);
    console.log(data);
"""

UPDATE = """
    console.log('checkbox_group: active=' + this.active)

    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/dashboard";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    var data = JSON.stringify({"active": this.active});
    xhr.send(data);
    console.log(data);
    sleep(3000);
    alert('Update is ready!');
"""
