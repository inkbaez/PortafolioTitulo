document.getElementById('idtipo').addEventListener('change', function () {
    var select = document.getElementById("idtipo");
    var options = document.getElementsByTagName("option");
    console.log(select.value);
    if (select.value == 2) {
        document.getElementById('divApellido').hidden = true
        document.getElementById('apellidoValue').value = 'Empresa, Campo no requerido.'
    }
    else
    {
        document.getElementById('divApellido').hidden = false
        document.getElementById('apellidoValue').value = ''
    }
});