$(function(){
    $('#btn').click(function(){
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())
        formData.append('file', document.getElementById('file').files[0])
        formData.append('title', $('#title').val())
        formData.append('text', $('#text').val())
            $.ajax('/post_create/', {
                'type': 'POST',
                'async': true,
                'dataType': 'json',
                'data': formData,
                'contentType': false,
                'processData': false,
                'success': function(data){
                    document.getElementById('title').innerHTML = data['title']
                    document.getElementById('text').innerHTML = data['text']
                    document.getElementById('file').innerHTML = data['file']
                }
            })
    })
})
$(document).ready(function(){
})