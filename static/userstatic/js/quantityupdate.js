$(document).ready(function(){
    $(".cart_quantity").on('change',function() {
        event.preventDefault();
        // Get the row containing the input
        var row = $(this).closest('tr');
        var cid = parseInt(row.find(".cartid").val());    
        var qty = row.find(this).val();
        var price = row.find('#productprice').val();
    
    location.reload(true);
            $.ajax({
                    url: "{% url 'quantityupdate' %}",
                    method: 'post',
                    cache: false,
                    data: {
                        cid: cid,
                        qty: qty,
                        price: price,
                        csrfmiddlewaretoken: '{{ csrf_token }}'
                    }
                });

    });
});  
