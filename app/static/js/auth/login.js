



function logar_usuario() {
    //solicitacao_novo_cadastro
    event.preventDefault()
    $(document).ready(()=>{
        $.ajax({
            method: "POST",
            url: "/auth/login/user",
            data: {
                email_usuario: $("#email_usuario").val(),
                senha_usuario: $("#senha_usuario").val(),
            }
        }).done((data)=> {
            Swal.fire(
                data
            ).then(function() {
                if (data.hasOwnProperty('icon') && data['icon'] == 'success'){
                    //
                }
            });
        });
    });
}






function redirect_register() {
    //solicitacao_novo_cadastro
    event.preventDefault()
    $(document).ready(()=>{
        window.location.href = "register";
    });
}


