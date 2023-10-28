function updateCartCount(em1,id,url){
    $.ajax({
        type:'GET',
        url:url,
        data:{
            prod_id:id
        },
        success:function(data){
            em1.innerHTML=data.quantity
            document.getElementById('amount').innerHTML=data.amount
            document.getElementById('totalamount').innerHTML=data.totalamount
            console.log('data : ',data);
        }
    })
}

$('.plus-cart').click(function(){
    var em1=this.parentNode.children[2]
    var id= $(this).attr('pid').toString()
    console.log('pid :',id);
    var url='/pluscart';
    updateCartCount(em1,id,url);
})

$('.minus-cart').click(function(){
    var em1=this.parentNode.children[2]
    var id= $(this).attr('pid').toString()
    console.log('pid :',id);
    var url='/minuscart';
    updateCartCount(em1,id,url);
})


$('.remove-cart').click(function(){
    var em1=this
    var id= $(this).attr('pid').toString()
    console.log(id)
    $.ajax({
        type:'GET',
        url:'/removecart',
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById('amount').innerHTML=data.amount
            document.getElementById('totalamount').innerHTML=data.totalamount
            em1.parentNode.parentNode.parentNode.parentNode.remove()
            console.log('data : ',data);
        }
    })
})

$('.plus-wishlist').click(function(){
    var id= $(this).attr('pid').toString()
    $.ajax({
        type:"GET",
        url:'/pluswhishlist',
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href=`http://localhost:8000/product-detail/${id}`
        }

    })

})

$('.minus-wishlist').click(function(){
    var id= $(this).attr('pid').toString()
    $.ajax({
        type:"GET",
        url:'/minuswhishlist',
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href=`http://localhost:8000/product-detail/${id}`
        }

    })

})