function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

document.addEventListener("DOMContentLoaded", function(event) {
    var elts = document.getElementsByClassName("poster");

    for(var i = 0; i < elts.length; i++) {
    num_poster = elts[i].getAttribute("id").split("poster")[1];
    elts[i].num_poster = num_poster;
    elts[i].addEventListener("click", function callAjax(e){
        e.preventDefault();
        url = "/vote_poster"
        var xmlhttp;
        xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function(){
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
                setCookie("user_id", xmlhttp.responseText, 2)
                user_id = getCookie("user_id");
                window.location = "/vote_succeed";
            }
        }
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        var options = {excludeWebGL: true, excludeCanvas: true}
        new Fingerprint2(options).get(function(result, components){
            user_id = getCookie("user_id");
            if(user_id == ""){
                user_id = "no_id";
            }

            xmlhttp.send("hash="+result+"&poster="+e.target.num_poster+"&user_id="+user_id);
        });
    }, false);

    }
});