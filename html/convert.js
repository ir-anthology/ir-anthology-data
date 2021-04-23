example_hex = "5b7b22726f6c65223a2022617574686f72222c202264626c706964223a20224d6172776120457373616d227d5d"
example_json = '[{"role": "author", "dblpid": "Marwa Essam"}]'
document.getElementById("hex").value = example_hex
document.getElementById("json").value = example_json

function readtextarea(id){
    return document.getElementById(id).value.replaceAll("\r","")
}
function utf8_2_hex(input) {
    input = utf8.encode(input)
    var output = "";
    for(var i = 0; i < input.length; i++) {
        output += input[i].charCodeAt(0).toString(16);
    }
    return output;
}
function hex_2_utf8(input) {
    var output = ""
    for (i = 0; i < input.length; i += 2){
        output += String.fromCharCode(parseInt(input.substr(i, 2), 16));
    }
    return utf8.decode(output);
}
function updatejson(){
    document.getElementById("json").value = hex_2_utf8(readtextarea("hex"));
}
function updatehex(){
    jsoninput = readtextarea("json")
    try {
        JSON.parse(jsoninput);
        document.getElementById("hex").value = utf8_2_hex(jsoninput);
    } catch (e) {
        document.getElementById("hex").value = "invalid json"
    }
}
document.getElementById("hex").onkeyup = updatejson
document.getElementById("json").onkeyup = updatehex