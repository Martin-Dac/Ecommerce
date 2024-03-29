var actubtn = document.getElementsByClassName('Actu-Carrito')

for( var i = 0; i < actubtn.length; i++){
    actubtn[i].addEventListener('click', function(){
        var productoId = this.dataset.producto
        var accion = this.dataset.action
        console.log('productoId', productoId, 'accion: ', accion)
        console.log('USER: ', user)
        if(user === 'AnonymousUser'){
            alert("Para comprar hay que iniciar sesion")
        }
        else{
            UpdateUserOrder(productoId, accion)
        }
    })
}

function UpdateUserOrder(productoId, accion){
    console.log('Hola', user)

    var url = '/update_Item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productoId': productoId, 'accion': accion})
    })

    .then((response) =>{
        return response.json()
    })

    .then((data) =>{
        console.log('data:', data)
        location.reload()
    })
}

window.addEventListener("resize", function (){
    let actual_width = window.innerWidth;
    let ChangeH1 = document.querySelectorAll('.ChH1');

    for(i in ChangeH1){
        if(actual_width < 550){
            ChangeH1[i].outerHTML = '<h2 class="ChH1">' + ChangeH1[i].innerHTML + '<h2>';
            console.log('test'); 
        }
        else{
            ChangeH1[i].outerHTML = '<h1 class="ChH1">' + ChangeH1[i].innerHTML + '<h1>';
            console.log('test2');
        }
    }
});