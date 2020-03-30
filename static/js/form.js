function get_current_datetime() {
    const today = new Date();
    const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    const time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return date + ' ' + time;
}

function get_current_datetime_id() {
    const today = new Date();
    const date = today.getFullYear() + '_' + (today.getMonth() + 1) + '_' + today.getDate();
    const time = today.getHours() + "_" + today.getMinutes() + "_" + today.getSeconds();
    return date + '_' + time;
}

function send_request(form_id) {

    const xhr = new XMLHttpRequest();
    const my_form = new FormData();
    const input_array = $('#' + form_id + ' input');
    my_form.append('function_name', form_id);
    for (let i = 0; i < input_array.length; ++i) {
        if (not_empty(input_array[i].name)) {
            my_form.append(input_array[i].name, input_array[i].value);
        }
    }
    xhr.onreadystatechange = function () {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            document.getElementById('function_result').innerHTML += get_function_result_html(form_id, xhr.responseText);
        }
    };

    xhr.open("POST", document.getElementById(form_id).getAttribute("action"));
    xhr.send(my_form);
}


function get_function_result_html(function_name, function_result) {
    const result_dict = $.parseJSON(function_result);
    let result_tab_html_head = '';
    let result_tab_html_body = '';
    let dict_count = 0;
    const datetime_id = get_current_datetime_id();
    $.each(result_dict, function (dict_key, dict_value) {
        if (dict_count === 0) {
            if (typeof dict_value === "object") {
                dict_value = JSON.stringify(dict_value);
            }
            result_tab_html_head += '<a id="' + datetime_id + function_name + dict_key + '" onclick="click_item(\'' + datetime_id + function_name + dict_key + '\')" class="ui vertical item ' + 'active' + '">' + dict_key + '</a>';
            result_tab_html_body += '<textarea disabled cols="30" class="ui attached tab segment active field form"\n' +
                'id="' + datetime_id + function_name + dict_key + 'tab"' +
                ' style="width: 100%;height: 35px;border: none">' + dict_value + '</textarea>';
        } else {
            if (typeof dict_value === "object") {
                dict_value = JSON.stringify(dict_value);
            }
            result_tab_html_head += '<a id="' + datetime_id + function_name + dict_key + '" onclick="click_item(\'' + datetime_id + function_name + dict_key + '\')" class="ui vertical item">' + dict_key + '</a>';
            result_tab_html_body += '<textarea disabled cols="30" class="ui attached tab segment field form"\n' +
                'id="' + datetime_id + function_name + dict_key + 'tab"' +
                ' style="width: 100%;height: 35px;border: none">' + dict_value + '</textarea>';
        }
        dict_count += 1;
    });
    let overflow = '';
    if (dict_count > 3) {
        overflow = 'overflow: scroll;';
    }
    const result_html = '<div class="ui feed">\n' +
        '<div class="event" style="margin-left: 45%;margin-right: 3%">\n' +
        '<div class="label">\n' +
        '<i style="display: none" class="chevron up icon" onclick="down_result(\'' + function_name + datetime_id + '\')" id="' + function_name + datetime_id + 'up"></i>' +
        '<i class="chevron down icon" onclick="up_result(\'' + function_name + datetime_id + '\')" id="' + function_name + datetime_id + 'down"></i>' +
        '</div>\n' +
        '<div class="content">\n' +
        '<div class="summary">' + function_name +
        '<div class="date">' + get_current_datetime() + '</div>\n' +
        '<div class="ui divided selection list" id="' + function_name + datetime_id + '">\n' +
        '<div class="ui vertical secondary attached tabular menu" style="float: left;width: 15%;max-height: 200px;' + overflow + '">\n' +
        result_tab_html_head +
        '</div>\n' +
        '<div style="float: left" class="vertical">\n' +
        result_tab_html_body +
        '</div>\n' +
        '</div>\n' +
        '</div>\n' +
        '</div>\n' +
        '</div>\n' +
        '</div>';


    return result_html;
}

function check_select_value(main_div) {

    main_div.getElementsByTagName('input')[1].value = main_div.getElementsByTagName('span')[0].innerText;

    return true;

}


function not_empty(str) {
    return str !== '' && str !== null && str !== undefined;
}


function click_item(item_id) {

    const current_item = document.getElementById(item_id);
    const item_brothers = current_item.parentNode.children;
    for (let i = 0; i < item_brothers.length; i++) {
        item_brothers[i].classList.remove('active');
    }
    current_item.classList.add('active');

    const current_tab = document.getElementById(item_id + 'tab');
    const tab_brothers = current_tab.parentNode.children;
    for (let i = 0; i < tab_brothers.length; i++) {
        tab_brothers[i].classList.remove('active');
    }
    current_tab.classList.add('active');
}

function up_result(result_id) {
    document.getElementById(result_id + 'up').style.display = 'block';
    document.getElementById(result_id + 'down').style.display = 'none';
    document.getElementById(result_id).style.display = 'none';
}

function down_result(result_id) {
    document.getElementById(result_id + 'up').style.display = 'none';
    document.getElementById(result_id + 'down').style.display = 'block';
    document.getElementById(result_id).style.display = 'block';
}