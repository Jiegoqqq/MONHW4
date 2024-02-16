$(document).ready(function(){

    $('#submit').click(function(){
        var strategy= document.getElementById('select')
        var strategy_Value = strategy.value;
        console.log('strategy:', strategy_Value);
        $.ajax({ 
        headers: { 'X-CSRFToken': csrf_token },
            type: 'POST',
            url: '/web_tool/total_list_data/', 
            data: {'strategy':strategy_Value},
            success: function(response) { 
                var url = response.url;
                // Redirect to the new URL
                window.location.href = url;

            },
            error: function(){
                alert('Something error');  
            },
        
        
        })



    })
})